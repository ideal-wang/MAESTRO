import json
import os
import pickle

from langchain.tools import BaseTool
import pandas as pd

from config.root_base import *

class HydrologicalDamageSurveyTool(BaseTool):
    name: str = "hydrological_damage_survey_tool"
    description: str = ("Useful to survey the hydrological damage during the disaster and Summarize the disaster damage"
                        " results for water conservancy projects.")

    def _run(self):
        return mainHydrologicalDamageSurvey()

    def _arun(self):
        raise NotImplementedError("hydrological_damage_survey_tool does not support async")


def mainHydrologicalDamageSurvey():
    damage_survey = summarize_damage()
    print(f"Hydrological disaster damage survey completed. Survey is : {damage_survey}")
    print('------------------')
    store_survey(damage_survey)
    return f"Hydrological disaster damage survey completed. Survey is : {damage_survey}"
def store_survey(damage_survey):
    print('store the hydrological damage survey result')
    print('------------------')

    disaster_name = 'Lekima'
    # with open(SYSTEM_FILE_PATH, 'rb') as f:
    #     system_memory = pickle.load(f)
    # try:
    #     disaster_name = system_memory['disaster_name']
    # except:
    #     disaster_name = 'unknown'

    survey_path = f'{hydrological_survey_root}/{disaster_name}_hydro.json'
    os.makedirs(os.path.dirname(survey_path), exist_ok=True)
    with open(survey_path, 'w') as json_file:
        json.dump(str(damage_survey), json_file, indent=4)
def summarize_damage():
    print('survey the hydrological damage')
    print('------------------')
    # damage_data = pd.read_csv(self.damage_data_path)
    damage_data = pd.DataFrame({
        'project': ['Dam', 'Canal', 'Pump Station'],
        'damage_level': ['Severe', 'Moderate', 'Mild'],
        'repair_cost_estimate': [1000000, 500000, 300000]
    })

    # 2. 生成汇总结果
    damage_summary = {
        'total_projects': damage_data.shape[0],
        'severe_damage': damage_data[damage_data['damage_level'] == 'Severe'].shape[0],
        'moderate_damage': damage_data[damage_data['damage_level'] == 'Moderate'].shape[0],
        'mild_damage': damage_data[damage_data['damage_level'] == 'Mild'].shape[0],
        'total_estimated_cost': damage_data['repair_cost_estimate'].sum()
    }

    # 3. 返回汇总结果
    return damage_summary

if __name__ == "__main__":
    tool = HydrologicalDamageSurveyTool()
    res = tool._run()
    # print(res)
