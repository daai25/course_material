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

Install them by running this command in your terminal (best in a virtual environment):

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

Let us continue with [the next part](./tutorial-part02.md).
