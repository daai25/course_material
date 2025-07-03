# pipeline.py
# A complete Luigi pipeline for fetching, cleaning, and training a model.
# To run: luigi --module pipeline TrainModelTask --local-scheduler

import luigi
import pandas as pd
import pickle
from pathlib import Path

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# =============================================================================
# Task 1: Fetch the raw data
# =============================================================================
class FetchDataTask(luigi.Task):
    """
    Downloads the Iris dataset and saves it as a raw CSV file.
    This task has no dependencies.
    """
    def output(self):
        """
        Defines the output file for this task.
        Luigi checks for this file's existence to see if the task is complete.
        """
        return luigi.LocalTarget('data/raw_data.csv')

    def run(self):
        """
        The main logic of the task. This runs only if the output file doesn't exist.
        """
        # Load dataset from scikit-learn
        iris = load_iris(as_frame=True)
        df = iris.frame
        
        # Ensure the output directory exists before writing the file
        output_path = Path(self.output().path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the raw data
        df.to_csv(output_path, index=False)

# =============================================================================
# Task 2: Clean the raw data
# =============================================================================
class CleanDataTask(luigi.Task):
    """
    Cleans the raw data by renaming columns.
    This task depends on FetchDataTask.
    """
    def requires(self):
        """
        Specifies the dependency for this task.
        Luigi will ensure FetchDataTask is complete before running this one.
        """
        return FetchDataTask()

    def output(self):
        """
        Defines the output file for the cleaned data.
        """
        return luigi.LocalTarget('data/cleaned_data.csv')

    def run(self):
        """
        Loads the raw data, cleans it, and saves the result.
        """
        # self.input() refers to the output of the required task (FetchDataTask)
        input_path = self.input().path
        df = pd.read_csv(input_path)

        # A simple "cleaning" step: format column names
        df.columns = [col.replace(' (cm)', '').replace(' ', '_') for col in df.columns]
        
        # Save the cleaned data
        output_path = Path(self.output().path)
        # The parent directory should already exist from the previous task,
        # but this is good practice for robustness.
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)

# =============================================================================
# Task 3: Train a model on the cleaned data
# =============================================================================
class TrainModelTask(luigi.Task):
    """
    Trains a simple logistic regression model on the cleaned data.
    This is the final task in our pipeline.
    """
    def requires(self):
        """
        This task depends on the cleaned data being available.
        """
        return CleanDataTask()

    def output(self):
        """
        The final output is the serialized model file.
        """
        return luigi.LocalTarget('models/model.pkl')

    def run(self):
        """
        Loads the cleaned data, trains a model, and saves it using pickle.
        """
        # Load the cleaned data from the previous task's output
        input_path = self.input().path
        df = pd.read_csv(input_path)

        # Prepare data for scikit-learn
        X = df.drop('target', axis=1)
        y = df['target']
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a simple model
        model = LogisticRegression(max_iter=200)
        model.fit(X_train, y_train)

        # Ensure the output directory exists
        output_path = Path(self.output().path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the trained model using pickle
        with output_path.open('wb') as f:
            pickle.dump(model, f)

# This block allows running the final task directly for testing,
# though the standard way is via the luigi command line.
if __name__ == '__main__':
    luigi.run(['TrainModelTask', '--local-scheduler'])

