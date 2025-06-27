## Part 3: The Luigi Pipeline (Orchestration)
Now we will build the Luigi tasks that will automate our ETL process.

### Step 1: The Extract Task
This first task will be responsible for running the Scrapy spider we just built.

Create the file `extract/tasks.py` and copy the following code.

```python
import luigi
import os
import subprocess
from datetime import datetime
from config import RAW_DATA_DIR, SCRAPY_PROJECT_PATH, SPIDER_NAME

class ExtractNews(luigi.Task):
    """
    EXTRACT Step: Runs the Scrapy spider and saves the raw output.
    """
    run_time = luigi.DateMinuteParameter(default=datetime.now())

    def run(self):
        # Create the output directory if it doesn't exist
        os.makedirs(os.path.dirname(self.output().path), exist_ok=True)
        
        # We build a relative path because we run the command from inside the Scrapy project
        relative_output_path = os.path.join('..', 'raw_data', self.output().path.split('/')[-1])
        
        command = ["scrapy", "crawl", SPIDER_NAME, "-o", relative_output_path]

        # Use a subprocess to run the Scrapy command
        subprocess.run(
            command,
            cwd=SCRAPY_PROJECT_PATH, # IMPORTANT: Run from the Scrapy project directory
            check=True
        )

    def output(self):
        """
        The output is a unique file for each run, stamped with the date and minute.
        This allows us to re-run the pipeline to get new data.
        """
        output_filename = f"news_{self.run_time.strftime('%Y-%m-%dT%H-%M')}.jl"
        return luigi.LocalTarget(os.path.join(RAW_DATA_DIR, output_filename))
```


### Step 2: The Transform & Load Task
This task takes the raw file from the previous step and loads it into our final database.

Fill in the file `transform_load/tasks.py` with this skeleton code. Your task is to complete the `TODO` sections.

```python
import luigi
import pandas as pd
import sqlite3
import os
from datetime import datetime
from config import DATABASE_FILE, TRANSFORM_LOAD_DIR
from extract.tasks import ExtractNews

class LoadNewsToDB(luigi.Task):
    """
    LOAD Step: Reads the raw file and loads it into the SQLite database.
    """
    run_time = luigi.DateMinuteParameter(default=datetime.now())

    def requires(self):
        # This task depends on the ExtractNews task from the same run.
        return ExtractNews(run_time=self.run_time)

    def run(self):
        # TODO: Read the raw data from the input file into a pandas DataFrame.
        # HINT: The input file is JSON Lines format. Use pd.read_json(..., lines=True)
        # HINT: The path to the input file is self.input().path
        df = pd.read_json(self.input().path, lines=True)

        # Connect to the database
        conn = sqlite3.connect(DATABASE_FILE)
        
        # Create the 'articles' table if it doesn't already exist.
        # The UNIQUE constraint on 'link' will prevent us from adding duplicate articles.
        conn.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                title TEXT,
                link TEXT UNIQUE,
                pub_date TEXT,
                source TEXT
            )
        ''')
        
        # TODO: Load the DataFrame into the 'articles' table in the database.
        # HINT: Use df.to_sql(...)
        # HINT: Use if_exists='append' to add new data without deleting old data.
        # HINT: Use index=False so pandas doesn't add an extra index column.
        try:
            df.to_sql('articles', conn, if_exists='append', index=False)
        except sqlite3.IntegrityError:
            print("Duplicates found and ignored.") # This is expected!
            
        conn.close()

        # Create a unique marker file to signal that this run is complete.
        with self.output().open('w') as f:
            f.write(f"Data loaded at {datetime.now()}")

    def output(self):
        # The output is a unique marker file for this specific run.
        output_filename = f"db_load_{self.run_time.strftime('%Y-%m-%dT%H-%M')}.SUCCESS"
        return luigi.LocalTarget(os.path.join(TRANSFORM_LOAD_DIR, output_filename))
```

### Step 3: The Analyze Task
This final task reads the clean data from the database and creates a summary file.

Fill in the file `analyse/tasks.py` with this code and complete the TODOs.

```python
import luigi
import pandas as pd
import sqlite3
import os
from datetime import datetime
from config import DATABASE_FILE, ANALYSIS_FILE, ANALYSE_DIR
from transform_load.tasks import LoadNewsToDB

class AnalyzeData(luigi.Task):
    run_time = luigi.DateMinuteParameter(default=datetime.now())

    def requires(self):
        # Depends on the successful loading of data into the database.
        return LoadNewsToDB(run_time=self.run_time)

    def run(self):
        # The main analysis file is overwritten each time with the latest analysis.
        conn = sqlite3.connect(DATABASE_FILE)
        df = pd.read_sql_query("SELECT * FROM articles", conn)
        conn.close()

        # TODO: 1. Analysis: Count the number of articles per news source.
        # TODO: 2 Store as csv: Save them in the csv file ANALYSIS_FILE
        # HINT: We want two columns 'source' and 'article_count'

        # Create its own unique marker file to signal completion.
        with self.output().open('w') as f:
            f.write(f"Analysis created at {datetime.now()}")

    def output(self):
        output_filename = f"analysis_{self.run_time.strftime('%Y-%m-%dT%H-%M')}.SUCCESS"
        return luigi.LocalTarget(os.path.join(ANALYSE_DIR, output_filename))
```

### Step 4: The Main Pipeline

Finally, we wire everything together in `main.py`.
Fill in the file `main.py` with this code.

```python
import luigi
from analyse.tasks import AnalyzeData
from datetime import datetime

class NewsScrapingPipeline(luigi.WrapperTask):
    """
    This is the main pipeline orchestrator.
    It triggers the full E-T-L chain of tasks.
    """
    run_time = luigi.DateMinuteParameter(default=datetime.now())

    def requires(self):
        # By requiring the final task, Luigi builds the entire dependency graph.
        return AnalyzeData(run_time=self.run_time)

if __name__ == '__main__':
    luigi.run()
```

Let us continue with [the next part](./tutorial-part04.md).
