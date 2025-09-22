import pickle
from collections import deque

from langchain.tools import BaseTool

from config.root_base import *

# define TerminateEmergencyResponseTool class
class TerminateEmergencyResponseTool(BaseTool):
    name: str = "terminate_emergency_response_tool"
    description: str = "Useful to terminate the emergency response and adjust the monitoring frequency."

    def _run(self):
        set_global_state()
        return f"The emergency response is terminated now!"

    def _arun(self, alert_info: dict):
        raise NotImplementedError("terminate_emergency_response_tool does not support async")

def set_global_state():
    with open(SYSTEM_FILE_PATH, 'rb') as f:
        system_file = pickle.load(f)
    system_file['emergency_response_status'] = 'END'
    system_file['subtask_queue'] = deque([{'subtask': 'hydraulic repair', 'status': 'pending'},
                                          {'subtask': 'agricultural recover', 'status': 'pending'}])
    print(system_file)
    with open(SYSTEM_FILE_PATH, 'wb') as f:
        pickle.dump(system_file, f)

# 示例使用
if __name__ == "__main__":

    # 创建工具实例
    terminate_response_tool = TerminateEmergencyResponseTool()

    # 运行工具并获取应急响应信息
    response_info = terminate_response_tool._run()

    # 打印结果
    print(response_info)
