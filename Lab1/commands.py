import itertools
from Model.city import City
from Model.country import Country
from Data.datarepository import DataRepository

class Commands():
    """
    Is responsible for running commands with input and ouput.
    See 'help' command for extra details. Note that spaces in help commands should be
    changed to underscores. The argument in the {} parenthesese should be given
    in the 'arg' parameter
    """
    def __init__(self, data: DataRepository):
        self.__data = data
        self.__city_key = 'city'
        self.__country_key = 'country'
        self.__data.make_foreign_key(self.__city_key, 'country_id', self.__country_key)
        self.__save_file_name = 'data.p'
        self.__help_message = " \
        You can use following commands \n\
            help - to view this message \n\
            list cities - to get the list of all cities in the app \n\
            list countries - to get the list of all countries in the app \n\
            list largecountries - lists all countries that have more than 3 towns with population > 1 million \n\
            add city - to add a new city \n\
            add country - to add an ew country \n\
            edit city {id} - to edit the city with id {id} \n\
            edit country {id} - to edit the country with id {id} \n\
            remove country {id} - to remove the country with id {id} \n\
            remove country {id} - to remove the country with id {id} \n\
            save \n\
            load \n\
            exit \
        "
        self.__error_message = 'This command does not exist. Try help'

        self.__commands = self.__create_commands()

    def __create_commands(self):
        commands = {
            'help': lambda: print(self.__help_message),
            'list_countries': self.__print_countries,
            'list_cities': self.__print_cities,
            'list_largecountries': self.__print_large_countries,
            'add_city': self.__add_city,
            'add_country': self.__add_country,
            'edit_country': self.__edit_country,
            'edit_city': self.__edit_city,
            'remove_country': lambda id: self.__remove_entity(self.__country_key, id),
            'remove_city': lambda id: self.__remove_entity(self.__city_key, id),
            'save': lambda: self.__data.serialize(self.__save_file_name),
            'load': self.__deserialize,
            'exit': lambda: None
        }
        return commands

    def __error(self, message):
        print('ERROR: %s' % message)

    def run(self, command_name: str, arg=None):
        """
        Runs the command.
        Args:
            command_name (str): the name for the command to be run.
            arg (any): the argument for the command. None if the command has no arguments.
        """
        try:
            if arg is None:
                self.__commands[command_name]()
            else:
                self.__commands[command_name](arg)
        except (KeyError, TypeError):
            self.__error(self.__error_message)

    def __print_countries_collection(self, data):
        print('Id, Name')
        if not data:
            print('...There is nothing here...')
        for country in data:
            print("%i\t%s" % (country.id, country.name))

    def __print_countries(self):
        countries = self.__data.get_all(self.__country_key)
        self.__print_countries_collection(countries)

    def __print_cities(self):
        cities = self.__data.get_all(self.__city_key)
        print('Id, Country, Name, Population')
        if not cities:
            print('...There is nothing here...')
        for city in cities:
            country_name = self.__data.get(self.__country_key, city.country_id).name
            print("%i\t%s\t%s\t%i" % (city.id, country_name, city.name, city.population))

    def __validate_parse_positive_int(self, string):
        try:
            value = int(string)
        except ValueError:
            self.__error('The value is not integer')
            return None
        if value < 0:
            self.__error('The value is negative')
            return None
        return value

    def __validate_parse_id(self, data_key, string):
        data_id = self.__validate_parse_positive_int(string)
        if data_id is None:
            return

        if not self.__data.exists(data_key, data_id):
            self.__error('The object does not exist')
            return None

        return data_id

    def __add_country(self):
        print('Please, enter the country name:')
        name = input()
        country = Country(0, name)
        self.__data.add(self.__country_key, country)
        print('Added with id %i' % country.id)

    def __add_city(self):
        print('Please, enter the country id:')
        country_id = self.__validate_parse_id(self.__country_key, input())
        if country_id is None:
            return

        print('Please, enter the city name:')
        name = input()

        print('Please, enter the population')
        population = self.__validate_parse_positive_int(input())
        if population is None:
            return

        city = City(0, country_id, name, population)
        self.__data.add(self.__city_key, city)
        print('Added with id %i' % city.id)

    def __deserialize(self):
        try:
            self.__data.deserialize(self.__save_file_name)
        except ValueError:
            self.__error('The save file \'data.p\' does not exist')

    def __remove_entity(self, key, data_id):
        data_id = self.__validate_parse_positive_int(data_id)
        if data_id is None:
            return
        if not self.__data.exists(key, data_id):
            self.__error('The object does not exist')
            return
        if self.__data.is_key_for_foreignkey(key):
            print('Some objects may depend on this one. Are you sure that you want to delete it?')
            print('Note that all connected entities will be removed too.')
            print('Print \'y\' if you want to delete it anyways')
            if input().lower() not in ['y', 'yes']:
                print('Aborting...')
                return

        self.__data.remove(key, data_id)
        print('The entity is successfully removed')

    def __edit_country(self, country_id):
        country_id = self.__validate_parse_id(self.__country_key, country_id)
        if country_id is None:
            return

        country = self.__data.get(self.__country_key, country_id)
        print('Type in the new name of the country[default=%s]:' % country.name)
        name = input()
        country.name = name or country.name
        print('The country was successfully changed')

    def __edit_city(self, city_id):
        city_id = self.__validate_parse_id(self.__city_key, city_id)
        if city_id is None:
            print('Aborting...')
            return

        city = self.__data.get(self.__city_key, city_id)
        print('Type in the new country id[default=%i]:' % city.country_id)
        country_id = input() or city.country_id
        country_id = self.__validate_parse_id(self.__country_key, country_id)
        if country_id is None:
            print('Aborting...')
            return

        print('Type in the new name of the city[default=%s]:' % city.name)
        name = input() or city.name

        print('Type in the new population[default=%i]:' % city.population)
        population = self.__validate_parse_positive_int(input())
        if population is None:
            print('Aborting...')
            return

        city.country_id = country_id
        city.name = name
        city.population = population
        print('The city was changed successfully')

    def __print_large_countries(self):
        cities = self.__data.get_all(self.__city_key)
        borderline_population = pow(10, 6)

        # Itertools groupby requires sorted grouping key
        sorted_cities = sorted(cities, key=lambda c: c.country_id)


        citied_by_country = itertools.groupby(sorted_cities, lambda c: c.country_id)
        filtered_countries = []
        for country_id, cities in citied_by_country:
            big_cities = sum([1 if c.population > borderline_population else 0 for c in cities])
            if big_cities >= 3:
                filtered_countries.append(self.__data.get(self.__country_key, country_id))
        self.__print_countries_collection(filtered_countries)
        