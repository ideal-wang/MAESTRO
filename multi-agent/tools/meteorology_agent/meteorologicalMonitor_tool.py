from datetime import datetime
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type


class MeteorologicalForecastInput(BaseModel):
    frequency: str = Field(description="frequency of meteorological monitor task, base on the emergency response level.")

class MeteorologicalMonitorTool(BaseTool):
    name: str = "meteorological_monitor_tool"
    description: str = ("Useful to monitor the meteorological data at the specific frequency base on the emergency "
                        "response level.")
    args_schema: Type[BaseModel] = MeteorologicalForecastInput

    def _run(self, frequency: str):
        return f"The meteorological monitor will be executed at the frequency {frequency}"

    def _arun(self, frequency: str):
        raise NotImplementedError("initiate_emergency_response_tool does not support async")


# 示例使用
if __name__ == "__main__":

    meteorological_monitor_tool = MeteorologicalMonitorTool()

    res = meteorological_monitor_tool._run(frequency='24h')

    print(res)
