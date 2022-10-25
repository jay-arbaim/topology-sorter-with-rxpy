import time, random
from queue import Queue
from graphlib import TopologicalSorter

from functools import partial
from .worker_manager import WorkerManager

class TaskManager:
    def __init__(self):
        self.node_list = []
        self.topology = {}
        self.topology_sorter = TopologicalSorter()
        self.prepared_task_queue = Queue()
        self.finished_task_queue = Queue()
        self.result = []
    def add_node(self, node):
        self.node_list.append(node)
    def add_edge(self, from_node, to_node):
        if from_node not in self.node_list or to_node not in self.node_list:
            raise ValueError("node is not in node_list")
        # check input and output format for connection
        for output_format in from_node.output_format:
            for input_format in to_node.input_format:
                if input_format["name"] == output_format["name"] and input_format["type"] == output_format["type"] and input_format["shape"] == output_format["shape"]:
                    break
            else:
                raise ValueError("from_node and to_node are not compatible")
        self.topology_sorter.add(to_node, from_node)
        if from_node in self.topology.keys():
            self.topology[from_node].append(to_node)
        else:
            self.topology[from_node] = [to_node]
    def validate_topology(self):
        self.topology_sorter.prepare()
    def run(self):
        worker_manager = WorkerManager(thread_num=4)
        while self.topology_sorter.is_active():
            # get next nodes
            for node in self.topology_sorter.get_ready():
                self.prepared_task_queue.put(node)
            while not self.prepared_task_queue.empty():
                node = self.prepared_task_queue.get()
                # run task of the node & push output of the node to next node
                def node_task_and_post_task(node):
                    time.sleep(random.random())
                    node.task()
                    if node in self.topology.keys():
                        for to_node in self.topology[node]:
                            to_node.input += node.output
                    else:
                        self.result += node.output
                    # put node that finished task to finished_task_queue
                    # data of node will be put to task_output_buffer
                    self.finished_task_queue.put(node)
                    self.topology_sorter.done(node)
                    print("Finished task: {}".format(node.name))
                worker_manager.add_task(partial(node_task_and_post_task, node))
                while self.finished_task_queue.get():
                    if(self.finished_task_queue.empty()):
                        break
    def get_task_output(self):
        return self.result

                