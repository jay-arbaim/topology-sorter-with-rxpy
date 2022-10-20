from threading import Thread
from queue import Queue
import random

class WorkerManager:
    def __init__(self, thread_num=1):
        self.worker_list = []
        self.task_queue = Queue()
        for _ in range(thread_num):
            self.worker_list.append(Worker(self.task_queue))
    def add_task(self, task):
        self.task_queue.put(task)
class Worker(Thread):
    def __init__(self, task_queue):
        num = random.randint(0, 100)
        print("Worker {} is created".format(num))
        Thread.__init__(self)
        self.name = "Worker_{}".format(num)
        self.task_queue = task_queue
        self.daemon = True
        self.start()
    def run(self):
        while True:
            task = self.task_queue.get()
            print("Worker {} is running task".format(self.name))
            task()
    def stop(self):
        pass
