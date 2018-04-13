import sys, json
import os.path

FILENAME = 'todo.json'
FILENAME = '/Users/breyerjs/code/todo_commandline/todo.json'

def main():
    todo_dict = load_or_create_file_contents()

    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]

    if command == 'add':
        add_todo(sys.argv, todo_dict)

    elif command == 'ls':
        show_todos(todo_dict)

    elif command == 'la':
        show_todos(todo_dict, True)

    elif command == 'rm':
        remove_todo(sys.argv, todo_dict)
    
    elif command == 'mv':
        mark_complete(todo_dict, sys.argv)

    elif command == 'clearAllDone':
        clear_all_done(todo_dict)

    elif command == 'help':
        show_help()

def load_or_create_file_contents():
    if not os.path.isfile(FILENAME):
        create_initial_json()
    # see https://stackoverflow.com/questions/1466000/python-open-built-in-function-difference-between-modes-a-a-w-w-and-r
    with open(FILENAME,'r+') as f:
        return json.load(f)

def create_initial_json():
    structure = {
        'in_progress': [],
        'done': []
    }
    
    json_structure = json.dumps(structure)
    with open(FILENAME, 'w+') as outfile:
        json.dump(structure, outfile)

def show_todos(todo_dict, show_all=False):
    print("\n" + bcolors.OKGREEN + "To Do:" + bcolors.ENDC)
    item_num = 0
    for item in todo_dict['in_progress']:
        print(" "*4 + bcolors.YELLOW + str(item_num) + bcolors.ENDC + ". " + item)
        item_num += 1
    if show_all:
        print(bcolors.OKGREEN + "Done:" + bcolors.ENDC)
        for item in todo_dict['done']:
            print(" "*4 + bcolors.YELLOW +  "x " + bcolors.ENDC + item)
    print("") # a de facto new line

def save_json(todo_dict):
    # clear and write to file
    with open(FILENAME, 'w+') as todo_file:
        todo_file.truncate()
        json.dump(todo_dict, todo_file)

def add_todo(args, todo_dict):
    if len(args) <= 1:
        print("Please enter a todo item")
        return
    
    todo_item = ' '.join(args[2:])
    todo_dict['in_progress'].append(todo_item)
    print("Todo added")
    save_json(todo_dict)
    show_todos(todo_dict)

def remove_todo(args, todo_dict):
    if len(args) <= 1 or not isInteger(args[2]):
        print('Please indicate the index of a todo item to remove')
        return
    index = int(args[2])
    todo_dict['in_progress'].pop(index)
    save_json(todo_dict)
    show_todos(todo_dict)

def mark_complete(todo_dict, args):
    if len(args) <= 1 or not isInteger(args[2]):
        print('Please indicate the index of a todo item to complete')
        return
    index = int(args[2])
    todo_dict['done'].append(todo_dict['in_progress'].pop(index))
    save_json(todo_dict)
    show_todos(todo_dict, True)

def clear_all_done(todo_dict):
    todo_dict['done'] = []
    save_json(todo_dict)
    show_todos(todo_dict, True)

def isInteger(string_val):
    try:
        int(string_val)
        return True
    except ValueError:
        return False

def show_help():
    print("""
`add <something>`: adds a todo item
`ls`: shows all in progress todo items
`la`: shows all in progress and completed todo items
`mv <index>`: completes a todo item
`rm <index>`: deletes an in progress todo item
`clearAllDone`: clears all completed todos
`help`: shows this key
""")

class bcolors:
    ENDC = '\033[0m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
              
if __name__ == "__main__":
    main()
