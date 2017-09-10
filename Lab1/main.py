"""
Entry point for Lab1 with CLI.
"""
import signal, sys

from city import City
from country import Country
from Data.dataholder import DataHolder

# Text commands' content
HELP = " \
    You can use following commands \n\
        help - to view this message \n\
        list cities - to get the list of all cities in the app \n\
        list countries - to get the list of all countries in the app \n\
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
ERROR = 'This command does not exist. Try help'

# Data initialisation
data = DataHolder()
COUNTRY_KEY = 'country'
CITY_KEY = 'city'
SAVE_FILE_NAME = 'data.p'

def __sigint_handler(signum, frame):
    sys.exit(0)


def __main():
    # Windows 10 does not close python proccess after Ctrl-C for some reason
    signal.signal(signal.SIGINT, __sigint_handler)
    commands = __create_commands()
    print(HELP)

    data.make_foreign_key(CITY_KEY, 'country_id', COUNTRY_KEY)
    try:
        __input_loop(commands)
    except (KeyboardInterrupt,  EOFError):
        SystemExit(0)


def __input_loop(commands):
    input_command = ""
    while input_command != 'exit':
        print(">", end=' ')
        input_command = input()
        words = input_command.split(' ')
        arg = None
        if words.__len__() == 3:
            arg = words[2]
            words.pop(2)

        command = '_'.join(words)
        if command not in commands:
            __error(ERROR)
            continue

        try:
            if arg is not None:
                commands[command](arg)
            else:
                commands[command]()
        except TypeError:
            __error(ERROR)

def __error(message):
    print('ERROR: %s' % message)

def __print_countries():
    countries = data.get_all(COUNTRY_KEY)
    print('Id, Name')
    if not countries:
        print('...There is nothing here...')
    for country in countries:
        print("%i\t%s" % (country.id, country.name))

def __print_cities():
    cities = data.get_all(CITY_KEY)
    print('Id, Country, Name, Population')
    if not cities:
        print('...There is nothing here...')
    for city in cities:
        country_name = data.get(COUNTRY_KEY, city.country_id).name
        print("%i\t%s\t%s\t%i" % (city.id, country_name, city.name, city.population))

def __validate_parse_positive_integer(string):
    try:
        value = int(string)
    except ValueError:
        __error('The value is not integer')
        return None
    if value < 0:
        __error('The value is negative')
        return None
    return value

def __validate_parse_id(data_key, string):
    data_id = __validate_parse_positive_integer(string)
    if data_id is None:
        return

    if not data.exists(data_key, data_id):
        __error('The object does not exist')
        return None

    return data_id

def __add_country():
    print('Please, enter the country name:')
    name = input()
    country = Country(0, name)
    data.add(COUNTRY_KEY, country)
    print('Added with id %i' % country.id)

def __add_city():
    print('Please, enter the country id:')
    country_id = __validate_parse_id(COUNTRY_KEY, input())
    if country_id is None:
        return

    print('Please, enter the city name:')
    name = input()

    print('Please, enter the population')
    population = __validate_parse_positive_integer(input())
    if population is None:
        return

    city = City(0, country_id, name, population)
    data.add(CITY_KEY, city)
    print('Added with id %i' % city.id)

def __deserialize():
    try:
        data.deserialize(SAVE_FILE_NAME)
    except ValueError:
        __error('The save file \'data.p\' does not exist')

def __remove_entity(key, data_id):
    data_id = __validate_parse_positive_integer(data_id)
    if data_id is None:
        return
    if not data.exists(key, data_id):
        __error('The object does not exist')
        return
    if data.is_key_for_foreignkey(key):
        print('Some objects may depend on this one. Are you sure that you want to delete it?')
        print('Note that all connected entities will be removed too.')
        print('Print \'y\' if you want to delete it anyways')
        if input().lower() not in ['y', 'yes']:
            print('Aborting...')
            return

    data.remove(key, data_id)
    print('The entity is successfully removed')

def __edit_country(country_id):
    country_id = __validate_parse_id(COUNTRY_KEY, country_id)
    if country_id is None:
        return

    country = data.get(COUNTRY_KEY, country_id)
    print('Type in the new name of the country[default=%s]:' % country.name)
    name = input()
    country.name = name or country.name
    print('The country was successfully changed')

def __edit_city(city_id):
    city_id = __validate_parse_id(CITY_KEY, city_id)
    if city_id is None:
        print('Aborting...')
        return

    city = data.get(CITY_KEY, city_id)
    print('Type in the new country id[default=%i]:' % city.country_id)
    country_id = input() or city.country_id
    country_id = __validate_parse_id(COUNTRY_KEY, country_id)
    if country_id is None:
        print('Aborting...')
        return

    print('Type in the new name of the city[default=%s]:' % city.name)
    name = input() or city.name

    print('Type in the new population[default=%i]:' % city.population)
    population = __validate_parse_positive_integer(input())
    if population is None:
        print('Aborting...')
        return

    city.country_id = country_id
    city.name = name
    city.population = population
    print('The city was changed successfully')


def __create_commands():
    commands = {
        'help': lambda: print(HELP),
        'list_countries': __print_countries,
        'list_cities': __print_cities,
        'add_city': __add_city,
        'add_country': __add_country,
        'edit_country': __edit_country,
        'edit_city': __edit_city,
        'remove_country': lambda id: __remove_entity(COUNTRY_KEY, id),
        'remove_city': lambda id: __remove_entity(CITY_KEY, id),
        'save': lambda: data.serialize(SAVE_FILE_NAME),
        'load': __deserialize,
        'exit': lambda: None
    }
    return commands

if __name__ == '__main__':
    __main()
