"""Module to manage all db connection functionality"""

import psycopg2
from psycopg2 import sql, pool


def compose_query(query, table):
    """uses the psycopg2.sql module to safely create SQL statements"""
    return sql.SQL(query).format(sql.Identifier(table))


def create_news_table():
    """returns statements to check if 'bill' table exists and, if not, creates it"""
    statement = (
        "CREATE TABLE IF NOT EXISTS {}"
        "("
        "title text not null,"
        "url text not null,"
        "cap_code text,"
        "article_id text primary key,"
        "source text,"
        "pub_date timestamp with time zone,"
        "description text"
        ");"
    )
    table = "news"
    return statement, table


def create_bill_table():
    """returns statements to check if 'news' table exists and, if not, creates it"""
    statement = (
        "CREATE TABLE IF NOT EXISTS {}"
        "("
        "title text not null,"
        "url text not null,"
        "cap_code text,"
        "number integer primary key,"
        "committees text[],"
        "policy_area text,"
        "bill_type text,"
        "congress integer"
        ");"
    )
    table = "bill"
    return statement, table


class PostGreManager:
    """
    Manages all db connection functionality
    """

    def __init__(self, config):
        self.config = config
        self.connection_pool = None

    def connect(self):
        """connect to postgres using configuration saved elsewhere"""
        try:
            self.connection_pool = pool.SimpleConnectionPool(
                1,
                20,
                host=self.config["HOST"],
                database=self.config["DBNAME"],
                user=self.config["USER"],
                password=self.config["PASSWORD"],
            )
            return True
        except psycopg2.Error as error:
            print("Error while connecting to PostGreSQL", error)
            return False

    def exec_query(self, query: str, table, parameters=None):
        """executes statement. If statement is a query, then returns results."""
        connection = None
        cursor = None
        try:
            connection = self.connection_pool.getconn()
            cursor = connection.cursor()
            formatted_query = compose_query(query, table)
            cursor.execute(formatted_query, parameters)
            connection.commit()
            if query.upper().startswith("SELECT"):
                result = cursor.fetchall()  # result of select statement
                return result

            connection.commit()
            return True
        except psycopg2.Error as error:
            print("Error executing query", error)
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                self.connection_pool.putconn(connection)

    def close(self):
        """closes any outstanding connections"""
        if self.connection_pool:
            self.connection_pool.closeall()
