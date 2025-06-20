

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

