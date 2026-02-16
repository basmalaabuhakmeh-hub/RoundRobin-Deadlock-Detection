import copy
processes = []  # [pid,arrival time,priority,burst1cpu,burstIO,burst2cpu]
request = []  # [resource number, pid, timeasking,realeseAfter,CPUBurst 1 or 2]
resourcenumberarr = []
numR = 0
numP = 0
def readfile():
    global numR, numP
    with open("C:/Users/Asus/OneDrive/Documents/folder_python/os_project/processes", 'r') as f:
        for line in f:
            burst1cpu = 0
            burst2cpu = 0
            burstIO = 0

            parts = line.strip().split('\t')
            if not parts[0]:
                continue
            pid = int(parts[0])
            numP += 1
            arrival_time = int(parts[1])
            priority = int(parts[2])

            if parts[3].startswith('CPU'):
                part = parts[3].split(' ')
                i = len(part)
                if (i == 4):  # CPU {R[1], 50, F[1]}
                    burst1cpu = int(part[2].split(',')[0])
                    e = part[1].split('[')
                    resourcenumber = int(e[1].split(']')[0])
                    if resourcenumber not in resourcenumberarr:
                        resourcenumberarr.append(resourcenumber)

                    request.append([resourcenumber, pid, 0, burst1cpu, 1])

                elif (i == 2):
                    burst1cpu = int(part[1].split('}')[0].split('{')[1])

                elif (i == 6):
                    # CPU {20, R[2], 30, F[2], 10}
                    burst1cpu = int(part[1].split('{')[1].split(',')[0])
                    burst1cpu2 = int(part[3].split(',')[0])
                    burst1cpu3 = int(part[5].split('}')[0])
                    resourcenumber = int(part[2].split('[')[1].split(']')[0])
                    if resourcenumber not in resourcenumberarr:
                        resourcenumberarr.append(resourcenumber)
                    request.append([resourcenumber, pid, burst1cpu, burst1cpu2, 1])
                    burst1cpu = burst1cpu + burst1cpu2 + burst1cpu3
                elif i > 6:  # Handling complex case like {R[0], 50, R[1], 50, F[0], F[1]}
                    timeasking = []
                    burst_duration = 0
                    current_burst = 0
                    for token in part:
                        if 'R[' in token:  # Request resource R[x]
                            resourcenumber = int(token.split('[')[1].split(']')[0])
                            if resourcenumber not in resourcenumberarr:
                                resourcenumberarr.append(resourcenumber)
                            duration = int(part[part.index(token) + 1].split(',')[0])
                            timeasking.append([resourcenumber, burst_duration])

                            current_burst += duration  # Update the current burst time
                        elif token.startswith('F['):  # Release resource F[x]
                            resourcenumber = int(token.split('[')[1].split(']')[0])
                            for t in timeasking:
                                if resourcenumber == t[0]:
                                    request.append(
                                        [resourcenumber, pid, t[1], current_burst - t[1], 1])  # Mark the release point
                        else:
                            # This should be the burst time itself
                            try:
                                duration = int(token.split(',')[0])
                                burst_duration += duration
                            except ValueError:
                                pass  # Ignore tokens that don't represent numbers
                    burst1cpu += burst_duration

            x = len(parts)
            if x > 4:
                if parts[4].startswith('IO'):
                    burstIO = int(parts[4].split('{')[1].split('}')[0])

                part = parts[5].strip().split(' ')
                i = len(part)
                if (i == 6):

                    burst2cpu = int(part[1].split('{')[1].split(',')[0])
                    burst2cpu2 = int(part[3].split(',')[0])
                    burst2cpu3 = int(part[5].split('}')[0])
                    resourcenumber = int(part[2].split('[')[1].split(']')[0])
                    if resourcenumber not in resourcenumberarr:
                        resourcenumberarr.append(resourcenumber)
                    request.append([resourcenumber, pid, burst2cpu, burst2cpu2, 2])
                    burst2cpu = burst2cpu + burst2cpu2 + burst2cpu3
                elif (i == 2):
                    burst2cpu = int(part[1].split('}')[0].split('{')[1])
                elif (i == 4):
                    burst2cpu = int(part[2].split(',')[0])
                    e = part[1].split('[')
                    resourcenumber = int(e[1].split(']')[0])
                    if resourcenumber not in resourcenumberarr:
                        resourcenumberarr.append(resourcenumber)
                    request.append([resourcenumber, pid, 0, burst2cpu, 2])
                elif i > 6:  # Handling complex case like {R[0], 50, R[1], 50, F[0], F[1]}

                    timeasking = []
                    burst_duration = 0
                    current_burst = 0
                    for token in part:
                        if 'R[' in token:  # Request resource R[x]
                            resourcenumber = int(token.split('[')[1].split(']')[0])
                            if resourcenumber not in resourcenumberarr:
                                resourcenumberarr.append(resourcenumber)
                            duration = int(part[part.index(token) + 1].split(',')[0])
                            timeasking.append([resourcenumber, burst_duration])

                            current_burst += duration  # Update the current burst time
                        elif token.startswith('F['):  # Release resource F[x]
                            resourcenumber = int(token.split('[')[1].split(']')[0])
                            for t in timeasking:
                                if resourcenumber == t[0]:
                                    request.append(
                                        [resourcenumber, pid, t[1], current_burst - t[1], 2])  # Mark the release point
                        else:
                            # This should be the burst time itself
                            try:
                                duration = int(token.split(',')[0])
                                burst_duration += duration
                            except ValueError:
                                pass  # Ignore tokens that don't represent numbers
                    burst2cpu += burst_duration

            processes.append([pid, arrival_time, priority, burst1cpu, burstIO, burst2cpu])
    numR = len(resourcenumberarr)
    print("processes: ", processes)
    print("number resources= " + str(numR) + ", number process= " + str(numP))
    print("request: ", request)
    print("")




