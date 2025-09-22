import os

from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type, List

from config.root_base import *

from datetime import datetime
from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

# Assume these paths are defined in your configuration module.
from config.root_base import rural_report_root, hydrological_report_root, review_report_template_root

# Define the input schema with an added field for the report drafting time.
class DraftDisasterReportInput(BaseModel):
    disaster_name: str = Field(
        description="The name of the disaster for drafting the report."
    )
    report_type: str = Field(
        description="The type of the report. Must be either 'post-disaster review report' or 'disaster in-progress brief report'."
    )
    time4report: str = Field(
        description="The time when the report is drafted, in the format YYYYMMDDHH."
    )

# Define the tool class for drafting the disaster report.
class DraftDisasterReportTool(BaseTool):
    name: str = "draft_disaster_report_tool"
    description: str = (
        "Tool for drafting disaster reports. The report type must be either a post-disaster review report or "
        "a disaster in-progress brief report. The report drafting time must be provided in the format YYYYMMDDHH."
    )
    args_schema: Type[BaseModel] = DraftDisasterReportInput

    def _run(self, disaster_name: str, report_type: str, time4report: str):
        return draft_disaster_report(disaster_name, report_type, time4report)

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("draft_post_disaster_review_report_tool does not support async operations.")

# Define the function that drafts the disaster report.
def draft_disaster_report(disaster_name: str, report_type: str, time4report: str):
    print(f'generate the disaster report for {disaster_name} in the {time4report} in {report_type} type')
    print('------------------')

    try:
        # Combine the loaded content.
        combined_content = (
            f"**report_template**\n\n"
            f"Agricultural Disaster Report:\n**agricultural_disaster_report**\n\n"
            f"Hydrological Disaster Report:\n**hydrological_disaster_report**"
        )

        # Select the final message based on the report type.
        if report_type == "post-disaster review report":
            final_message = (
                f"The post-disaster review report for {disaster_name} drafted at {time4report} has been finalized. "
                "It is imperative that we continue to monitor the environment to prepare for potential new disasters."
            )
        elif report_type == "disaster in-progress briefing":
            final_message = (
                f"The disaster in-progress briefing for {disaster_name} drafted at {time4report} has been finalized. "
                "Immediate action is required to mitigate ongoing impacts."
            )
        else:
            return f"Invalid report type specified for disaster: {disaster_name}."

        # Store the combined report, including the drafting time in the file name.
        store_report(combined_content, disaster_name, time4report)

    except Exception as e:
        print(f'When loading the disaster reports, the exception {e} occurs.')
        return f"Error drafting reports for disaster: {disaster_name}"

    return final_message


def store_report(report: str, disaster_name: str, time4report: str):
    print('store the disaster report')
    print('------------------')
    report_file_path = f'{review_report_template_root}/{disaster_name}_{time4report}_reviewReport.txt'
    os.makedirs(os.path.dirname(report_file_path), exist_ok=True)
    with open(report_file_path, 'w') as report_file:
        report_file.write(report)

# Example usage:
if __name__ == "__main__":
    # Create tool instance.
    disaster_report_tool = DraftDisasterReviewReportTool()

    # Run the tool with disaster name, report type, and drafting time (format YYYYMMDDHH).
    report_info = disaster_report_tool._run(
        disaster_name='Lekima',
        report_type='post-disaster review report',  # or 'disaster in-progress briefing'
        time4report='2025030112'
    )

    # Print the result.
    print(report_info)
