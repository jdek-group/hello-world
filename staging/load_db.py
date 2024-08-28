import pandas as pd
import sqlalchemy as db

engine = db.create_engine('postgresql://postgres:admin@localhost:5432/moviedb-test2')
conn = engine.raw_connection()

def load_to_db(file_uri: str) -> None:
    df = pd.read_csv(file_uri)
    table_name = file_uri.replace('.csv', '')
    df.to_sql(name= table_name, con=engine, if_exists="replace", chunksize=50000, method="multi")
    print(table_name + str(df.shape) + ': df loaded to db')