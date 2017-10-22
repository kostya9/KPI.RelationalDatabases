from MySQLdb.cursors import Cursor

from api.models import Airplane

import time

class Airplanes:
    def __init__(self, cursor : Cursor):
        self.cursor = cursor
    
    def __map_airplane(self, data):
        return Airplane(data[0], data[1], data[2])

    def all(self):
        self.cursor.execute("""
        SELECT Id, ModelName, BuildDate FROM Airplanes;
        """)
        airplanes = self.cursor.fetchall()

        mapped = map(self.__map_airplane, airplanes)
        return list(mapped)

    def remove(self, id):
        query = "DELETE FROM Airplanes WHERE Id=%s"
        self.cursor.execute(query, (id))

    def search(self, model_name, start_date, end_date):
        query = """
        SELECT Id, ModelName, BuildDate FROM Airplanes
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

        