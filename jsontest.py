import json

my_dict = {
    88005553535: {
        'first_name': 'Nikita',
        'last_name': 'Kolobov'
    }
}
with open('userstest.json', 'w') as file:
    json.dump(my_dict, file)


chatid = 88005553535
first_name = 'Nikita'
last_name = 'Kolobov'


def generate_dict_json(chat_id, fname, lname):
    my_dict3 = {
        chat_id: {
            'name': fname,
            'lname': lname
        }
    }
    return my_dict3

print(generate_dict_json(chatid, first_name, last_name))