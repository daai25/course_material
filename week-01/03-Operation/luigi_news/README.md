# **Tutorial: Building an Automated News Scraper & Dashboard**

Welcome! In this tutorial, you will build a complete, real-world data pipeline from scratch. You will learn how to automatically extract data from the web, process it, store it in a database, and display it on a live dashboard.

## **Project Goal**

Our goal is to build a pipeline that:

1. **Extracts** the latest technology news headlines from a live RSS feed.  
2. **Loads** this data into a persistent database, avoiding duplicate entries.  
3. **Analyzes** the data to see which news sources are most active.  
4. **Visualizes** the results on a simple web dashboard.  
5. Is **automated and re-runnable**, allowing us to schedule it to fetch new data continuously.

## **Core Concepts**

* **ETL Pipeline:** This stands for **Extract, Transform, Load**. It's a standard pattern in data engineering.  
  * **Extract:** Get raw data from a source (in our case, a website).  
  * **Transform/Load:** Clean the data and load it into a structured storage system (our database). In our case, we combine these steps.  
  * **Analyze:** A final step where we use the clean data to generate insights.  
* **Scrapy:** A powerful Python framework for web crawling and scraping. We will use it for our **Extract** step.  
* **Luigi:** A Python package from Spotify for building complex data pipelines. It helps manage dependencies between tasks and makes our pipeline robust. We will use it to orchestrate the entire ETL process.  
* **Dash:** A Python framework for building interactive web-based dashboards. We will use this for our **Visualize** step.

## Part 1: Project Setup
The project contains the following folders and **empty** `__init__.py` files.
We separated our project into different functional parts (extract, transform_load, analyse and visualize).
The empty __init__.py files tell Python to treat the directories (extract/, transform_load/, etc.) as "packages".
These empty files are the essential "glue" that allows our different parts
(main.py, extract/tasks.py, analyse/tasks.py, etc.) to be aware of each other
and share code, making our organized, multi-folder structure possible.

```text
├── main.py
├── config.py
├── requirements.txt
|
├── extract/
│   └── __init__.py
│
├── transform_load/
│   ├── __init__.py
│   └── tasks.py
│
├── analyse/
│   ├── __init__.py
│   └── tasks.py
│
└── visualize/
    ├── __init__.py
    └── app.py
```

### Step 1: Install Dependencies
We use following `requirements.txt`:

```bash
luigi
scrapy
pandas
dash
```

Install them by running this command in your terminal:

```bash
pip install -r requirements.txt
```

### Step 2: Create the Configuration File
The `config.py` file will hold all our important file paths and settings, making them easy to change later.

```python
import os

# --- Core Directories ---
EXTRACT_DIR = 'extract'
TRANSFORM_LOAD_DIR = 'transform_load'
ANALYSE_DIR = 'analyse'
VISUALIZE_DIR = 'visualize'

# --- Scrapy Project Configuration ---
SCRAPY_PROJECT_NAME = 'news_scraper' 
SCRAPY_PROJECT_PATH = os.path.join(EXTRACT_DIR, SCRAPY_PROJECT_NAME)
SPIDER_NAME = 'news_spider' 

# --- File Paths ---
RAW_DATA_DIR = os.path.join(EXTRACT_DIR, 'raw_data') 
DATABASE_FILE = os.path.join(TRANSFORM_LOAD_DIR, 'news_data.db')
ANALYSIS_FILE = os.path.join(ANALYSE_DIR, 'source_analysis.csv')

# --- Dash App Configuration ---
DASH_PORT = 8050
DASH_HOST = '127.0.0.1'
```

## Part 2: The Scraper (Extract)
In this part, you will create a Scrapy project that extracts news from the Google News RSS feed.

### Step 1: Create the Scrapy Project
Navigate into your `extract` directory in the terminal and run the command to create a new Scrapy project.

```bash
cd extract
scrapy startproject news_scraper
```

This command creates a `news_scraper` folder with all the necessary files for a Scrapy project.

### Step 2: Create the News Spider

Now, inside your new project, create the spider. This is the bot that will visit the website and extract the data.