def RR(processes, request, time_quanta, numR, numP):
    resource_holder = [None] * numR  # Tracks which process holds each resource
    waiting_Q = {i: [] for i in range(numR)}  # Processes waiting for each resource
    blocked_processes = set()  # Set of processes that are blocked (waiting)
    realeseTime = []
    t = 0
    gantt = []
    completed = {}
    IOq = []
    notCompleted = []
    avg_wt = []
    avg_tt = []
    sum_wt = 0
    sum_tt = 0
    burst_times = {}
    arrival = {}
    burst1cpu=[]
    burst2cpu=[]
    burst_io = {}
    replayat=[]
    deadlockRequest=[]

    burst1cpuIO={}
    for p in processes:  # [pid,arrival time,priority,burst1cpu,burstIO,burst2cpu]
        pid_p = p[0]
        burst1cpu.append([pid_p,p[3]])
        burst2cpu.append([pid_p, p[5]])
        burst_time = p[3] + p[5]
        burst_io[pid_p] = p[4]
        burst_times[pid_p] = burst_time
        arrival[pid_p] = p[1]
    while processes != [] or IOq :
        readyQ = []
        # Handle processes returning from IO burst
        for io_process in IOq:
            if t >= io_process[6]:  # If current time >= time when process end [6], means it finished
                io_process[4] = 0  # I/O burst is complete
                IOq.remove(io_process)  # Remove from I/O queue
                completed[io_process[0]] = io_process[6]
                io_process[3] = io_process[5]  # Move burst2cpu to burst1cpu to execute again
                burst1cpuIO[io_process[0]]=io_process[5]
                io_process[1] = io_process[6]  # Arrival time now is the time when it ends IOburst
                io_process.pop()  # Remove the last element (timeend)
                for r in request:
                    if io_process[0] == r[1] and r[4] == 2:
                        r[4] = 1
                processes.insert(0,io_process)  # Move to processes queue to be selected in ready queue

        for p in processes[:]:  # processes [pid, arrival time, priority, burst1cpu, burstIO, burst2cpu]
            if p[1] <= t:  # Process has arrived
                readyQ.append(p)

        # If no ready processes, idle
        if readyQ == []:
            gantt.append("idle")
            t += 1
            continue
        else:
            # Sort ready queue by priority (or any other criteria)
            process = sorted(readyQ, key=lambda x: x[2])[0]
            flag=0
            work=False
            request=sorted(request, key=lambda x: x[2])

            for r in request:
                if process[0] == r[1] and r[4] == 1:  # If the process is requesting the resource
                    if r[2] == 0:  # If request type is resource request
                        flag = 1
                        resource_number, pid, TA, TR, BT = r  # Unpack resource request
                        if [resource_number,pid] not in deadlockRequest:
                            deadlockRequest.append([resource_number,pid])

                        result,waiting_Processes,deadlock_processes,normalRequest=deadlock_detection(deadlockRequest, numR, numP)

                        if (result):
                            print("Deadlock processes",deadlock_processes)
                            print("At time ",t)
                            print("Recovery: ")
                            terminated_pid = Recovery(waiting_Processes,deadlock_processes, normalRequest, numR, numP)

                            for b in burst1cpu:
                                if b[0]==terminated_pid:
                                    b1=b[1]
                            for bt in burst2cpu:
                                if bt[0] == terminated_pid:
                                    b2=bt[1]
                            restart_process = [terminated_pid,0,process[2],b1,burst_io[terminated_pid],b2]

                            for i in range(numR):
                                if resource_holder[i] == terminated_pid:
                                    resource_holder[i] = None
                                    for waiting_pid in waiting_Q[i]:
                                        if waiting_pid[0] in blocked_processes:
                                            blocked_processes.remove(waiting_pid[0])
                                            readyQ.append(waiting_pid)
                                            processes.append(waiting_pid)
                                            waiting_Q[i].remove(waiting_pid)
                                for w in waiting_Q[i]:
                                    if terminated_pid==w[0]:
                                        blocked_processes.remove(terminated_pid)
                                        waiting_Q[i].remove(w)

                            for p_terminate in processes:
                                if p_terminate[0]==terminated_pid:
                                    processes.remove(p_terminate)
                                    readyQ.remove(p_terminate)

                            for r_terminate in deadlockRequest:
                                if r_terminate[1]==terminated_pid:
                                    deadlockRequest.remove(r_terminate)
                            process = sorted(readyQ, key=lambda x: x[2])[0]
                            replayat.append([process[0], restart_process])

                            continue
                        # Check if the resource number is within valid range
                        if resource_holder[resource_number] is None:
                            resource_holder[resource_number] = pid
                            work=True
                            if r not in realeseTime:
                                new_release = copy.deepcopy(r)
                                realeseTime.append(new_release)
                            break

                        elif resource_holder[resource_number] == process[0]:
                            work=True

                        else:

                            waiting_Q[resource_number].append(process)
                            blocked_processes.add(pid)
                            processes.remove(process)
                            readyQ.remove(process)
                            process=sorted(readyQ, key=lambda x: x[2])[0]
                            continue

                    else:
                        if process[0] in burst1cpuIO.keys():
                            allB=burst1cpuIO[process[0]]
                        else:
                            for b in burst1cpu:
                                if process[0]==b[0]:
                                    allB=b[1]

                        comp=r[2]-(allB-process[3])
                        if (comp <= time_quanta):
                            rem = allB - r[2]
                            pnew = [process[0], process[1], process[2], rem, process[4], process[5]]

                            notCompleted.append(pnew)
                            process[3] = comp
                            r[2] = 0
                            work = True
                        else:
                            work=True
            if (flag==0):# if the process doesnt request a resource
                work=True
            if(work):
                #print(" working pid and t ",process,t,waiting_Q)
                gantt.append(process[0])
                processes.remove(process)
                rem_burst = process[3]

                if rem_burst <= time_quanta:

                    t += rem_burst
                    for rt in realeseTime:
                        if process[0] == rt[1]:  # Process holding resource
                            rt[3] -= rem_burst

                    x = 0
                    rem = 0
                    if process[4] == 0:  # No IO burst
                        for i in notCompleted:
                            if process[0] == i[0]:
                                x = 1
                                rem = i[3]
                                notCompleted.remove(i)
                        if (x == 0):
                            ct = t
                            pid = process[0]
                            arrival_time = arrival[pid]
                            burst_time = burst_times[pid]
                            ioT = burst_io[pid]
                            tt = ct - arrival_time
                            avg_tt.append(tt)
                            wt = tt - burst_time-ioT
                            avg_wt.append(wt)
                            completed[process[0]] = [ct, tt, wt]
                            for resource_number in range(numR):
                                if resource_holder[resource_number] is not None:
                                    if process[0] == resource_holder[resource_number]:
                                        for rr in realeseTime:
                                            if rr[1]== process[0]:
                                                if rr[3]==0:
                                                    pass
                                                else:
                                                    resource_holder[resource_number]=None
                                                    for waiting_pid in waiting_Q[resource_number]:
                                                        if waiting_pid[0] in blocked_processes:
                                                            blocked_processes.remove(waiting_pid[0])
                                                            processes.append(waiting_pid)
                                                            waiting_Q[resource_number].remove(waiting_pid)

                            for e in replayat:
                                if process[0] == e[0]:
                                    restart=e[1]
                                    restart[1]=t

                                    processes.append(restart)

                        else:
                            process[3] = rem
                            processes.append(process)

                    else:
                        timeend = process[4] + t
                        io_process_end = process + [timeend]
                        IOq.append(io_process_end)
                else:
                    t += time_quanta
                    for r in realeseTime:
                        if process[0] == r[1]:  # Process holding resource
                            r[3] -= time_quanta
                    process[3] -= time_quanta

                    process[1] = t
                    processes.append(process)

        # Handle releasing of resources
        for resource_number in range(numR):
            if resource_holder[resource_number] is not None:  # Resource held by a process
                for r in realeseTime:
                    if r[3] <= 0:  # If release time is 0
                        pid = resource_holder[resource_number]
                        resource_holder[resource_number] = None  # Release the resource
                        realeseTime.remove(r)

                        deadlockRequest.remove([resource_number,pid])#remove the resource request after releasing it ,so it doesnt enter the deadlock detection cycle
                        # Unblock processes waiting for the resource
                        for waiting_pid in waiting_Q[resource_number]:
                            if waiting_pid[0] in blocked_processes:
                                blocked_processes.remove(waiting_pid[0])
                                processes.append(waiting_pid)
                                waiting_Q[resource_number].remove(waiting_pid)


    print("\nGantt chart:", gantt)


    print("\nCompleted processes:")
    # Labels for the values
    # Labels for the values
    labels = ["Finished at", "Turnaround Time", "Waiting Time"]

    # Iterating through the dictionary
    for key, values in completed.items():
        print(f"{key}:")
        if isinstance(values, list) and len(values) == len(labels):
            for label, value in zip(labels, values):
                print(f"  {label}: {value}")
        else:
            print("  - Invalid data format")

    for value in avg_wt:
        sum_wt = value + sum_wt
    for value in avg_tt:
        sum_tt = value + sum_tt

    print("\nAverage waiting time: ", sum_wt / numP)
    print("Average turnaround time: ", sum_tt / numP)

