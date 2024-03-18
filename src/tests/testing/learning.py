## Classes
import time

class Vehicle:

    tank_state = 100

    def __init__(self, brand: str, type: str, color: str, wheels: int):
        self.brand = brand
        self.type = type
        self.color = color
        self.wheels = wheels
        
    def Show_Specs(self):
        self.string = f"These are the specs: Brand: {self.brand}, Type: {self.type}, Color: {self.color}, No. of wheels: {self.wheels}."
        return self.string

    def Run(self, state: bool):
        self.running = state
        while True:
            if self.tank_state > 0:
                print("Running")
                self.tank_state -= 20
                time.sleep(1)
            else:
                self.running = False
                if self.running == False:
                    print("Car stopped.")
                    time.sleep(1)
                    print("Parking...")
                    time.sleep(1)
                    print("Ready to refuel.")
                    time.sleep(1)
                    self.Refuel(True)
                

    def Refuel(self, state: bool):
        refueling = state
        if self.tank_state == 0:
            print("Refueling...")
            while refueling:
                if self.tank_state < 100:
                    time.sleep(1)
                    self.tank_state += 20
                    print(f"Tank Currently at {self.tank_state}%")
                else:
                    print("Tank full, ready to drive...")
                    time.sleep(1)
                    print("Going in the road...")
                    time.sleep(1)
                    break


car = Vehicle('Toyota', 'Car', 'Red', 4)

car.Run(True)