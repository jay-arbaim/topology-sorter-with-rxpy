from dataclasses import dataclass, field
from queue import Queue

@dataclass
class Pin:
    name: str
    direction: str
    type: str
    shape: list[int]
    buffer: Queue = field(default_factory=Queue)
    connected: bool = False
    prev: "Pin" = None
    next: "Pin" = None

    def validate_connection(self, pin: "Pin"):
        if self.direction == pin.direction:
            raise ValueError("pin direction is not compatible")
        if self.name != pin.name:
            raise ValueError("pin name is not compatible")
        if self.type != pin.type:
            raise ValueError("pin type is not compatible")
        if self.shape != pin.shape:
            raise ValueError("pin shape is not compatible")
    
    def connect(self, pin: "Pin"):
        if(self.connected == True or pin.connected == True):
            raise ValueError("pin is already connected")
        if self.direction == "input":
            self.prev = pin
            pin.next = self
        else:
            self.next = pin
            pin.prev = self
        self.connected = True
        pin.connected = True

    def commit_data(self, data):
        self.buffer.push(data)

    def transfer_data(self, pin: "Pin"):
        if self.direction == "input":
            self.buffer.put(pin.buffer.get())
        else:
            pin.buffer.put(self.buffer.get())

    def pull_data(self):
        if self.prev:
            self.prev.transfer_data(self)

    def push_data(self):
        if self.next:
            self.transfer_data(self.next)