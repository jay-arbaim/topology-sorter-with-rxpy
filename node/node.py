from threading import current_thread

from node.pin import Pin

class Node:
    name: str
    pins: list[Pin]
    def __init__(self, name=""):
        self.name = name
        self.pins = []
        print("Node {} is created".format(self.name))
    def process(self):
        def fill_data_to_pin(data:dict):
            for pin in [pin for pin in self.pins if pin.direction == "output" and pin.name == data.get("key")]:
                pin.buffer.put(data.get("value"))
            
            
            
        result = self.task()
        
    def task(self):
        print("Node {} is running on {}".format(self.name, current_thread().name))
        # Do something with inputs
        # And fill outputs
    def free(self):
        print("Node {} is free".format(self.name))
    def __repr__(self):
        return "Node({}, {}, {})".format(self.name, self.pins)
    def __str__(self):
        return "Node({}, {}, {})".format(self.name, self.pins)
