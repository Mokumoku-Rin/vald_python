import grpc
from vald.v1.vald import insert_pb2_grpc
from vald.v1.vald import search_pb2_grpc
from vald.v1.vald import remove_pb2_grpc
from vald.v1.agent.core import agent_pb2_grpc
from vald.v1.payload import payload_pb2
import numpy as np


class ValdClient:
    def __init__(self, ip: str, port: str):
        # create a channel by passing "{host}:{port}"
        self.channel = grpc.insecure_channel(f"{ip}:{port}")

        # create stubs for calling RPCs
        self.I_STUB = insert_pb2_grpc.InsertStub(self.channel)
        self.S_STUB = search_pb2_grpc.SearchStub(self.channel)
        self.R_STUB = remove_pb2_grpc.RemoveStub(self.channel)

    def __del__(self):
        # close channel
        self.channel.close()

    def insert(self, data_id: str, data: np.ndarray):
        # call RPCs: Insert
        vec = payload_pb2.Object.Vector(id=data_id, vector=data)
        icfg = payload_pb2.Insert.Config(skip_strict_exist_check=True)
        self.I_STUB.Insert(payload_pb2.Insert.Request(vector=vec, config=icfg))

    def search(self, data: np.ndarray, result_num: int):
        # call RPCs: Search
        # num: number of results
        # timeout: 3 seconds
        scfg = payload_pb2.Search.Config(
            num=result_num, radius=-1.0, epsilon=0.01, timeout=3000000000)
        pp = payload_pb2.Search.Request(vector=data, config=scfg)
        try:
            res = self.S_STUB.Search(pp)
        except grpc._channel._InactiveRpcError as e:
            print("ERROR: check shape of your data")
            raise e
        return res

    def delete(self, data_id: str):
        # call RPCs: Remove
        rcfg = payload_pb2.Remove.Config(skip_strict_exist_check=True)
        rid = payload_pb2.Object.ID(id=data_id)
        self.R_STUB.Remove(payload_pb2.Remove.Request(id=rid, config=rcfg))

    def create_index(self, pool_size: int):
        request = payload_pb2.Control().CreateIndexRequest(pool_size=pool_size)
        agent_pb2_grpc.AgentStub(self.channel).CreateAndSaveIndex(request)