Create the file `extract/news_scraper/news_scraper/spiders/news_spider.py` and add the following code:

```python
import scrapy

class NewsSpider(scrapy.Spider):
    # The name we use to call this spider
    name = 'news_spider'
    
    # The URL of the Google News RSS feed for Technology
    start_urls = ['https://news.google.com/rss/search?q=technology']

    def parse(self, response):
        # RSS feeds are XML. remove_namespaces() helps with parsing.
        response.selector.remove_namespaces()
        
        # We loop through each <item> tag in the XML, which represents one news article.
        for item in response.xpath('//item'):
            # yield is like 'return', but for generators. It sends one item at a time.
            yield {
                'title': item.xpath('title/text()').get(),
                'link': item.xpath('link/text()').get(),
                'pub_date': item.xpath('pubDate/text()').get(),
                'source': item.xpath('source/text()').get(),
            }
```


### Step 3: Test Your Spider
From inside the `extract/news_scraper` directory, run your spider and save the output to a test file.

```bash
cd extract/news_scraper
scrapy crawl news_spider -o test_output.json
```

If it works, you will see a `test_output.json` file full of news articles! You have successfully built your extractor


## Part 3: The Luigi Pipeline (Orchestration)
Now we will build the Luigi tasks that will automate our ETL process.

### Step 1: The Extract Task
This first task will be responsible for running the Scrapy spider we just built.

Fill in the file `extract/tasks.py` with this code.

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

## Part 4: Running Your Pipeline!
You are now ready to run your entire pipeline.

### Step 1: Run the Luigi Pipeline
Open your terminal in the project's root directory and run:

```bash
luigi --module main NewsScrapingPipeline --local-scheduler
```
You will see Luigi check the dependencies and run the Extract, Load, and Analyze tasks in order.

### Step 2: Re-run the Pipeline
Run the same command again a few minutes later. You will see it run again! This is because the DateMinuteParameter creates a new, unique target each time, allowing you to fetch fresh data.

Congratulations! You have successfully built and run a complete, automated data pipeline.

## Part 5: The Dashboard (Visualize)
Now we'll create a standalone web app to view our results.
Fill in the file `visualize/app.py` with this code.

```python
import dash
from dash import dcc, html, dash_table
import pandas as pd
import os
import sqlite3
import sys

# This allows us to import the config.py file from the parent directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from config import DATABASE_FILE, ANALYSIS_FILE, DASH_HOST, DASH_PORT

# --- Load Data ---
# Load data only if the files have been created by the pipeline
if os.path.exists(DATABASE_FILE):
    conn = sqlite3.connect(DATABASE_FILE)
    df_articles = pd.read_sql_query("SELECT title, source, pub_date FROM articles ORDER BY pub_date DESC LIMIT 100", conn)
    conn.close()
else:
    df_articles = pd.DataFrame(columns=['title', 'source', 'pub_date'])

if os.path.exists(ANALYSIS_FILE):
    df_analysis = pd.read_csv(ANALYSIS_FILE)
else:
    df_analysis = pd.DataFrame(columns=['source', 'article_count'])

# --- Create Dash App ---
app = dash.Dash(__name__)

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
    html.H1("News Analysis Dashboard"),
    html.H2("Article Count by Source"),
    dcc.Graph(
        figure={
            'data': [{'x': df_analysis['source'], 'y': df_analysis['article_count'], 'type': 'bar'}],
            'layout': {'title': 'Article Count by News Source'}
        }
    ),
    html.H2("Latest News Headlines"),
    dash_table.DataTable(data=df_articles.to_dict('records'), page_size=10)
])

# --- Main entry point to run the app ---
if __name__ == '__main__':
    app.run(host=DASH_HOST, port=DASH_PORT, debug=True)
```


Step 1: Start the Dashboard
In a new terminal window, run the visualization app:

```bash
python visualize/app.py
```

Open your web browser to `http://127.0.0.1:8050` and you will see your dashboard, populated with the data you just scraped. If you re-run the pipeline, you can refresh the dashboard page to see the updated data.

