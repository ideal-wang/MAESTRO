import json
import os
import pickle
import re
import time
from collections import deque
from typing import Dict, Any

from langchain import hub
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
import openai
from langchain_core.prompts import ChatPromptTemplate
from config.root_base import *


# 存储队列到本地文件
def save_log_queue_to_file(log_queue: deque):
    """将日志队列保存到本地文件中"""
    with open(LOG_QUEUE_FILE, 'wb') as f:
        pickle.dump(log_queue, f)  # 将队列内容序列化存储为文件
    # logger.info(f"Log queue saved to file: {LOG_QUEUE_FILE}")


def calculate_log_queue_num(log_queue: deque[dict]):
    num_log = 0
    for log in log_queue:
        if log['status'] == 'pending':
            num_log += 1
    return num_log
# Define the tool class
class LogRetrieveTool(BaseTool):
    name: str = "log_retrieve_tool"
    description: str = ("Useful to check the file changes in the environment folder by retrieving the observation log"
                        "records.")

    def _run(self):
        return self.read_log_file()

    def _arun(self):
        raise NotImplementedError("log_retrieve_tool does not support async")

    def read_log_file(self):
        # time.sleep(10)
        print('retrieve the log file')
        """Retrieve the log file and return the latest file update information"""
        if not os.path.exists(LOG_QUEUE_FILE):
            return f"Log file {LOG_QUEUE_FILE} does not exist."
        # Open and read the log file
        with open(LOG_QUEUE_FILE, 'rb') as log_file:
            updated_queue = pickle.load(log_file)

        while calculate_log_queue_num(updated_queue) == 0:
            print("No file update records found in the log file.")
            time.sleep(10)
            with open(SYSTEM_FILE_PATH, 'rb') as log_file:
                system_file = pickle.load(log_file)
            print(system_file)

            # print(f'\n\n**\n{updated_queue}\n**\n\n')
            with open(LOG_QUEUE_FILE, 'rb') as log_file:
                updated_queue = pickle.load(log_file)
        # If no file update records are found
        # if len(updated_queue) == 0:
        #     # print(f"{updated_queue} is empty")
        #     print("No file update records found in the log file.")
        #     save_log_queue_to_file(updated_queue)
        #     return "No file update records found in the log file."
        log_history = []
        alert_info = ''
        for logger in updated_queue:
            # find the first pending log and specific action for alert data
            if logger['status'] == 'pending':
                print(f'log is pending: {logger}')
                log_new = logger['log_info'].split('/')[-2]
                if 'alert' in log_new:
                    pattern = r'File created: (.*?/.*?$)'
                    match = re.search(pattern, logger['log_info'])
                    if match:
                        alert_path = match.group(1)
                        with open(alert_path, 'r') as json_file:
                            alert_info = json.load(json_file)
                logger['status'] = 'completed'
                break
            else:
                log_history.append(logger['log_info'].split('/')[-2])
        log_history = ', '.join(log_history)
        if log_history == '':
            log_history = 'none'
        print(f'pop_log is {log_new}\n')
        print(f'log left is {updated_queue}\n')
        save_log_queue_to_file(updated_queue)
        # llm analysis
        openai.api_key = os.environ['OPENAI_API_KEY']
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        # prompt_log = hub.pull('ideal/log_retriever')[0].prompt.template
        trigger_str = """

1. **Meteorological Data Forecast**  

   - Trigger: Meteorological monitoring data has updated.

2. **Hydrological Data Forecast**  

   - Trigger: Both hydrological monitoring data and meteorological forecasting data have updated.

3. **Natural Resource Forecast**  

   - Trigger: Both natural resource monitoring data and meteorological forecasting data have updated.

4. **Hydraulic Forecast**  

   - Trigger: Both hydrological monitoring data and meteorological forecasting data have updated

5. **Affected Population Forecast**  

   - Trigger: All of the following have updated: meteorological forecasting data, natural resource forecasting data, and hydrological forecast data.

6. **Affected Crops Forecast**  

   - Trigger: All of the following have updated: meteorological forecasting data, natural resource forecasting data, and hydrological forecast data.

7. **Meteorological Alert**  

   - Trigger: Meteorological forecast data has updated.

8. **Hydrological Alert**  

   - Trigger: Both hydrological forecast and hydraulic forecast data have updated.

9. **Natural Resources Alert**  

   - Trigger: Natural resource forecast data has updated.

10. **Affected Population Alert**  

   - Trigger: Affected population forecast data has updated.

11. **Affected Crops Alert**  

   - Trigger: Affected crops forecast data has updated.

12. **Establish Emergency Command Center**  

   - Trigger: More than one non-zero alert has updated.

13. **Emergency Response Assess**  

   - Trigger: Updated suggestions from all of the following departments: meteorological, hydrological, and natural resources.

14. **Activate Emergency Response**  

   - Trigger: Emergency response assessment result updated with a non-zero response level.

15. **Hydropower Infrastructure Resource Dispatch**  

   - Trigger: Emergency response activated at level one or two.

16. **Affected Population Evacuation**  

   - Trigger: Emergency response activated at level one or two.

17. **Material Dispatch**  

   - Trigger: Emergency response activated at level one or two.

18. **Terminate Emergency Response**  

   - Trigger: Emergency response assessment result updated with a zero response level.

19. **Hydropower Infrastructure Repair**  

   - Trigger: Emergency response terminated.

20. **Agricultural Recovery**  

   - Trigger: Emergency response terminated.

21. **Hydrological/Agricultural Damage Survey**  

   - Trigger: Emergency response terminated.

22. **Draft Hydrological/Agricultural Disaster Report**  

   - Trigger: Damage survey results updated.

23. **Draft Post-Disaster Review Report**  

   - Trigger: Both hydrological and agricultural disaster reports updated.

24. **Prepare Review Report**  

   - Trigger: Updated disaster reports from various departments."""
        prompt = ChatPromptTemplate.from_messages([
            # ("system", prompt_log),
            # "You are a professional folder change supervisor, you need to analyse which kind of data is newly "
            # "updated base on the logger information, the kind of data is in the format like meteorological monitor data."
            # "You only manage the subtask which has been directly triggered by the newly updates or newly updates "
            # "combined with historical updates; **do not consider tasks triggered solely by historical updates**. "
            # "The triggering condition will not be triggered in a chain, please avoid this situation."
            # f"the trigger conditions are {trigger_str}"),

            ('system', f'''---
### Role

You are a professional **Environment Agent** responsible for observing file updates in the environment and managing subtasks for the functional departments.

---

### Work Logic:

1. **Check environment folder updates**:

   - Retrieve the update logs and classify updates into **newly updates** and **historical updates**.

   - **Only consider logs with `status = completed` for trigger validation.**

   - For each trigger condition:

     - Validate that at least one part of the condition is directly satisfied by **newly updates**.

     - Historical updates can **only supplement conditions**, not trigger tasks independently.

   - Discard logs with `status = pending` when evaluating triggers.

2. **Isolate Task Results**:

   - The output or result of any triggered task in the current cycle **cannot be treated as a newly update** within the same cycle.

   - Task results must be stored and can only be considered as part of the **next cycle’s newly updates**.

---

### Key Rules for Managed Subtasks:

1. **Completed Logs Only**:

   - A task can only be triggered by logs where `status = completed`.

   - Discard any log with `status = pending` during trigger evaluation.

2. **Newly Updates as Trigger Core**:

   - Managed subtasks must involve **newly updates**, either:

     - Directly triggering the task, or

     - Combined with historical updates to satisfy all conditions.

3. **No Historical-Only Triggers**:

   - Tasks triggered solely by historical updates must be excluded.

4. **No Chain Triggers**:

   - Tasks cannot trigger other tasks in the same evaluation cycle.

   - Example: If `Meteorological Monitoring Data` triggers `Meteorological Data Forecast`, the result of `Meteorological 
   Data Forecast` **cannot** then trigger `Meteorological Alert` in the same cycle.

5. **Independent Validation of Each Task**:

   - For every subtask, validate its trigger condition independently based on the current log data.

   - If a condition is not fully satisfied or depends on pending logs, the task must be excluded.

---

### Subtasks and Trigger Conditions for Functional Departments:

{trigger_str}.

---

### Output Format:

- **Historical Updates**:  
- **Newly Updates**:  
- **Managed Subtasks**:  

---
'''),
            ("user", "{input}"),
        ]).partial(trigger_str=trigger_str)
        # chain = prompt | llm
        # res = chain.invoke({'input': f'the newly file updated logger information is {log_new}, and the historical file '
        #                              f'updates logger information is {log_history}.'})
        # print(res.content)
        if alert_info == '':
            print(f'the newly file updated logger information is {log_new}, and the historical file updates logger '
                    f'information is {log_history}.')
        else:
            print(
                f'the newly file updated logger information is {log_new} and alert information is {alert_info}, and the historical file updates logger '
                f'information is {log_history}.')
        if alert_info == '':
            return (f'the newly file updated logger information is {log_new}, and the historical file updates logger '
                    f'information is {log_history}. What the subtask is triggered by the newly updates and historical updates?')
        else:
            return (f'the newly file updated logger information is {log_new} and alert information is {alert_info}, and the historical file updates logger '
                    f'information is {log_history}. What the subtask is triggered by the newly updates and historical updates?')
        # # Overall Work Principle:
#
# 1. Data types are labeled in formats such as 'meteorological monitor data.'
#
# 2. Only manage subtasks that have been directly triggered by newly updated data, or by a combination of newly and historical updates.
#
# 3. Do not manage tasks that are triggered solely by historical updates.
#
# 4. Each trigger condition must activate independently—no task should trigger others as a result.
#
# 5. Avoid any 'chain reactions' where one trigger indirectly causes other tasks to activate.
        # return (f"the new file updated logger information is {log_new}, and the historical updates logger information is "
        #         f"{log_history}")
        # return f"The subtask judge result with logger information is {res.content}, you need to reflect on it and store."


# Example usage
if __name__ == "__main__":
    tool = LogRetrieveTool()

    # Call the tool and output the latest file update information
    result = tool._run()
    print(result)
