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

