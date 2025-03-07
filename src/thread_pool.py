import threading
import time
import random
import heapq

# Task class to represent a task with arrival time and burst time
class Task:
    def __init__(self, task_id, arrival_time, burst_time):
        self.task_id = task_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time

    def __lt__(self, other):
        # Priority comparison for the priority queue (lower burst time has higher priority)
        return self.burst_time < other.burst_time
# Priority task queue to prioritize tasks based on burst time
class PriorityTaskQueue:
    def __init__(self):
        self.queue = []
        self.counter = 0  # To handle tasks with the same priority

    def put(self, task):
        heapq.heappush(self.queue, (task.burst_time, self.counter, task))
        self.counter += 1

    def get(self):
        return heapq.heappop(self.queue)[-1]

    def task_done(self):
        pass  # No-op for simplicity

    def qsize(self):
        return len(self.queue)
