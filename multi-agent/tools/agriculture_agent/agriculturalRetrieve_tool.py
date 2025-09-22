from datetime import datetime

from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
from config.root_base import *

class AgriculturalDisasterRetrieveInput(BaseModel):
    retrieve_data_type: str = Field(
        description="The type of agricultural disaster data to retrieve. This could be 'crop damage', 'drought impact', 'flood damage', etc."
    )
    location4retrieve: str = Field(
        description="The geographic location for which the agricultural disaster data is to be retrieved. It could be a farm name, city name, coordinates (latitude, longitude), or any location identifier."
    )
    time4retrieve: str = Field(
        default=datetime.now().strftime("%Y%m%d%H"),  # Default value is the current time
        description="The specific time or time range for which the agricultural disaster data is needed. It could be a timestamp or a date range (e.g., '2025-02-07' or '2025-02-01 to 2025-02-07')."
    )





class AgriculturalDisasterRetrieveTool(BaseTool):
    name: str = "agricultural_disaster_retrieve_tool"
    description: str = (
        "A tool for retrieving agricultural disaster-related data, such as crop damage due to natural disasters, "
        "drought effects, flood impacts, etc. It takes parameters like data type, location, and time range to provide "
        "detailed information about the agricultural impact of disasters."
    )
    args_schema: Type[BaseModel] = AgriculturalDisasterRetrieveInput

    def _run(self, retrieve_data_type: str, location4retrieve: str, time4retrieve: str):
        return mainAgriculturalDisasterRetrieve(retrieve_data_type, location4retrieve, time4retrieve)

    def _arun(self, retrieve_data_type: str, location4retrieve: str, time4retrieve: str):
        raise NotImplementedError("agricultural_disaster_retrieve_tool does not support async")

def mainAgriculturalDisasterRetrieve(retrieve_data_type, location4retrieve, time4retrieve):
    try:
        print(f"Retrieving the needed agricultural disaster data: type-{retrieve_data_type}, location-{location4retrieve}, time-{time4retrieve}")
        print('------------------')

    except Exception as e:
        return f"The agricultural disaster retrieve task has failed, and meets the exception: {e}"

    return "The agricultural disaster retrieve task has completed."

if __name__ == '__main__':
    # Initialize input parameters for agricultural disaster data
    retrieve_data_type = 'flood damage crops'  # Example: data type related to agricultural disaster (e.g., 'crop damage', 'flood damage')
    location = 'Ningbo city'  # Location affected by the disaster
    time4retrieve = '2022091308'  # The time or timestamp for the disaster data retrieval

    agricultural_disaster_retrieve_tool = AgriculturalDisasterRetrieveTool()

    # Call the tool to retrieve the data
    retrieve_result = agricultural_disaster_retrieve_tool._run(retrieve_data_type, location, time4retrieve)

    # Print the result
    print(retrieve_result)
