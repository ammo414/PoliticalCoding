import psycopg2 


"""
Manages all db connection functionality
"""

class PostGreManager:
    def __init__(self, config):
        self.config = config
        self.connection_pool = None

    def connect(self):
        try:
            self.connection_pool = pool.SimpleConnectionPool(
                1, 20, 
                host = self.config['HOST'],
                database = self.config['DATABASE'],
                user = self.config['USER'],
                password = self.config['PASSWORD']
            )
            return True
        except (Exception, psycopg2.Error) as error:
            print('Error while connecting to PostGreSQL', error)
            return False

    def execute_query(self, query: str, table, parameters):
        connection = None
        cursor = None
        try: 
            connection = self.connection_pool.getconn()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            if query.upper().startswith('SELECT'):
                result = cursor.fetchall() # result of select statement
                return result
            else:
                connection.commit()
                return True
        except (Exception, psycopg2.Error) as error:
            print('Error executing query', error)
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                self.connection_pool.putconn(connection)


    def close(self):
        if self.connection_pool:
            self.connection_pool.closeall()
