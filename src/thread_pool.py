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
    
# Thread pool class with dynamic resizing
class ThreadPool:
    def __init__(self, min_threads, max_threads):
        self.min_threads = min_threads
        self.max_threads = max_threads
        self.task_queue = PriorityTaskQueue()  # Use priority queue for task prioritization
        self.threads = []
        self.stop_signal = False
        self.lock = threading.Lock()
        self.report = SimulationReport()

        # Create initial worker threads
        for _ in range(min_threads):
            self.add_thread()

    def add_thread(self):
        with self.lock:
            if len(self.threads) < self.max_threads:
                thread = threading.Thread(target=self.worker)
                thread.start()
                self.threads.append(thread)

    def worker(self):
        while not self.stop_signal:
            try:
                task = self.task_queue.get()
                print(f"Executing Task {task.task_id} (Arrival: {task.arrival_time}, Burst: {task.burst_time})")
                time.sleep(task.burst_time)  # Simulate task execution
                print(f"Task {task.task_id} Completed (Arrival: {task.arrival_time}, Burst: {task.burst_time})")
                self.report.log_task_completion(task.burst_time)
                self.task_queue.task_done()
            except IndexError:  # No tasks in the queue
                time.sleep(1)  # Sleep briefly to avoid busy-waiting

    def enqueue_task(self, task):
        if self.task_queue.qsize() > len(self.threads) and len(self.threads) < self.max_threads:
            self.add_thread()  # Add a new thread if the queue is overloaded
        self.task_queue.put(task)

    def shutdown(self):
        self.stop_signal = True
        for thread in self.threads:
            thread.join()
        self.report.generate_report()

# Simulation report class to track metrics
class SimulationReport:
    def __init__(self):
        self.start_time = time.time()
        self.completed_tasks = 0
        self.total_burst_time = 0

    def log_task_completion(self, burst_time):
        self.completed_tasks += 1
        self.total_burst_time += burst_time

    def generate_report(self):
        end_time = time.time()
        total_time = end_time - self.start_time
        avg_task_time = self.total_burst_time / self.completed_tasks if self.completed_tasks > 0 else 0

        print("\nSimulation Report:")
        print(f"Total Simulation Time: {total_time:.2f} seconds")
        print(f"Number of Tasks Executed: {self.completed_tasks}")
        print(f"Average Task Completion Time: {avg_task_time:.2f} seconds")

#  Function to load tasks from a file and enqueue them
def load_tasks(filename, pool):
    try:
        with open(filename, "r") as file:
            for line in file:
                try:
                    task_id, arrival, burst = map(int, line.split())
                    time.sleep(arrival)  # Simulate task arrival time
                    pool.enqueue_task(Task(task_id, arrival, burst))
                except ValueError:
                    print(f"Invalid task data: {line.strip()}")
    except FileNotFoundError:
        print(f"File not found: {filename}")

# Function to generate a task file with random tasks
def generate_task_file(filename, num_tasks):
    with open(filename, "w") as file:
        for task_id in range(1, num_tasks + 1):
            arrival = random.randint(0, 10)  # Random arrival time (0-10 seconds)
            burst = random.randint(1, 5)  # Random burst time (1-5 seconds)
            file.write(f"{task_id} {arrival} {burst}\n")


def main():
    filename = "tasks.txt"
    generate_task_file(filename, 10) 
    pool = ThreadPool(min_threads=2, max_threads=5) 
    load_tasks(filename, pool)  
    time.sleep(20)  
    pool.shutdown()  

if __name__ == "__main__":
    main()