import os
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type

from config.root_base import *


class HydraulicForecastInput(BaseModel):
    time4forecast: str = Field(description="The timestamp for generating the hydraulic infrastructure status forecast, "
                                           "formatted as 'YYYYMMDDHH'.")
    forecast_duration: str = Field(description="The forecast duration for the hydraulic infrastructure status "
                                               "(e.g., '24h').")

class HydraulicForecastTool(BaseTool):
    name: str = "hydraulic_infrastructure_status_forecast_tool"
    description: str = ("Tool designed to forecast the status of hydraulic infrastructure using the meteorological "
                        "forecast result over a specified forecast duration.")
    args_schema: Type[BaseModel] = HydraulicForecastInput

    def _run(self, time4forecast: str, forecast_duration: str):
        return mainHydraulicForecast(time4forecast, forecast_duration)

    def _arun(self, time4forecast: str, forecast_duration: str):
        raise NotImplementedError("hydraulic_infrastructure_status_forecast_tool does not support asynchronous "
                                  "operations")

# 定义 mainHydropowerForecast 函数
def mainHydraulicForecast(time4forecast, forecast_duration):
    print(f'Calculating the hydraulic infrastructure status forecast result at time {time4forecast} for the duration at {forecast_duration}')
    print('-------------------')
    try:
        print('read the past data.')
        print('-------------------')
        print('load the forecast model and calculate the future data.')
        print('-------------------')
        print('store the forecast hydraulic infrastructure status')

        #
        forecast_time = (datetime.strptime(time4forecast, "%Y%m%d%H") + timedelta(hours=int(forecast_duration.rstrip('h')))).strftime(
            "%Y%m%d%H")
        forecast_result_path = f'{hydraulic_forecast_root}/{forecast_time}_haf.npy'
        os.makedirs(os.path.dirname(forecast_result_path), exist_ok=True)

        forecast_hydraulic_result = np.ones(5)
        np.save(forecast_result_path, forecast_hydraulic_result)
    except Exception as e:
        return f"The hydraulic infrastructure status forecast task is failed and the exception is {e}."

    return f"The hydraulic infrastructure status forecast task has completed and the forecast data between {time4forecast} to {forecast_time} is calculated."


# 工具调用实例
if __name__ == "__main__":
    # 初始化输入参数
    current_time = '2022091320'
    forecast_duration = '24h'

    hydraulic_forecast_tool = HydraulicForecastTool()

    # 调用工具
    forecast_result = hydraulic_forecast_tool._run(current_time, forecast_duration)

    # 打印结果
    # print("Hydropower Forecast Result Path is :")
    # print(forecast_result)
