from datetime import datetime
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
import pickle
from config.root_base import *

class StoreSubtaskInput(BaseModel):
    subtask_queue: list = Field(description="A list of subtask for the following work")

class StoreSubtaskTool(BaseTool):
    name: str = "Store_subtask_tool"
    description: str = ("Useful to store subtask queue which is base on the observation log updates into the system file,"
                        "only when the retrieve log tool has specific subtask results works.")
    args_schema: Type[BaseModel] = StoreSubtaskInput

    def _run(self, subtask_queue: list):
        print(f'store the subtask: {subtask_queue}')
        set_global_state(subtask_queue)
        return 0

    def _arun(self, subtask_queue: list):
        raise NotImplementedError("initiate_emergency_response_tool does not support async")

def set_global_state(subtask_queue):
    with open(SYSTEM_FILE_PATH, 'rb') as f:
        system_file = pickle.load(f)
    for subtask in subtask_queue:
        origin_subtask_queue = system_file['subtask_queue']
        flag = True
        for s_q in origin_subtask_queue:
            if s_q['subtask'] == subtask:
                flag = False
        if flag:
            s = {'subtask': subtask, 'status': 'pending'}
            system_file['subtask_queue'].append(s)
    print(system_file)
    with open(SYSTEM_FILE_PATH, 'wb') as f:
        pickle.dump(system_file, f)
    # print(system_file)