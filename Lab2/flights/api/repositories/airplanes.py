from MySQLdb.cursors import Cursor

from api.models import Airplane

import time

class Airplanes:
    def __init__(self, cursor : Cursor):
        self.cursor = cursor
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
    
    def __map_airplane(self, data):
        return Airplane(data[0], data[1], data[2])

    def add(self, airplane: Airplane):
        query = """
        INSERT INTO airplanes (ModelName, BuildDate) VALUES (%s, %s)
        """
        self.cursor.execute(query, (airplane.modelname, airplane.builddate))

    def import_all(self, airplanes):
        query = """
        DELETE FROM airplanes 
        """
        self.cursor.execute(query)
        for airplane in airplanes:
            self.add(airplane)

    def all(self):
        self.cursor.execute("""
        SELECT Id, ModelName, BuildDate FROM airplanes;
        """)
        airplanes = self.cursor.fetchall()

        mapped = map(self.__map_airplane, airplanes)
        return list(mapped)

    def remove(self, id):
        query = "DELETE FROM airplanes WHERE Id=%s"
        self.cursor.execute(query, [id])

    def search(self, model_name, start_date, end_date):
        query = """
        SELECT Id, ModelName, BuildDate FROM airplanes
        WHERE ModelName LIKE %s AND (BuildDate > %s AND BuildDate < %s) 
        """
        
        if start_date is None:
            start_date = '1900-01-01'

        if end_date is None:
            end_date = time.strftime("%Y-%m-%d")

        self.cursor.execute(query, (model_name + '%', start_date, end_date))
        airplanes = self.cursor.fetchall()
        
        mapped = map(self.__map_airplane, airplanes)
        return list(mapped)

        
