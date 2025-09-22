from datetime import datetime

from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
from config.root_base import *


class HydrologicalRetrieveInput(BaseModel):
    retrieve_data_type: str = Field(
        description="The type of hydrological data to retrieve. This could be 'reservoir storage', 'river flow', 'water level', etc."
    )
    location4retrieve: str = Field(
        description="The geographic location for which the hydrological data is to be retrieved. It could be a city name, coordinates (latitude, longitude), or any location identifier."
    )
    time4retrieve: str = Field(
        default=datetime.now().strftime("%Y%m%d%H"),  # Default value is the current time
        description="The specific time or time range for which the hydrological data is needed. It could be a timestamp or a date range (e.g., '2025-02-07' or '2025-02-01 to 2025-02-07')."
    )


class HydrologicalRetrieveTool(BaseTool):
    name: str = "hydrological_retrieve_tool"
    description: str = (
        "A tool for retrieving specific hydrological data based on input parameters like data type, location, and time. "
        "It supports various hydrological data such as reservoir storage, water levels, river flows, etc., to assist in "
        "flood prediction, water management, and related tasks."
    )
    args_schema: Type[BaseModel] = HydrologicalRetrieveInput

    def _run(self, retrieve_data_type: str, location4retrieve: str, time4retrieve: str):
        return mainHydrologicalRetrieve(retrieve_data_type, location4retrieve, time4retrieve)

    def _arun(self, retrieve_data_type: str, location4retrieve: str, time4retrieve: str):
        raise NotImplementedError("hydrological_retrieve_tool does not support async")

def mainHydrologicalRetrieve(retrieve_data_type, location4retrieve, time4retrieve):
    try:
        print(
            f'retrieve the needed data: type-{retrieve_data_type}, location-{location4retrieve}, time-{time4retrieve}')
        print('------------------')
    except Exception as e:
        return f"The hydrological retrieve task has failed, and meets the exception{e}"

    return f"The hydrological retrieve task has completed."

if __name__ == '__main__':
    # Initialize input parameters
    retrieve_data_type = 'water level'
    location = 'the Qiantang River'
    time4retrieve = '2022091308'

    hydrological_retrieve_tool = HydrologicalRetrieveTool()

    # Call the tool
    retrieve_result = hydrological_retrieve_tool._run(retrieve_data_type, location, time4retrieve)
    #
    # # Print the result
    # print(forecast_result)