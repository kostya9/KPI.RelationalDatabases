from MySQLdb.cursors import Cursor

from api.models import Airport

class Airports:
    def __init__(self, cursor: Cursor):
        self.cursor = cursor
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')

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

    def add(self, airport: Airport):
        query = """
            INSERT INTO airports (Name, Code, City) VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (airport.name, airport.code, airport.city))

    def search(self, name, code, city):
        query = """
        SELECT Id, Name, Code, City FROM airports
        WHERE Code LIKE %s AND City LIKE %s
        """

        params = (code + '%', city + '%')
        if name is not None and name is not "":
            query += """ AND MATCH (Name)
        AGAINST (%s IN BOOLEAN MODE)
            """
            params += ('-' + name,)
        self.cursor.execute(query, params)

        return self.__get_result()
    
    def remove(self, id: int):
        query = """
        DELETE FROM airports WHERE Id=%s
        """
        self.cursor.execute(query, [id])

    def import_all(self, airports):
        query = """
        DELETE FROM airports
        """
        self.cursor.execute(query)
        for airport in airports:
            self.add(airport)

        
