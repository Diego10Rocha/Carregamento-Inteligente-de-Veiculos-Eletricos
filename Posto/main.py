# This is a sample Python script.
from Posto import Posto
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def run_posto() -> None:
    region_id = int(input("Digite a regiao do posto: "))
    my_posto = Posto(region_id)
    print("Id da região:", my_posto.region_id)
    my_posto.start()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_posto()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
