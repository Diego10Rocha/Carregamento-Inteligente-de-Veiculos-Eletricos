# This is a sample Python script.
from Nevoa import Nevoa
from consts import CLOUD_NEVOA_PORT, CLOUD_ADDR, REGION_1, REGION_2, REGION_3
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def run_nevoa() -> None:
    region = int(input("Digite a região da nevoa: "))
    my_nevoa = Nevoa(region, "localhost", CLOUD_NEVOA_PORT)
    my_nevoa.run()
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_nevoa()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
