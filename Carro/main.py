from SoftApi import SoftAPI

my_api = SoftAPI("0.0.0.0", 8889)
my_api.create_get("posto")
my_api.create_server()
my_api.server_on()
