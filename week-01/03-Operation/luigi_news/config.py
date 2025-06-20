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
RAW_DATA_DIR   = os.path.join(EXTRACT_DIR, 'raw_data')
DATABASE_FILE  = os.path.join(TRANSFORM_LOAD_DIR, 'news_data.db')
ANALYSIS_FILE  = os.path.join(ANALYSE_DIR, 'source_analysis.csv')

# --- Dash App Configuration ---
DASH_PORT = 8050
DASH_HOST = '127.0.0.1'
