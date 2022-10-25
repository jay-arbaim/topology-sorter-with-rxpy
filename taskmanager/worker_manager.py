import multiprocessing
from threading import current_thread
from queue import Queue
from enum import Enum

import reactivex
from reactivex.scheduler import ThreadPoolScheduler
from reactivex import operators as ops

class WorkerManager:
    def __init__(self, thread_num=1):
        def get_task(observer, scheduler):
            while True:
                observer.on_next(self.task_queue.get())
        self.task_queue = Queue()
        optimal_thread_count = multiprocessing.cpu_count()
        pool_scheduler = ThreadPoolScheduler(optimal_thread_count)
        for _ in range(thread_num):
            reactivex.create(get_task).pipe(
                ops.subscribe_on(pool_scheduler)
            ).subscribe(
                on_next = lambda task: task(),
                on_completed = lambda: print("All tasks are done"),
            )
        print("WorkerManager is created on {}".format(current_thread().name))
    def add_task(self, task):
        self.task_queue.put(task)
