from MySQLdb.connections import Connection
from MySQLdb.cursors import Cursor
from api.models import Pilot

class Pilots:
    def __init__(self, cursor : Cursor):
        self.cursor = cursor

    def __map_pilot(self, data):
        return Pilot(data[0], data[1], data[2], data[3])

    def all(self):
        self.cursor.execute("""
        SELECT Id, FirstName, LastName, StartingDate FROM pilots;
        """)
        pilots = self.cursor.fetchall()

        mapped = map(self.__map_pilot, pilots)
        return list(mapped)

    def add(self, pilot: Pilot):
        add_pilot = """
        INSERT INTO pilots (FirstName, LastName, StartingDate) VALUES
(%s, %s, %s)
        """
        data_pilot = (pilot.firstname, pilot.lastname, pilot.starting_date)
        self.cursor.execute(add_pilot, data_pilot)

    def search(self, firstname, lastname):
        query = "SELECT Id, FirstName, LastName, StartingDate FROM pilots WHERE FirstName LIKE %s AND LastName LIKE %s"
        data_search = (firstname + '%', lastname + '%')
        self.cursor.execute(query, data_search)
        pilots = self.cursor.fetchall()

        mapped = map(self.__map_pilot, pilots)
        return list(mapped)

    def remove(self, id):
        query = "DELETE FROM pilots WHERE Id=%s"
        self.cursor.execute(query, (id))
