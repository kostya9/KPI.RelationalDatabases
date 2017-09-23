from MySQLdb.connections import Connection
from MySQLdb.cursors import Cursor
from api.models import Pilot
class Pilots:
    def __init__(self, cursor : Cursor):
        self.cursor = cursor

    def all(self):
        self.cursor.execute("""
        SELECT Id, FirstName, LastName, StartingDate FROM Pilots;
        """)
        pilots = self.cursor.fetchall()

        mapped = map(lambda pilot: Pilot(pilot[0], pilot[1], pilot[2], pilot[3]), pilots)
        return list(mapped)

    def add(self, pilot: Pilot):
        add_pilot = """
        INSERT INTO PILOTS  (FirstName, LastName, StartingDate) VALUES
(%s, %s, %s)
        """
        data_pilot = (pilot.firstname, pilot.lastname, pilot.starting_date)
        self.cursor.execute(add_pilot, data_pilot)