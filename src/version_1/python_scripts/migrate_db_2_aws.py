import psycopg2
import pandas as pd


def get_table_names(database):
    """
    Returns list of table names from database.

    Args:
        database (string): Database name

    Returns:
        list of strings: Table names
    """
    with psycopg2.connect(
        database=database,
        user="postgres",
        password="password",
        host="localhost",
        port="5432",
    ) as conn:
        query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
                """
        table_names = []
        with conn.cursor() as curs:
            curs.execute(query)
            for row in curs:
                table_names.append(row[0])
            return table_names


def table_to_csv(database, table_name):
    """
    Saves PostgreSQL table to csv file.

    Args:
        database (string): PostgreSQL database name
        table_name (string):
    """
    with psycopg2.connect(
        database=database,
        user="postgres",
        password="password",
        host="localhost",
        port="5432",
    ) as conn:
        file = open(
            f"/home/jeff/Documents/Galvanize_DSI/capstones/C2_Yelp_Review_Quality/data/full_data/yelp_2/{table_name}.csv",
            "w",
        )
        query = "COPY %s TO STDOUT WITH CSV HEADER"
        with conn.cursor() as curs:
            curs.copy_expert(sql=query % table_name, file=file)


if __name__ == "__main__":
    s3_bucket_path = "s3://predicting.yelp.review.quality/yelp_database_csv/checkin_expanded_2.csv"

    df = pd.read_csv(s3_bucket_path)

    print(df.info())
    print(df.head(5))
