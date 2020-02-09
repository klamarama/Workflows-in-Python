class Person:
    def __init__(self, name, age, licensed):
        self.name = name
        self.age = age
        self.licensed = licensed


class Vehicle:
    def __init__(self, wheels, fuel):
        self.wheels = wheels
        self.fuel = fuel


class Car(Vehicle):
    def __init__(self, make, model):
        self.make = make
        self.model = model
        self.wheels = 4
        self.fuel = 100


