# **Thread Pool Simulation - README**

Welcome to the **Thread Pool Simulation** project! This program simulates how a computer can handle multiple tasks at the same time using something called a **thread pool**. Think of it like a team of workers (threads) who are ready to do jobs (tasks) as soon as they come in. This README will explain everything you need to know to run the program and understand how it works step by step.

---

## **Table of Contents**
1. [What is a Thread Pool?](#what-is-a-thread-pool)
2. [What Does This Program Do?](#what-does-this-program-do)
3. [How to Run the Program](#how-to-run-the-program)
4. [How Does It Work?](#how-does-it-work)
   - [Step 1: Importing Libraries](#step-1-importing-libraries)
   - [Step 2: Defining the Task Class](#step-2-defining-the-task-class)
   - [Step 3: Creating the Priority Task Queue](#step-3-creating-the-priority-task-queue)
   - [Step 4: Creating the Thread Pool](#step-4-creating-the-thread-pool)
   - [Step 5: Creating the Simulation Report](#step-5-creating-the-simulation-report)
   - [Step 6: Loading Tasks from a File](#step-6-loading-tasks-from-a-file)
   - [Step 7: Generating a Task File](#step-7-generating-a-task-file)
   - [Step 8: Running the Simulation](#step-8-running-the-simulation)
5. [Example of the Task File](#example-of-the-task-file)
6. [Customizing the Program](#customizing-the-program)
7. [Why Is This Useful?](#why-is-this-useful)
8. [Troubleshooting](#troubleshooting)
9. [Have Fun!](#have-fun)

---

## **What is a Thread Pool?**
A **thread pool** is like a group of workers waiting for jobs. Instead of hiring a new worker every time a job comes in, we keep a team of workers ready. When a job arrives, one of the workers picks it up and gets it done. This makes things faster and more efficient!

---

## **What Does This Program Do?**
This program simulates a thread pool in action. Here’s what it does step by step:
1. **Generates Tasks**: It creates a list of random tasks (jobs) with different arrival times and durations.
2. **Creates a Thread Pool**: It sets up a team of workers (threads) to handle the tasks.
3. **Executes Tasks**: The workers pick up tasks from the queue and complete them.
4. **Generates a Report**: At the end, it tells you how long everything took, how many tasks were completed, and more.

---

## **How to Run the Program**

### **Step 1: Install Python**
Make sure you have **Python 3.x** installed on your computer. You can download it from [python.org](https://www.python.org/).

### **Step 2: Download the Code**
1. Copy the code from the `thread_pool.py` file.
2. Save it to a file on your computer, for example, `thread_pool.py`.

### **Step 3: Run the Program**
1. Open a terminal or command prompt.
2. Navigate to the folder where you saved the `thread_pool.py` file.
3. Run the program by typing:
   ```bash
   python thread_pool.py
   ```

---

## **How Does It Work?**

### **Step 1: Importing Libraries**
The program starts by importing the necessary libraries:
```python
import threading  # For creating and managing threads
import queue      # For creating a thread-safe task queue
import time       # For simulating task execution and delays
import random     # For generating random task data
import heapq      # For creating a priority queue
```

- **`threading`**: This library is used to create and manage threads (workers).
- **`time`**: This library is used to simulate delays (e.g., task execution time).
- **`random`**: This library is used to generate random task data.
- **`heapq`**: This library is used to create a priority queue for task prioritization.

---

### **Step 2: Defining the Task Class**
The `Task` class represents a task with three properties:
```python
class Task:
    def __init__(self, task_id, arrival_time, burst_time):
        self.task_id = task_id       # Unique ID for the task
        self.arrival_time = arrival_time  # When the task arrives
        self.burst_time = burst_time      # How long the task takes to complete

    def __lt__(self, other):
        # This method is used to prioritize tasks in the priority queue.
        # Tasks with shorter burst times are executed first.
        return self.burst_time < other.burst_time
```

- **`task_id`**: A unique number to identify the task.
- **`arrival_time`**: The time when the task arrives (in seconds).
- **`burst_time`**: The time it takes to complete the task (in seconds).
- **`__lt__`**: This method is used to compare tasks for prioritization.

---

### **Step 3: Creating the Priority Task Queue**
The `PriorityTaskQueue` class is a custom priority queue that sorts tasks based on their burst time:
```python
class PriorityTaskQueue:
    def __init__(self):
        self.queue = []  # The list to store tasks
        self.counter = 0  # To handle tasks with the same priority

    def put(self, task):
        # Add a task to the queue with its burst time as the priority
        heapq.heappush(self.queue, (task.burst_time, self.counter, task))
        self.counter += 1

    def get(self):
        # Remove and return the task with the highest priority (shortest burst time)
        return heapq.heappop(self.queue)[-1]

    def task_done(self):
        # No-op (does nothing) for simplicity
        pass

    def qsize(self):
        # Return the number of tasks in the queue
        return len(self.queue)
```

- **`heapq`**: This library is used to create a priority queue.
- **`put`**: Adds a task to the queue.
- **`get`**: Removes and returns the task with the shortest burst time.
- **`task_done`**: A placeholder method (does nothing in this implementation).
- **`qsize`**: Returns the number of tasks in the queue.

---

### **Step 4: Creating the Thread Pool**
The `ThreadPool` class manages the worker threads and the task queue:
```python
class ThreadPool:
    def __init__(self, min_threads, max_threads):
        self.min_threads = min_threads  # Minimum number of threads
        self.max_threads = max_threads  # Maximum number of threads
        self.task_queue = PriorityTaskQueue()  # Priority queue for tasks
        self.threads = []  # List to store worker threads
        self.stop_signal = False  # Signal to stop the threads
        self.lock = threading.Lock()  # Lock for thread-safe operations
        self.report = SimulationReport()  # For generating the simulation report

        # Create initial worker threads
        for _ in range(min_threads):
            self.add_thread()

    def add_thread(self):
        # Add a new worker thread if the maximum number of threads is not exceeded
        with self.lock:
            if len(self.threads) < self.max_threads:
                thread = threading.Thread(target=self.worker)
                thread.start()
                self.threads.append(thread)

    def worker(self):
        # Worker thread function: picks up tasks and executes them
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
        # Add a task to the queue and add more threads if needed
        if self.task_queue.qsize() > len(self.threads) and len(self.threads) < self.max_threads:
            self.add_thread()
        self.task_queue.put(task)

    def shutdown(self):
        # Stop all worker threads and generate the simulation report
        self.stop_signal = True
        for thread in self.threads:
            thread.join()
        self.report.generate_report()
```

- **`min_threads` and `max_threads`**: The minimum and maximum number of worker threads.
- **`task_queue`**: The priority queue for tasks.
- **`threads`**: A list to store worker threads.
- **`stop_signal`**: A flag to stop the threads gracefully.
- **`lock`**: A lock for thread-safe operations.
- **`report`**: An instance of `SimulationReport` to track simulation metrics.

---

### **Step 5: Creating the Simulation Report**
The `SimulationReport` class tracks and reports simulation metrics:
```python
class SimulationReport:
    def __init__(self):
        self.start_time = time.time()  # Start time of the simulation
        self.completed_tasks = 0  # Number of completed tasks
        self.total_burst_time = 0  # Total time spent on tasks

    def log_task_completion(self, burst_time):
        # Log a completed task and update metrics
        self.completed_tasks += 1
        self.total_burst_time += burst_time

    def generate_report(self):
        # Generate and print the simulation report
        end_time = time.time()
        total_time = end_time - self.start_time
        avg_task_time = self.total_burst_time / self.completed_tasks if self.completed_tasks > 0 else 0

        print("\nSimulation Report:")
        print(f"Total Simulation Time: {total_time:.2f} seconds")
        print(f"Number of Tasks Executed: {self.completed_tasks}")
        print(f"Average Task Completion Time: {avg_task_time:.2f} seconds")
```

- **`start_time`**: The time when the simulation starts.
- **`completed_tasks`**: The number of tasks completed.
- **`total_burst_time`**: The total time spent on tasks.
- **`log_task_completion`**: Logs a completed task and updates metrics.
- **`generate_report`**: Generates and prints the simulation report.

---

### **Step 6: Loading Tasks from a File**
The `load_tasks` function reads tasks from a file and enqueues them:
```python
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
```

- **`filename`**: The name of the file containing tasks.
- **`pool`**: The thread pool where tasks are enqueued.
- **`time.sleep(arrival)`**: Simulates the arrival time of each task.

---

### **Step 7: Generating a Task File**
The `generate_task_file` function creates a file with random tasks:
```python
def generate_task_file(filename, num_tasks):
    with open(filename, "w") as file:
        for task_id in range(1, num_tasks + 1):
            arrival = random.randint(0, 10)  # Random arrival time (0-10 seconds)
            burst = random.randint(1, 5)  # Random burst time (1-5 seconds)
            file.write(f"{task_id} {arrival} {burst}\n")
```

- **`filename`**: The name of the file to create.
- **`num_tasks`**: The number of tasks to generate.
- **`arrival`**: Random arrival time for each task.
- **`burst`**: Random burst time for each task.

---

### **Step 8: Running the Simulation**
The `main` function runs the simulation:
```python
def main():
    filename = "tasks.txt"
    generate_task_file(filename, 10)  # Generate a file with 10 random tasks
    pool = ThreadPool(min_threads=2, max_threads=5)  # Create a thread pool
    load_tasks(filename, pool)  # Load tasks from the file
    time.sleep(20)  # Let tasks execute (adjust as needed)
    pool.shutdown()  # Shutdown the thread pool and generate the report
```

- **`generate_task_file`**: Generates a file with random tasks.
- **`ThreadPool`**: Creates a thread pool with 2-5 worker threads.
- **`load_tasks`**: Loads tasks from the file and enqueues them.
- **`time.sleep(20)`**: Waits for tasks to complete.
- **`pool.shutdown()`**: Stops the thread pool and generates the report.

---

## **Example of the Task File**
The program generates a file called `tasks.txt` with tasks like this:
```
1 0 2
2 1 3
3 2 1
```
- The first number is the **task ID**.
- The second number is the **arrival time** (in seconds).
- The third number is the **burst time** (in seconds).

---

## **Customizing the Program**
You can change the program to do different things:
1. **Number of Tasks**: Change the number of tasks generated by editing this line in the code:
   ```python
   generate_task_file(filename, 10)  # Change 10 to any number
   ```
2. **Number of Workers**: Change the number of workers in the thread pool by editing this line:
   ```python
   pool = ThreadPool(min_threads=2, max_threads=5)  # Change the numbers
   ```

---

## **Why Is This Useful?**
This program helps you understand how computers handle multiple tasks at the same time. It’s used in real-world applications like:
- **Web Servers**: Handling multiple requests from users.
- **Video Games**: Running multiple tasks like rendering graphics and handling player input.
- **Operating Systems**: Managing processes and resources efficiently.

---

## **Troubleshooting**
If something doesn’t work:
1. Make sure you have Python installed.
2. Check that you saved the code in a file called `thread_pool.py`.
3. Make sure you’re running the program in the correct folder.

---

## **Have Fun!**
Now that you know how it works, run the program and see how the thread pool handles tasks. Try changing the number of tasks or workers and see what happens. Have fun exploring! 🚀

---
