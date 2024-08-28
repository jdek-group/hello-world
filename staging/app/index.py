from flask import Flask, render_template, render_template_string
import psycopg2
import plotly.express as px
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.environ['DBNAME'],
        user=os.environ['DBUSER'],
        password=os.environ['DBPASS'],
        host=os.environ['DBHOST'],
        port=os.environ['DBPORT']
    )
    return conn

@app.route('/')
def index():

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM GenreName_Rating;')
    results = cur.fetchall()
    cur.close()
    conn.close()
    # return str(results)
    
    df = pd.DataFrame(results)
    df.columns = df.iloc[0]  # Set the first row as the header
    df = df[1:]              # Remove the first row from the DataFrame

    # Rename the columns for clarity
    df.columns = ['Genre', 'Average Rating']
    
    # print(df.columns)
    fig = px.bar(df, x='Genre', y='Average Rating', title='Average Movie Rating by Genre')
    
    # Adjust the title position
    fig.update_layout(
        title={
            'text': "Average Movie Rating by Genre",
            'y':0.9,  # vertical position: 0.0 (bottom) to 1.0 (top)
            'x':0.5,  # horizontal position: 0.0 (left) to 1.0 (right)
            'xanchor': 'center',  # alignment relative to the x position
            'yanchor': 'top'      # alignment relative to the y position
        }
    )
    plot_html = fig.to_html(full_html=False)
    
    # str = fig.show()
    # print(str)
    # Convert the DataFrame to HTML
    # df_html = df.to_html()
    # <h1>DataFrame</h1>
    #     {df_html}
    combined_html = f'''
    <html>
    <head><title>Flask Plot Viz</title></head>
    <body>
        {plot_html}
    </body>
    </html>
    '''

    return render_template_string(combined_html)
    # Render the HTML template and pass the DataFrame HTML
    # return render_template('index.html', tables=[df_html], titles=df.columns.values)

if __name__ == '__main__':
    app.run(debug=True)