def deadlock_detection(requests, num_resources, num_processes):
    # Initialize the allocation and waiting lists
    resource_holder = [None] * num_resources  # Tracks which process holds each resource
    waiting_processes = {i: [] for i in range(num_resources)}  # Processes waiting for each resource
    blocked_processes = set()  # Set of processes that are blocked (waiting)
    deadlock_processes=[]
    # Process each request
    for request in requests:
        resource_number, pid = request  # Unpacking: resource_number, pid

        # If the resource is not held by any process, allocate it to the requesting process
        if resource_holder[resource_number] is None:
            resource_holder[resource_number] = pid
        else:
            # If the resource is held by another process, add this process to the waiting list
            waiting_processes[resource_number].append(pid)
            blocked_processes.add(pid)
    result=False
    # Detecting deadlock
    for num in range(num_resources):
        if waiting_processes[num]:
            holding_pid = resource_holder[num]  # Process holding the resource

            # If the resource is held, check if any process in the waiting list is blocked
            for waiting_pid in waiting_processes[num]:
                # Check if the process that is holding the resource is blocked
                if holding_pid in blocked_processes:
                    if holding_pid not in deadlock_processes:
                        result=True
                        deadlock_processes.append(holding_pid)
                    print(f"Deadlock detected! Process {waiting_pid} is waiting for resource {num} held by blocked process {holding_pid}")


    return result,blocked_processes,deadlock_processes,requests


def Recovery(blocked_processes,deadlock_processes,request,numR,numP):
    process_to_terminate = list(deadlock_processes)[0]  # For simplicity, choose the first one
    print(f"Terminating process {process_to_terminate} to break the deadlock.")
    # Remove terminated process from blocked processes and release its held resources
    blocked_processes.remove(process_to_terminate)
    deadlock_processes.remove(process_to_terminate)
    for r in request:
        if process_to_terminate== r[1]:
            request.remove(r)
    return process_to_terminate

def main():
    readfile()
    time_qaunta=10
    RR(processes, request, time_qaunta, numR, numP)
    print("---------------------------------------------------------------------")



if __name__ == "__main__":
    main()