from queue import Queue
from threading import Thread
import requests
import time
from pandas.core.frame import DataFrame
from typing import List, Callable, Any


class Worker(Thread):
    """Thread handling the task"""
    def __init__(self, tasks: Queue):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            callback, params = self.tasks.get()
            print(params)
            try:
                print(callback(*params))
            except Exception as e:
                print(e)
            finally:
                self.tasks.task_done()


class Pool:
    """Pool organising tasks in queue"""
    def __init__(self, threads: int):
        self.q = Queue(threads)
        for _ in range(threads):
            Worker(self.q)

    def add_to_queue(self, callback: Callable, params: Any):
        self.q.put((callback, params))

    def wait(self):
        self.q.join()


base_url = "https://dummyjson.com/"
categories = ["products", "carts", "users", "posts", "comments", "quotes", "todos"]


if __name__ == "__main__":
    data = []

    with requests.Session() as session:
        con_start_time = time.time()
        pool = Pool(len(categories))
        for cat in categories:
            pool.add_to_queue(session.get, [base_url + cat])
        pool.wait()
        con_end_time = time.time() - con_start_time

    seq_start_time = time.time()
    for cat in categories:
        response = requests.get(base_url + cat)
    seq_end_time = time.time() - seq_start_time
        # data.append(response.text)
    print(f"seq:{seq_end_time}", f"parallel:{con_end_time}")
