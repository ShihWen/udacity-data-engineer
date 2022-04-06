import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries



def drop_tables(cur, conn):
    """
    Drop tables if they are already exists in the database.

    :param cur: curser of the database
    :param conn: connection to the database
    :returns: none

    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Create staging tables, fact table and dimension tables at once. 

    :param cur: curser of the database
    :param conn: connection to the database
    :returns: none

    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Get variables from config file, connect to the database, 
    create cursor and execute drop_tables() and create_tables().

    :returns: none

    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()