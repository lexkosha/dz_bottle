import requests
import sys
# Данные авторизации в API Trello  
auth_params = {    
    'key': "Enter your key !!!",    
    'token': "Enter your token !!!", }  
  
# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.  
base_url = "https://api.trello.com/1/{}"  
board_id="Enter your board_d !!!!"

def read():
    print("\n--====== Task list: ======--\n")
    
    # Получим данные всех колонок на доске:    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:
        #print(column['name'])
        # Получим данные всех задач в колонке и перечислим все названия   
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print('\t' + column['name']+ " - ({})".format(len(task_data)) + '\n')
        if not task_data:
            print('\t\t' + 'Нет задач!' + '\n')
            continue
        for task in task_data:
            print('\t\t' + task['name'] + '\t\t'  + task['id'])
        print('\n')
    
    print("\n--====== Instructions Options ======--")
    print("trello_console_client.py 'Read all column and tasks from server' ")
    print("trello_console_client.py create [task_name] [column_name]")
    print("trello_console_client.py move [task_name] [column_name]")
    print("trello_console_client.py 'create column' [column_name]")
    print("\n\n")


def column_check(column_name):
    column_id = None
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        if column['name'] == column_name:
            column_id = column['id']
            return column_id
    return

def get_task_duplicates(task_name):  
    # Получим данные всех колонок на доске  
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()  
    # Заведём список колонок с дублирующимися именами  
    duplicate_tasks = []  
    for column in column_data:  
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()  
        for task in column_tasks:  
            if task['name'] == task_name:  
                duplicate_tasks.append(task)  
    return duplicate_tasks

def create_column(column_name):
    return requests.post(base_url.format('lists'), data={'name':column_name,'idBoard': board_id, **auth_params}).json()


def create(name, column_name):
    column_id = column_check(column_name)
    if column_id is None:
        column_id = create_column(column_name)['id']
    requests.post(base_url.format('cards'), data={'name': name, 'idList': column_id, **auth_params})
    read()

def move(name, column_name):
    duplicate_tasks = get_task_duplicates(name)
    if len(duplicate_tasks) > 1:
        print("There are several tasks with this name:")
        for index, task in enumerate(duplicate_tasks):
            task_column_name = requests.get(base_url.format('lists') + '/' + task['idList'], params=auth_params).json()['name']
            print("Task №{}\tid: {}\tIs in the column: {}\t ".format(index, task['id'], task_column_name))
        task_id = input("Please enter the ID of the task you want to move: ")
    else:
        task_id = duplicate_tasks[0]['id']
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить
    # Получим ID колонки, в которую мы будем перемещать задачу
    column_id = column_check(column_name)
    if column_id is None:
        column_id = create_column(column_name)['id']
    # И совершим перемещение:
    requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column_id, **auth_params})
    read()
    
if __name__ == "__main__":
    #print(len(sys.argv))
    #print(sys.argv)
    if (len(sys.argv) <= 2):
        if (len(sys.argv)!=1):
            print("\n    !!! Missing value !!! Please see the instrunctions! \n")
        read()
    elif sys.argv[1] == 'create':
        if(len(sys.argv) <=2):
            print("\n    !!! Missing value !!! Please see the instrunctions! \n")
            read()
        else:
            create(sys.argv[2], sys.argv[3])
            read()
    elif sys.argv[1] == 'create column':
        create_column(sys.argv[2])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
