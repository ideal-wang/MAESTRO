from datetime import datetime
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
from config.root_base import *


class NaturalResourceRetrieveInput(BaseModel):
    retrieve_data_type: str = Field(
        description="The type of natural resource disaster data to retrieve. This could be 'natural resource data', 'geological disaster', 'marine disaster', 'earthquake', 'tsunami', 'storm surge', etc."
    )
    location4retrieve: str = Field(
        description="The geographic location for which the natural disaster data is to be retrieved. It could be a city, coordinates (latitude, longitude), or a specific region."
    )
    time4retrieve: str = Field(
        default=datetime.now().strftime("%Y%m%d%H"),  # Default value is the current time
        description="The specific time or time range for which the natural resource disaster data is needed. It could be a timestamp or a date range (e.g., '2025-02-07' or '2025-02-01 to 2025-02-07')."
    )

class NaturalResourceRetrieveTool(BaseTool):
    name: str = "natural_resource_retrieve_tool"
    description: str = (
        "A tool for retrieving natural resource disaster-related data, such as geological disasters (earthquakes, landslides) "
        "and marine disasters (tsunami, storm surge). The tool takes parameters like data type, location, and time range to "
        "provide detailed information about the impact and conditions related to these disasters."
    )
    args_schema: Type[BaseModel] = NaturalResourceRetrieveInput

    def _run(self, retrieve_data_type: str, location4retrieve: str, time4retrieve: str):
        return mainNaturalResourceRetrieve(retrieve_data_type, location4retrieve, time4retrieve)

    def _arun(self, retrieve_data_type: str, location4retrieve: str, time4retrieve: str):
        raise NotImplementedError("natural_resource_retrieve_tool does not support async")


def mainNaturalResourceRetrieve(retrieve_data_type, location4retrieve, time4retrieve):
    try:
        print(f'retrieve the needed data: type-{retrieve_data_type}, location-{location4retrieve}, time-{time4retrieve}')
        print('------------------')

    except Exception as e:
        return f"The natural resource retrieve task has failed, and meets the exception{e}"

    return f"The natural resource retrieve task has completed."

if __name__ == '__main__':
    # Initialize input parameters
    retrieve_data_type = 'storm surge'
    location = 'Ninbo city'
    time4retrieve = '2022091308'

    natural_resource_retrieve_tool = NaturalResourceRetrieveTool()

    # Call the tool
    retrieve_result = natural_resource_retrieve_tool._run(retrieve_data_type, location, time4retrieve)
    #
    # # Print the result
    # print(forecast_result)

