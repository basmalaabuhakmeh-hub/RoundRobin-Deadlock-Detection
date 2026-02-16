# Round Robin Scheduler with Resource Allocation & Deadlock Handling

Python implementation of Round Robin (RR) CPU scheduling with multiple resources. Processes have CPU bursts, optional I/O bursts, and can request/release resources (`R[i]`, `F[i]`). Includes **deadlock detection** and **recovery** (terminate one process to break the cycle). Reads a tab-separated process specification file and prints a Gantt chart, completion times, and average waiting and turnaround times.


## Overview

- **Scheduling:** Round Robin with configurable time quanta (e.g. 10 or 20).
- **Resources:** Each process can request resource `R[i]` for a duration and release it with `F[i]`; the scheduler tracks who holds each resource and blocks processes until the resource is free.
- **Deadlock:** When a cycle of waiting is detected (process A holds a resource needed by B, B holds one needed by A, etc.), **deadlock detection** runs and **recovery** terminates one process, releases its resources, and restarts it later (as per the report).
- **Output:** Gantt chart (process IDs and "idle"), per-process finish time / turnaround / waiting time, and average waiting and turnaround time.

**Input file format (tab-separated):**  
Each line describes one process: `pid`, `arrival_time`, `priority`, then CPU/IO bursts. Examples from the report:

- `CPU {R[0], 50, F[0]}` — request R[0], use CPU 50, release F[0]
- `CPU {20} IO{30} CPU {34, R[1], 30, F[1], 10}` — CPU 20, I/O 30, then CPU with a resource request in the middle
- `CPU {20, R[2], 30, F[2], 10}` — CPU 20, then request R[2] for 30, release F[2], then CPU 10

The code parses these patterns and builds internal `processes` and `request` lists for the RR and resource logic.

---

## Project structure

```
.
├── README.md
├── os_project2.pdf          # Report (test cases: no deadlock, deadlock + recovery)
└── main.py                  # RR scheduler, resource handling, deadlock detection & recovery
```

---

## Requirements

- **Python 3.x** (no extra packages; uses only the standard library).
- **Input file:** The program reads the process list from a **hardcoded path** in `main.py`:  
  `C:/Users/Asus/OneDrive/Documents/folder_python/os_project/processes`  
  Create a file named `processes` (no extension) in that directory with your test input, or change the path in `readfile()` to point to your own file (e.g. in the project folder).

---

## Usage

1. Create or edit the **processes** file with one process per line (tab-separated), using the CPU/IO/R/F format described in the report and in the code comments.
2. (Optional) In `main.py`, change the path in `readfile()` to your processes file, and set `time_qaunta` in `main()` (e.g. 10 or 20).
3. Run:

```bash
python main.py
```

Output includes the parsed processes and requests, the Gantt chart, completed processes with finish/turnaround/waiting times, and average waiting and turnaround time. If deadlock is detected, the program prints the involved processes and runs recovery (terminate one process, then continue).

---

## Report

Test cases (no deadlock and deadlock with recovery) and sample input format:  
**`os_project2.pdf`**
