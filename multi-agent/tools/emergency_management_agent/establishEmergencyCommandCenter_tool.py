from datetime import datetime
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type, List
import pickle
from config.root_base import *


# define EstablishEmergencyCommandCenterTool class
class EstablishEmergencyCommandCenterTool(BaseTool):
    name: str = "establish_emergency_command_center_tool"
    description: str = ("Useful to establish an emergency command center based on alert information and consult "
                        "meteorological bureau, hydrological department, and natural resource department for emergency "
                        "response suggestions")

    def _run(self):
        set_global_state()
        # consult_content = {
        #     "meteorological_bureau": "please give me the meteorological emergency response suggestion.",
        #     "hydrological_department": "please give me the hydrological emergency response suggestion.",
        #     "natural_resource_department": "please give me the natural resource emergency response suggestion."
        # }
        return (f'Emergency command center has been established and consult meteorological bureau, hydrological '
                f'department and natural resource department for emergency response suggestions at the same time.')

    def _arun(self, alert_info: dict):
        raise NotImplementedError("establish_emergency_command_center_tool does not support async")


def set_global_state():
    with open(SYSTEM_FILE_PATH, 'rb') as f:
        system_file = pickle.load(f)
    subtask = [{'subtask': 'meteorological emergency response suggestion', 'status': 'pending'},
               {'subtask': 'hydrological emergency response suggestion', 'status': 'pending'},
               {'subtask': 'natural resource emergency response suggestion', 'status': 'pending'}]
    system_file['subtask_queue'].extend(subtask)
    system_file['emergency_command_center_status'] = 'establish'
    # print(system_file)
    with open(SYSTEM_FILE_PATH, 'wb') as f:
        pickle.dump(system_file, f)


# 示例使用
if __name__ == "__main__":
    # 创建工具实例
    emergency_command_center_tool = EstablishEmergencyCommandCenterTool()

    # 运行工具并获取指挥中心信息
    command_center_info = emergency_command_center_tool._run()

    # 打印结果
    print(command_center_info)
