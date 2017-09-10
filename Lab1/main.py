from Data.dataholder import DataHolder
from city import City
from country import Country


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
ERROR = 'Sorry, this command does not exist'

# Data initialisation
data = DataHolder()
COUNTRY_KEY = 'country'
CITY_KEY = 'city'
SAVE_FILE_NAME = 'data.p'

def __main():
    commands = __create_commands()
    print(HELP)

    data.make_foreign_key(CITY_KEY, 'country_id', COUNTRY_KEY)

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
            print(ERROR)
            continue;

        try:
            if arg is not None:
                commands[command](arg)
            else:
                commands[command]()
        except Exception as e:
            print(ERROR)

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

def __add_country():
    print('Please, enter the country name:')
    name = input()
    country = Country(0, name)
    data.add(COUNTRY_KEY, country)
    print('Added with id %i' % country.id)

def __add_city():
    while True:
        print('Please, enter the country id:')
        id = input()
        try:
            id = int(id)
        except ValueError:
            print('The value is not integer')
            continue
        if not data.exists(COUNTRY_KEY, id):
            print('Country with this id does not exist')
            continue
        break

    print('Please, enter the city name:')
    name = input()

    while True:
        print('Please, enter the population')
        population = input()
        try:
            population = int(population)
        except ValueError:
            print('The population is not integer')
            continue
        break
    city = City(0, id, name, population)
    data.add(CITY_KEY, city)
    print('Added with id %i' % city.id)


def __create_commands():
    commands = {
        'help': lambda: print(HELP),
        'list_countries': __print_countries,
        'list_cities': __print_cities,
        'add_city': __add_city,
        'add_country': __add_country,
        'save': lambda: data.serialize(SAVE_FILE_NAME),
        'load': lambda: data.deserialize(SAVE_FILE_NAME), 
        'exit': lambda: None
    }
    return commands

if __name__ == '__main__':
    __main()
