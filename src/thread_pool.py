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
