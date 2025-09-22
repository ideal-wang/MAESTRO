from datetime import datetime

from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
from config.root_base import *


class MeteorologicalRetrieveInput(BaseModel):
    retrieve_data_type: str = Field(
        description="The type of meteorological data to retrieve. This could be 'temperature', 'precipitation', 'wind intensity', 'typhoon' etc."
    )
    location4retrieve: str = Field(
        description="The geographic location for which the meteorological data is to be retrieved. It could be a city name, coordinates (latitude, longitude), or any location identifier."
    )
    time4retrieve: str = Field(
        default=datetime.now().strftime("%Y%m%d%H"),  # Default value is the current time
        description="The specific time or time range for which the meteorological data is needed. It could be a timestamp or a date range (e.g., '2025-02-07' or '2025-02-01 to 2025-02-07')."
    )


class MeteorologicalRetrieveTool(BaseTool):
    name: str = "meteorological_retrieve_tool"
    description: str = (
        "A tool for retrieving specific meteorological data based on input parameters like data type, location, and time. "
        "It allows users to fetch meteorological data such as temperature, precipitation, or wind intensity for a given location and time."
    )
    args_schema: Type[BaseModel] = MeteorologicalRetrieveInput

    def _run(self, retrieve_data_type: str, location4retrieve: str, time4retrieve: str):
        return mainMeteorologicalRetrieve(retrieve_data_type, location4retrieve, time4retrieve)

    def _arun(self, retrieve_data_type: str, location4retrieve: str, time4retrieve: str):
        raise NotImplementedError("meteorological_retrieve_tool does not support async")


def mainMeteorologicalRetrieve(retrieve_data_type, location4retrieve, time4retrieve):
    try:
        print(
            f'retrieve the needed data: type-{retrieve_data_type}, location-{location4retrieve}, time-{time4retrieve}')
        print('------------------')
    except Exception as e:
        return f"The meteorological retrieve task has failed, and meets the exception{e}"

    return f"The meteorological retrieve task has completed."

if __name__ == '__main__':
    # Initialize input parameters
    retrieve_data_type = 'precipitation'
    location = 'whole Zhejiang province'
    time4retrieve = '2022091308'

    meteorological_retrieve_tool = MeteorologicalRetrieveTool()

    # Call the tool
    retrieve_result = meteorological_retrieve_tool._run(retrieve_data_type, location, time4retrieve)
    #
    # # Print the result
    # print(forecast_result)