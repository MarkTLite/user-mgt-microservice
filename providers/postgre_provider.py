
from db_interface import DatabaseInterface
from configparser import ConfigParser
import psycopg2, os

class PostgresDBProvider(DatabaseInterface):
    def __init__(self):
        self.conn = None
        self.cursor = None

    def read_db_config(self, filename='dbconfig.ini',section='postgresql'):
        parser = ConfigParser()
        path = os.path.dirname(os.path.abspath(__file__))
        parser.read(path + f'\{filename}')
        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        self.params = db
        return db

    def connect(self):
        """ Connect to the PostgreSQL database server """
        self.conn = None
        try:
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**self.params)
            self.cursor = self.conn.cursor()
            print('PostgreSQL database version:')
            self.cursor.execute('SELECT version()')
            db_version = self.cursor.fetchone()
            print(db_version)
            return (True, 'Connection Successful')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return (False, "Error")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print('closed db connection')

        return (True, "Disconnected")

    def create(self, location: str, data: dict):
        """Create an odds entry """        
        try:
            create_command = """CREATE TABLE IF NOT EXISTS odds (
                            id SERIAL PRIMARY KEY,
                            league VARCHAR(50) NOT NULL,
                            home_team VARCHAR(50) NOT NULL,
                            away_team VARCHAR(50) NOT NULL,
                            home_team_win_odds FLOAT NOT NULL, 
                            away_team_win_odds FLOAT NOT NULL,
                            draw_odds FLOAT NOT NULL,
                            game_date VARCHAR(50) NOT NULL,
                            creator VARCHAR(50) NOT NULL
                        )"""
            self.cursor.execute(create_command)            
            self.conn.commit()
            if data: 
               self.insert(data=data)
            else:
                raise Exception()

            # self.cursor.close()
            # self.conn.close()            
            return (True, 'Created')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return (False, "Error")       

    def read(self, location: str, data: dict):
        """Read by given league and date range"""
        try:            
            sql = """SELECT * FROM odds WHERE league = %s AND game_date >= %s AND game_date < %s"""
            if location is None:
                raise Exception()
            self.cursor.execute(sql,data['ids'])
            rows = self.cursor.fetchall()
            data = {'list':[]}
            for row in rows:
                data['list'].append(row)                
            return (True, 'Read Successful', data)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return (False, "Error", {})

    def insert(self, data: dict):
        """ insert multiple rows into the table  """        
        # self.conn = None
        try:
            insert_sql = """INSERT INTO odds (league, home_team, away_team, home_team_win_odds, 
                away_team_win_odds,draw_odds,game_date,creator) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
            if data:
                print(data['data'])
                self.cursor.execute(insert_sql,data['data'])
                self.conn.commit()
                return (True, 'Insert Successful')
            else:
                raise Exception()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return (False, "Error")

    def update(self, location: str, data: dict):
        """ update based on the id"""
        sql = """UPDATE odds
                    SET league = %s, home_team = %s, away_team = %s, home_team_win_odds = %s, 
            away_team_win_odds = %s,draw_odds = %s, game_date = %s
                    WHERE id = %s"""
        try:
            if data is None:
                raise Exception()
            self.cursor.execute(sql, data['data'])
            updated_rows = self.cursor.rowcount
            self.conn.commit()
            return (True, 'Update Successful')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return (False, "Error")

    def delete(self, location: str, data: dict):
        """ delete row by data given"""
        try:
            value = data['data']
            print(value)
            self.cursor.execute("""DELETE FROM odds WHERE league = %s AND home_team = %s AND 
                                away_team = %s AND game_date = %s""", value)
            # rows_deleted = self.cursor.rowcount
            self.conn.commit()
            return (True, 'Delete Successful')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return (False, "Error")
