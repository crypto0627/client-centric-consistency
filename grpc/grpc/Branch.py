import grpc
from concurrent import futures

import branch_pb2
import branch_pb2_grpc
PORT_BASE = 50000

class Branch(branch_pb2_grpc.BranchServicer):

    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # iterate the processID of the branches

        # TODO: students are expected to store the processID of the branches
        pass

    # Received from Client delivery
    def MsgDelivery(self, request, context):
        # handle received messages from the Client and propagate them to the branches
        return self.process(request, do_propagate=True)

    # Received from Branch propagation
    def MsgPropagation(self, request, context):
        # Update the balance of the current branch with the received money from the other branch
        return self.process(request, do_propagate=False)

    def process(self, request, do_propagate):
        # check if the parameters are all valid
        if request.money < 0:
            # money has to be positive or 0
            result = "fail"
        elif request.interface == "withdraw" and self.balance < request.money:
            # cannot withdraw more money than the balance
            result = "fail"
        else:
            result = "success"
            if request.interface == "query":
                pass
            else:
                if request.interface == "withdraw":
                    self.balance -= request.money
                elif request.interface == "deposit":
                    self.balance += request.money
                if do_propagate:
                    self.propagate(request)
        return branch_pb2.MsgResponse(interface=request.interface, result=result, money=self.balance)

    def propagate(self, request):
        for stub in self.stubList:
            stub.MsgPropagation(branch_pb2.MsgRequest(id=request.id, interface=request.interface, money=request.money))
    
    def createStub(self):
        for branch in self.branches:
            # only create for the branch that is not the current branch
            if branch.id != self.id:
                port = str(PORT_BASE + branch.id)
                channel = grpc.insecure_channel("localhost:" + port)
                self.stubList.append(branch_pb2_grpc.BranchStub(channel))

    def start(self):
        # create branch stub
        self.createStub()
        # start current branch process
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        branch_pb2_grpc.add_BranchServicer_to_server(self, server)
        port = str(PORT_BASE + self.id)
        server.add_insecure_port("[::]:" + port)
        server.start()
        server.wait_for_termination()