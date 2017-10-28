from MySQLdb.cursors import Cursor

from api.models import Airport

class Airports:
    def __init__(self, cursor: Cursor):
        self.cursor = cursor

    def __map_airport(self, data):
        return Airport(data[0], data[1], data[2], data[3])

    def __get_result(self):
        airports = self.cursor.fetchall()
        mapped = map(self.__map_airport, airports)
        return list(mapped)

    def all(self):
        self.cursor.execute("""
        SELECT Id, Name, Code, City FROM airports;
        """)

        return self.__get_result()

    def search(self, name, code, city):
        query = """
        SELECT Id, Name, Code, City FROM airports
        WHERE Name LIKE %s AND Code LIKE %s AND City LIKE %s
        """
        params = (name + '%', code + '%', city + '%')
        self.cursor.execute(query, params)

        return self.__get_result()
    
    def remove(self, id):
        query = """
        DELETE FROM airports WHERE Id=%s
        """
        self.cursor.execute(query, (id))
        
