from threading import current_thread

class Node:
    def __init__(self, name=""):
        self.name = name
        self.input_format = [{"name": "", "type": "", "shape": []}]
        self.output_format = [{"name": "", "type": "", "shape": []}]
        self.input = []
        self.output = []
        print("Node {} is created".format(self.name))
    def task(self):
        print("Node {} is running on {}".format(self.name, current_thread().name))
        # Do something with inputs
        # And fill outputs
    def free(self):
        print("Node {} is free".format(self.name))
    def __repr__(self):
        return "Node({}, {}, {})".format(self.name, self.input_format, self.output_format)
    def __str__(self):
        return "Node({}, {}, {})".format(self.name, self.input_format, self.output_format)
