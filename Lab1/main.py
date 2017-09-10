from dataholder import DataHolder
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
        exit \
    "
ERROR = 'Sorry, this command does not exist'

# Data initialisation
data = DataHolder()
COUNTRY_KEY = 'country'
CITY_KEY = 'city'

def __main():
    commands = __create_commands()
    print(HELP)

    data.make_foreign_key(CITY_KEY, 'country_id', COUNTRY_KEY)

    input_command = ""
    while input_command != 'exit':
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

        commands[command]()

def __print_countries():
    countries = data.get_all(COUNTRY_KEY)
    print('Id, Name')
    for country in countries:
        print("%i\t%s" % (country.id, country.name))

def __print_cities():
    cities = data.get_all(CITY_KEY)
    print('Id, Country, Name, Population')
    for city in cities:
        country_name = data.get(COUNTRY_KEY, city.country_id).name
        print("%i\t%s\t%s\t%i" % (city.id, country_name, city.name, city.population))

def __create_commands():
    commands = {
        'help': lambda: print(HELP),
        'list_countries': __print_countries,
        'list_cities': __print_cities,
        'add_city': lambda: data.add(CITY_KEY, City(0, 0, "all", 123)),
        'add_country': lambda: data.add(COUNTRY_KEY, Country(0, "Name")),
        'exit': lambda: None
    }
    return commands

if __name__ == '__main__':
    __main()
