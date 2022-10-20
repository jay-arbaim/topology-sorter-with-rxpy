import operator as op

from taskmanager.task_manager import TaskManager
from node.node import Node

class StartNode(Node):
    def __init__(self, name="Start"):
        super().__init__(name)
        self.name = name
        self.input_format = []
        self.output_format = [{"name": "test_number", "type": "INT64", "shape": [1]}]
    def task(self):
        super().task()
        self.output = [10]

class BypassNode(Node):
    def __init__(self, name="Bypass"):
        super().__init__(name)
        self.name = name
        self.input_format = [{"name": "test_number", "type": "INT64", "shape": [1]}]
        self.output_format = [{"name": "test_number", "type": "INT64", "shape": [1]}]
    def task(self):
        super().task()
        self.output = self.input

class SquareNode(Node):
    def __init__(self, name="Square"):
        super().__init__(name)
        self.name = name
        self.input_format = [{"name": "test_number", "type": "INT64", "shape": [1]}]
        self.output_format = [{"name": "test_number", "type": "INT64", "shape": [1]}]
    def task(self):
        super().task()
        self.output.append(op.mul(self.input[0], self.input[0]))

class ArithmeticOperationNode(Node):
    def __init__(self, operator, name="ArithmeticOperation"):
        super().__init__(name)
        self.name = name
        self.operator = operator
        self.input_format = [{"name": "test_number", "type": "INT64", "shape": [1]}, {"name": "test_number", "type": "INT64", "shape": [1]}]
        self.output_format = [{"name": "test_number", "type": "INT64", "shape": [1]}]
    def task(self):
        super().task()
        operator_map = {"+": op.add, "-": op.sub, "*": op.mul, "/": op.truediv}
        self.output.append(operator_map[self.operator](self.input[0], self.input[1]))

def test_squre_task():
    task_manager = TaskManager()
    start_node = StartNode()
    task_manager.add_node(start_node)
    square_node = SquareNode()
    task_manager.add_node(square_node)
    task_manager.add_edge(start_node, square_node)
    task_manager.validate_topology()
    task_manager.run()
    
    result = task_manager.get_task_output()
    print("Result: {}".format(result))
    assert result == [100]

def test_arithmetic_operation_task():
    task_manager = TaskManager()
    start_node1 = StartNode("Start1")
    start_node2 = StartNode("Start2")
    task_manager.add_node(start_node1)
    task_manager.add_node(start_node2)
    
    add_node = ArithmeticOperationNode("+", "Add")
    minus_node = ArithmeticOperationNode("-", "Minus")
    multiply_node = ArithmeticOperationNode("*", "Multiply")
    divide_node = ArithmeticOperationNode("/", "Divide")
    task_manager.add_node(add_node)
    task_manager.add_node(minus_node)
    task_manager.add_node(multiply_node)
    task_manager.add_node(divide_node)
    
    task_manager.add_edge(start_node1, add_node)
    task_manager.add_edge(start_node2, add_node)
    task_manager.add_edge(start_node1, minus_node)
    task_manager.add_edge(start_node2, minus_node)
    task_manager.add_edge(start_node1, multiply_node)
    task_manager.add_edge(start_node2, multiply_node)
    task_manager.add_edge(start_node1, divide_node)
    task_manager.add_edge(start_node2, divide_node)
    
    task_manager.validate_topology()
    task_manager.run()
    
    result = task_manager.get_task_output()
    print("Result: {}".format(result))

test_squre_task()
test_arithmetic_operation_task()