import os
import numpy as np
from pydantic import BaseModel, Field
from typing import Type
from langchain.tools import BaseTool

from config.root_base import *  # Ensure this is defined in your config


# Define the MaterialSchedulingInput class to accept the predicted scheduling time
class MaterialDispatchInput(BaseModel):
    time4schedule: str = Field(
        description="Time for planning the material dispatch schedule, format as YYYYMMDDHH"
    )
    schedule_duration: str = Field(description="Duration for material dispatch.(e.g., '24h')")

# Define the MaterialSchedulingTool class inheriting from BaseTool
class MaterialDispatchTool(BaseTool):
    name: str = "material_scheduling_tool"
    description: str = (
        "Optimize the dispatch schedule for materials required during disaster response based on the predicted time. "
        "Paths for material inventory and demand data are automatically derived."
    )
    args_schema: Type[BaseModel] = MaterialDispatchInput

    def _run(self, time4schedule: str, schedule_duration: str):
        return mainMaterialDispatch(time4schedule, schedule_duration)

    def _arun(self, time4schedule: str, schedule_duration: str):
        raise NotImplementedError("material_scheduling_tool does not support async operations.")


def mainMaterialDispatch(time4schedule: str, schedule_duration: str):
    print(f"Optimizing material dispatch schedule at {time4schedule} for the duration {schedule_duration}")
    print("-------------------")
    try:
        print("Loading material inventory data...")
        print("-------------------")
        # Simulate data loading; in practice, load actual inventory data here.
        material_inventory = np.random.rand(10) * 100  # Dummy inventory data

        print("Performing scheduling optimization...")
        print("-------------------")
        # Simulate optimization logic; here we create a dummy scheduling result.
        # For example, create a matrix indicating scheduled material dispatch quantities.
        scheduling_result = np.random.rand(5, 5)

        print("Storing the material scheduling result...")
        print("-------------------")
        # disaster_name = 'Lekima'
        # schedule_path = f"{material_dispatch_root}/{disaster_name}-{time4schedule}_material_dispatch.npy"
        # os.makedirs(os.path.dirname(schedule_path), exist_ok=True)
        # np.save(schedule_path, scheduling_result)
    except Exception as e:
        return f"Encountered exception {e} while optimizing material scheduling."

    return f"The material dispatch schedule for {time4schedule} has been successfully generated."


# Example usage
if __name__ == "__main__":
    current_time = "2024092312"  # Example predicted scheduling time
    material_tool = MaterialDispatchTool()
    schedule_result = material_tool._run(current_time)
    print(schedule_result)

