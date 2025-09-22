import pickle
from collections import deque

from langchain.tools import BaseTool

from config.root_base import *

# define ActivateEmergencyResponseTool class
class ActivateEmergencyResponseTool(BaseTool):
    name: str = "activate_emergency_response_tool"
    description: str = ("Useful to activate the emergency response when the emergency response level is not equal to "
                        "zero and adjust the monitoring frequency base on the emergency response level.")

    def _run(self):
        return mainActivateEmergencyresponse()

    def _arun(self):
        raise NotImplementedError("activate_emergency_response_tool does not support async")

def mainActivateEmergencyresponse():
    print('activate the emergency response status')
    level = set_global_state()
    if level == 0:
        return f"The emergency response level is zero. No emergency response is required."
    return f"The emergency response is acitvated now, and the current emergency response level is {level}"

def set_global_state():
    with open(SYSTEM_FILE_PATH, 'rb') as f:
        system_file = pickle.load(f)
    emergency_response_level = system_file['emergency_response_level']
    # Update the global state based on the emergency_response_level
    if emergency_response_level == 4:
        system_file['monitor_frequency'] = '12h'
        system_file['emergency_response_status'] = 'START'
    elif emergency_response_level == 3:
        system_file['monitor_frequency'] = '8h'
        system_file['emergency_response_status'] = 'START'
    elif emergency_response_level == 2:
        system_file['monitor_frequency'] = '6h'
        system_file['emergency_response_status'] = 'START'
    elif emergency_response_level == 1:
        system_file['monitor_frequency'] = '3h'
        system_file['emergency_response_status'] = 'START'

    if emergency_response_level == 1 or emergency_response_level == 2:
        system_file['subtask_queue'] = deque([{'subtask': 'affected people relocation', 'status': 'pending'},])
                                              # {'subtask': 'material dispatch', 'status': 'pending'}])
    with open(SYSTEM_FILE_PATH, 'wb') as f:
        pickle.dump(system_file, f)
    return emergency_response_level
# 示例使用
if __name__ == "__main__":

    # 创建工具实例
    activate_response_tool = ActivateEmergencyResponseTool()

    # 运行工具并获取应急响应信息
    response_info = activate_response_tool._run()

    # 打印结果
    print(response_info)
