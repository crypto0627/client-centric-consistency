import grpc
import branch_pb2
import branch_pb2_grpc
import time
PORT_BASE = 50000
class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub = None

    # TODO: students are expected to create the Customer stub
    def createStub(self):
        port = str(PORT_BASE + self.id)
        channel = grpc.insecure_channel("localhost:" + port)
        self.stub = branch_pb2_grpc.BranchStub(channel)

    # TODO: students are expected to send out the events to the Bank
    def executeEvents(self):
        for idx, event in enumerate(self.events):
            print("Customer " + str(self.id) + ": Processing event " + str(idx + 1) + " / " + str(len(self.events)))
            
            # fill fake money for query interface
            if "money" not in event:
                event["money"] = 0

            # Send request to Branches
            response = self.stub.MsgDelivery(
                branch_pb2.MsgRequest(id=event["id"], interface=event["interface"], money=event["money"])
            )

            result = {"interface": response.interface, "result": response.result}
            # Only query has money result to be logged to file
            if response.interface == "query":
                result["balance"] = response.money

            self.recvMsg.append(result)
            # Sleep 1 seconds for each event for branch propagation
            time.sleep(1)