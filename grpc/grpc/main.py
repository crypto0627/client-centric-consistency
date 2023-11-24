import grpc
import time
import json
import multiprocessing

from Branch import Branch
from Customer import Customer

# read input json file and load all processes
json_file = "input.json"
with open(json_file, 'r') as f:
    processes = json.load(f)

# handle branches
## create branch with given id and initial balance
branch_list = []
for process in processes:
    if process["type"] == "branch":
        branch = Branch(process["id"], process["balance"], branch_list)
        branch_list.append(branch)
## start all processes
branch_process_list = []
for branch in branch_list:
    p = multiprocessing.Process(target=branch.start, )
    branch_process_list.append(p)
    p.start()

# wait for branch to get online
print("Waiting for branches to get online", end="", flush=True)
for i in range(5):
    time.sleep(1)
    print(".", end="", flush=True)
print()

# handle customers and execute all events
# write result to output file
with open("output.txt", "w") as f:
    for process in processes:
        if process["type"] == "customer":
            customer = Customer(process["id"], process["events"])
            customer.createStub()
            customer.executeEvents()
            result = {"id": customer.id, "recv": customer.recvMsg}
            f.write(str(result) + "\n")
            f.flush()

# terminate all branches
for branch_process in branch_process_list:
    branch_process.terminate()