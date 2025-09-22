import json
import os
from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from config.root_base import *  # Ensure paths are correctly configured in your config

# Define the input schema for the AgriculturalRecoveryTool
class AgriculturalRecoveryInput(BaseModel):
    time4recovery: str = Field(
        description="The timestamp for agricultural recovery plan formulation, format in YYYYMMDDHH"
    )
    location4recovery: str = Field(
        default="whole province",  # Default value for location is "whole province"
        description="The geographic location for the agricultural recovery plan. It could be a city, region, or specific coordinates."
    )

# Define the AgriculturalRecoveryTool class
class AgriculturalRecoveryTool(BaseTool):
    name: str = "agricultural_recovery_tool"
    description: str = "Useful to schedule agricultural recovery work on agricultural infrastructure and resources."
    args_schema: Type[BaseModel] = AgriculturalRecoveryInput

    def _run(self, time4recovery: str, location4recovery: str):
        # Logic to perform scheduling based on current agricultural disaster damage and resources
        return mainAgriculturalRecovery(time4recovery, location4recovery)

    def _arun(self, time4recovery: str, location4recovery: str):
        raise NotImplementedError("agricultural_recovery_tool does not support async")


# Function to store the agricultural recovery plan as a JSON file
def store_recovery(recovery_schedule: dict, time4recovery: str):
    disaster_name = 'Lekima'  # Example disaster name (can be dynamically assigned)
    recovery_path = f'{rural_recover_root}/{disaster_name}-{time4recovery}_rural.json'
    os.makedirs(os.path.dirname(recovery_path), exist_ok=True)
    with open(recovery_path, 'w') as json_file:
        json.dump(recovery_schedule, json_file, indent=4)

# Main function to create the agricultural recovery plan
def mainAgriculturalRecovery(time4recovery: str, location4recovery: str):
    print(f"Starting agricultural recovery scheduling for {location4recovery} at {time4recovery}")
    print('-------------------')

    # Example agricultural project status and resources
    project_status = {
        'rice_fields': {'status': 'damaged', 'severity': 0.8},
        'wheat_fields': {'status': 'operational', 'severity': 0.2},
        'irrigation_systems': {'status': 'damaged', 'severity': 0.6}
    }

    resource_status = {
        'workers': 100,
        'equipment': {'tractors': 5, 'irrigation_pumps': 3},
        'materials': {'seeds': 1000, 'fertilizer': 500}
    }

    # Sorting the projects based on severity (highest first)
    sorted_projects = sorted(project_status.items(), key=lambda x: x[1]['severity'], reverse=True)

    recovery_plan = []
    for project, status in sorted_projects:
        if status['status'] == 'damaged':
            required_workers = int(status['severity'] * 20)  # Hypothetical calculation of worker requirements
            if resource_status['workers'] >= required_workers:
                recovery_plan.append(f"Restore {project} with {required_workers} workers.")
                resource_status['workers'] -= required_workers
            else:
                recovery_plan.append(f"Not enough workers to restore {project}. Assigning available resources.")
                return f"Not enough workers to restore {project}. Assigning available resources."

    recovery_res = {
        'currentTime': time4recovery,
        'recovery_plan': recovery_plan,
        'remaining_resources': resource_status
    }

    # Store the recovery plan
    store_recovery(recovery_res, time4recovery)

    return f"Agricultural recovery schedule for {time4recovery} has been completed."


# Example usage:
if __name__ == "__main__":
    agricultural_recovery_tool = AgriculturalRecoveryTool()

    # Call the tool with parameters
    res = agricultural_recovery_tool._run('2022091320', 'whole province')  # Example time and location
    print(res)
