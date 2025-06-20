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


## [Part 1](doc/tutorial-part01.md)
## [Part 2](doc/tutorial-part02.md)
## [Part 3](doc/tutorial-part03.md)
## [Part 4](doc/tutorial-part04.md)
## [Part 5](doc/tutorial-part05.md)