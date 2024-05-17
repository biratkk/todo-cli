import os
import sys
from dataclasses import dataclass

todo_fp = "todo.md"

cli_tool_instructions = [
        ("ls", "Lists all of the todos left to do"),
        ("create", "Create a new todo file in the current directory"),
        ("reset", "Reset the todo file in current directory"),
        ("comp <id>", "Marks the todo with id provided as complete"),
        ("undo <id>", "Marks the todo with id provided as undone"),
        ("add <description>", "Adds the arguments as a todo to the list"),
        ("rm <id>", "Removes the todo with the id provided"),
        ("gui", "Run the gui for the todo program"),
        ("help", "Help text provided"),
        ("exit", "Exits the program"),
]

@dataclass
class Todo:
    index: int
    complete: bool
    description: str

class CLI_STR:
    @staticmethod
    def underline(s: str):
        return f'\033[4m{s}\033[0m'

todos:list[Todo] = []

def check(flag: bool, message: str):
    if flag == False:
        print(f"Please check the following: {message}")
        exit()


def clear_screen():
    if os.name == 'nt':
        # Clearing the Screen in windows
        os.system('cls')
    else:
        # Clearing the Screen in mac / linux
        os.system('clear')

def validate_file(fp:str):
    check(os.path.isfile(fp), file_name_underlined())

def parse_todo(index: int, plaintext: str) -> Todo | None:
    if not plaintext.startswith("- "):
        return
    complete = plaintext.startswith("- [x]")
    desc = plaintext[5:].strip()
    return Todo(index=index, complete=complete, description=desc)

def file_name_underlined():
    return CLI_STR.underline(f'{todo_fp}')

def import_todos(fp: str):
    validate_file(fp)

    lines = []
    with open(fp, "r+") as file:
        lines = file.read().split("\n")
    

    global todos
    todos = []
    for index, line in enumerate(lines):
        todo = parse_todo(index, line)
        if todo is not None:
            todos.append(todo)



def list_todos():
    print(file_name_underlined())
    for todo in todos:
        complete_emoji = '✅' if todo.complete else '❌'
        print(complete_emoji, todo.index+1, todo.description)

def add(args:list[str]):
    desc = " ".join(args)
    with open(todo_fp, "a") as file:
        file.write(f"\n- [ ] {desc}")


def remove(id: int):
    text = []
    with open(todo_fp, "r") as file:
        text = file.read().split("\n")

    del text[id]

    with open(todo_fp, "w") as file:
        file.write("\n".join(text))

def complete(id: int):
    text = []
    with open(todo_fp, "r") as file:
        text = file.read().split("\n")

    text[id] = text[id].replace("[ ]", "[x]")

    with open(todo_fp, "w") as file:
        file.write("\n".join(text))

def undo(id: int):
    text = []
    with open(todo_fp, "r") as file:
        text = file.read().split("\n")

    text[id] = text[id].replace("[x]", "[ ]")

    with open(todo_fp, "w") as file:
        file.write("\n".join(text))


def prompt() -> list[str]:
    return input(">>> ").split(" ")


def create_initial_file():
    with open(todo_fp, "w") as file:
        file.write("- [ ] Delete this todo using todo rm 1")

def reset():
    create_initial_file()
    print("Reset complete!")

def create():
    if os.path.isfile(todo_fp):
        print("File already exists. To reset it use the command todo reset")
        return

    create_initial_file()  
    print("Todo file created!")
    return

def gui():
    help()
    while True:
        action(prompt(), True)
        
def print_divider():
    print("---------------------------------------------------------")

def help():
    print_divider()
    print("The following are the instructions in case you forget em")
    print_divider()
    for tool, instruction in cli_tool_instructions:
        print(f"{tool}\n\t{instruction}")
    print_divider()

def action(args:list[str], in_gui: bool=False):

    if args[0] == 'create':
        create()
        return
    elif args[0] == 'help':
        help() 
        return

    import_todos(todo_fp)
    if args[0] == 'ls':
        list_todos() 
    elif args[0] == 'reset':
        reset() 
    elif args[0] == 'add':
        add(args[1:])
    elif args[0] == 'rm':
        remove(int(args[1]) - 1)
    elif args[0] == 'comp':
        complete(int(args[1]) - 1)
    elif args[0] == 'undo':
        undo(int(args[1]) - 1)
    elif not in_gui and args[0] == 'gui':
        clear_screen()
        gui()
    elif args[0] == 'clear':
        clear_screen() 
    elif args[0] == 'exit':
        exit()
    else:
        print("Invalid command.")
        help()

show_help_text = len(sys.argv) == 1
if show_help_text:
    help()
    exit()
action(sys.argv[1:])
