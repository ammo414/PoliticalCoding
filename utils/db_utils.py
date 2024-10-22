"""Module to manage all db connection functionality"""
import psycopg2
from psycopg2 import sql, pool


def compose_query(query, table):
    """uses the psycopg2.sql module to safely create SQL statements""" 
    return sql.SQL(query).format(sql.Identifier(table))


def create_bill_table():
    """returns statements to check if 'bill' table exists and, if not, creates it"""
    statement = 'CREATE TABLE {} IF NOT EXIST \
                (title text NOT NULL, url text NOT NULL, cap_code text, article_id text PRIMARY,\
                     source text, pub_date timestamp with time zone, description text)'
    table = 'bill'
    return statement, table


def create_news_table():
    """returns statements to check if 'news' table exists and, if not, creates it"""
    statement = 'CREATE TABLE {} IF NOT EXIST \
                (title text NOT NULL, url text NOT NULL, cap_code text, number integer PRIMARY,\
                    committees text[], policy_area text, bill_type text, congress integer)'
    table = 'news'
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
                host = self.config['HOST'],
                database = self.config['DBNAME'],
                user = self.config['USER'],
                password = self.config['PASSWORD']
            )
            return True
        except psycopg2.Error as error:
            print('Error while connecting to PostGreSQL', error)
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
            if query.upper().startswith('SELECT'):
                result = cursor.fetchall() # result of select statement
                return result

            connection.commit()
            return True
        except psycopg2.Error as error:
            print('Error executing query', error)
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                self.connection_pool.putconn(connection)

    def create_table_if_not_exist(self, which_type):
        """creates table if they don't already exist"""
        if which_type == 'news':
            self.exec_query('CREATE TABLE {} IF NOT EXIST \
                (title text NOT NULL, url text NOT NULL, cap_code text, article_id text PRIMARY,\
                     source text, pub_date timestamp with time zone, description text)',
                    'news')
        elif which_type == 'bill':
            self.exec_query('CREATE TABLE {} IF NOT EXIST \
                (title text NOT NULL, url text NOT NULL, cap_code text, number integer PRIMARY,\
                    committees text[], policy_area text, bill_type text, congress integer)',
                    'bill')
        else:
            print('Wrong type. Please check')


    def close(self):
        """closes any outstanding connections"""
        if self.connection_pool:
            self.connection_pool.closeall()
