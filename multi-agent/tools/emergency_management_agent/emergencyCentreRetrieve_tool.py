from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
from config.root_base import *

from datetime import datetime

class EmergencyCenterRetrieveInput(BaseModel):
    retrieve_data_type: str = Field(
        description="The type of emergency data to retrieve. This could be 'affected people', 'personnel transfer', 'material supply', 'shelter status', etc."
    )
    location4retrieve: str = Field(
        default="whole province",  # Default value is "whole province"
        description="The geographic location for which the emergency data is to be retrieved. It could be a city name, disaster zone, coordinates (latitude, longitude), or any location identifier."
    )
    time4retrieve: str = Field(
        description="The specific time or time range for which the emergency data is needed. It could be a timestamp or a date range (e.g., '2025-02-07' or '2025-02-01 to 2025-02-07')."
    )

class EmergencyCenterRetrieveTool(BaseTool):
    name: str = "emergency_center_retrieve_tool"
    description: str = (
        "A tool for retrieving specific emergency-related data based on input parameters like data type, location, and time. "
        "This could include information on affected people, personnel transfers, material supplies, shelter statuses, etc. "
        "It is useful for disaster response teams and emergency management."
    )
    args_schema: Type[BaseModel] = EmergencyCenterRetrieveInput

    def _run(self, retrieve_data_type: str, location4retrieve: str, time4retrieve: str):
        # if time4retrieve is None:
        #     time4retrieve = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Use current time if no time is provided

        # Here you would have the actual logic to retrieve data based on these parameters
        print(f"Retrieving emergency data... Type: {retrieve_data_type}, Location: {location4retrieve}, Time: {time4retrieve}")
        return mainEmergencyCenterRetrieve(retrieve_data_type, location4retrieve, time4retrieve)

    def _arun(self, retrieve_data_type: str, location4retrieve: str, time4retrieve: str):
        raise NotImplementedError("emergency_center_retrieve_tool does not support async")


def mainEmergencyCenterRetrieve(retrieve_data_type, location4retrieve, time4retrieve):
    try:
        # print(f"Retrieving the emergency data: type-{retrieve_data_type}, location-{location4retrieve}, time-{time4retrieve}")
        print('------------------')

        # Simulate some disaster data retrieval process
        # For example, retrieving data related to affected people, shelters, or supplies
        if retrieve_data_type == "affected people":
            print("Retrieving data about affected people...")
            print('------------------')
        elif retrieve_data_type == "personnel transfer":
            print("Retrieving data on personnel transfer operations...")
            print('------------------')
        elif retrieve_data_type == "material supply":
            print("Retrieving data about material supplies...")
            print('------------------')
        elif retrieve_data_type == "shelter status":
            print("Retrieving data about shelter statuses...")
            print('------------------')
        else:
            print(f"Retrieving data about {retrieve_data_type}.")
            print('------------------')



    except Exception as e:
        return f"The emergency center retrieve task has failed due to an exception: {e}"
    # Simulating the actual data retrieval process
    print(f"Data for {retrieve_data_type} in {location4retrieve} at {time4retrieve} retrieved successfully.")
    print('------------------')
    return "The emergency center retrieval task has completed."

if __name__ == '__main__':
    # Initialize input parameters for emergency center data retrieval
    retrieve_data_type = 'affected people'  # Example data type related to emergency (e.g., 'affected people', 'material supply', etc.)
    location = 'Ningbo city'  # Location affected by the disaster
    time4retrieve = '2022091308'  # The time or timestamp for the emergency data retrieval

    emergency_center_retrieve_tool = EmergencyCenterRetrieveTool()

    # Call the tool to retrieve the data
    retrieve_result = emergency_center_retrieve_tool._run(retrieve_data_type, time4retrieve, location)

    # Print the result
    print(retrieve_result)
