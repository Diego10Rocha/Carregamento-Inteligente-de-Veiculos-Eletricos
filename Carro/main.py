from fastapi import FastAPI

from Carro import *

app = FastAPI()


@app.get("/posto")
async def root():
    car = Car()
    if car.recharging:
        return {"message": str("O carro está sendo reccarregado no posto com id:", car.best_station.id)}
    return {"message": str("O carro está carregado com", car.battery_level, "% de bateria")}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

