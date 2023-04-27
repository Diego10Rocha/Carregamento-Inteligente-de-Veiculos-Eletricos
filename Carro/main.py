from Carro import Car
from SoftApi import SoftAPI

car_region = int(input("Digite a regiao do carro: "))
carro = Car(car_region)
carro.start()

my_api = SoftAPI("0.0.0.0", 8889, car_region)
my_api.create_get("posto")
my_api.create_server()
my_api.server_on()
