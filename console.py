import os
from colors import Colors


def clear() -> None:
    os.system('cls') if os.name == "nt" else os.system('clear')

def print_menu(buttons: list[str]) -> None:
    for i, text in enumerate(buttons):
        print(f"[{Colors.BLUE}{i+1}{Colors.END}] {text}")

def print_table(dicts: list[dict]) -> None:
    if len(dicts) == 0:
        return
    for key in dicts[0].keys():
        print('{:25s}'.format(str(key).replace('_', ' ').capitalize()), end='')
    print('\n' + '-' * 25 * len(dicts[0]))
    for dict in dicts:
        for value in dict.values():
            value = str(value)
            print('{:25s}'.format(value), end='')
            print(' '*9 if Colors.END in value else '', end='')
        print()
    print('-' * 25 * len(dicts[0]) + '\n')