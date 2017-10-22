from MySQLdb.cursors import Cursor

from api.models import Flight

class Flights:
    def __init__(self, cursor: Cursor):
        self.cursor = cursor

    def __map_flight(self, data):
        id = data[0]
        pilot_id = data[1]
        air_id = data[2]
        dep_airp_id = data[3]
        arr_airp_id = data[4]
        dep_time = data[5]
        arr_time = data[6]
        flight = Flight(id, pilot_id, air_id, dep_airp_id, arr_airp_id, dep_time, arr_time)

        return flight

    def add(self, flight: Flight):
        query = """
        INSERT INTO flights (PilotId, AirplaneId, DepartureAirportId, ArrivalAirportId, DepartureTime, ArrivalTime)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (flight.pilot_id, flight.airplane_id, 
        flight.departure_airport_id, flight.arrival_airport_id, 
        flight.departure_time, flight.arrival_time)

        self.cursor.execute(query, params)

    def all(self):
        query = """
        SELECT Id, PilotId, AirplaneId, DepartureAirportId, ArrivalAirportId, DepartureTime, ArrivalTime FROM flights
        """
        self.cursor.execute(query)

        flights = self.cursor.fetchall()
        mapped = map(self.__map_flight, flights)

        return list(mapped)

    def update(self, id, flight: Flight):
        query = """
        UPDATE flights SET PilotId=%s, AirplaneId=%s, DepartureAirportId=%s, ArrivalAirportId=%s, DepartureTime=%s, ArrivalTime=%s
        WHERE flights.Id = %s
        """
        params = (flight.pilot_id, flight.airplane_id, flight.departure_airport_id, flight.arrival_airport_id, flight.departure_time, flight.arrival_time, id)
        self.cursor.execute(query, params)