import json
import os
import pickle

from langchain.tools import BaseTool
import pandas as pd

from config.root_base import *  # Ensure these paths are defined in your config


class AgriculturalDamageSurveyTool(BaseTool):
    name: str = "agricultural_damage_survey_tool"
    description: str = ("Useful to survey the agricultural damage during the disaster and summarize the disaster damage"
                        " results for agricultural projects like crops, irrigation systems, and farmland.")

    def _run(self):
        return mainAgriculturalDamageSurvey()

    def _arun(self):
        raise NotImplementedError("agricultural_damage_survey_tool does not support async")


def mainAgriculturalDamageSurvey():
    damage_survey = summarize_damage()
    print(f"Agricultural disaster damage survey completed. Survey is: {damage_survey}")
    print('------------------')
    store_survey(damage_survey)
    return f"Agricultural disaster damage survey completed. Survey is: {damage_survey}"


def store_survey(damage_survey):
    print('Store the agricultural damage survey result')
    print('------------------')

    disaster_name = 'Lekima'  # Example disaster name (can be dynamically assigned)

    survey_path = f'{rural_survey_root}/{disaster_name}_rural.json'
    os.makedirs(os.path.dirname(survey_path), exist_ok=True)
    with open(survey_path, 'w') as json_file:
        json.dump(str(damage_survey), json_file, indent=4)


def summarize_damage():
    print('Survey the agricultural damage')
    print('------------------')

    # Simulate agricultural damage data
    damage_data = pd.DataFrame({
        'project': ['Rice', 'Wheat', 'Vegetables'],
        'damage_level': ['Severe', 'Moderate', 'Mild'],
        'repair_cost_estimate': [200000, 100000, 50000]
    })

    # Summarize the damage data
    damage_summary = {
        'total_projects': damage_data.shape[0],
        'severe_damage': damage_data[damage_data['damage_level'] == 'Severe'].shape[0],
        'moderate_damage': damage_data[damage_data['damage_level'] == 'Moderate'].shape[0],
        'mild_damage': damage_data[damage_data['damage_level'] == 'Mild'].shape[0],
        'total_estimated_cost': damage_data['repair_cost_estimate'].sum()
    }

    return damage_summary


if __name__ == "__main__":
    tool = AgriculturalDamageSurveyTool()
    res = tool._run()
    print(res)

