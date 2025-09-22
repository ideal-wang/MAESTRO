**LLM-EMF: A Multi-Agent Framework for Government Decision Support in Automated Natural Disaster Simulations**

LLM-EMF is a modular, multi-agent system designed to assist government agencies in conducting automated scenario analyses during natural disasters. By orchestrating specialized agents—each responsible for distinct functional tasks—LLM-EMF enables rapid, data-driven decision support throughout the lifecycle of an event.

---

## Quick Start

To explore LLM-EMF’s capabilities, open and run the Jupyter notebook
**`multi_agent_test.ipynb`**
(located alongside this README). This notebook provides hands-on demonstrations of how the various agents be constructed and interact to simulate disaster scenarios and generate actionable insights.

---

## Repository Structure

All subdirectories listed below contain essential components for the multi-agent system:

```
LLM-EMF/
├── README.md
├── multi_agent_test.ipynb
├── config/
│   ├── root_base.py
│   └── prompt_config.py
├── tools/
│   ├── meteorology_agent/
│   ├── emergency_management_agent/
│   └── …
├── long_memory/
│   ├── forecast_data/
│   │   ├── .csv
│   │   └── …
│   └── static_data/
│       ├── .npy
│       └── …
└── short_memory/
    ├── system_file.pkl
    └── …
```

* **`config/`**
  Stores configuration files, including system path definitions and prompt templates for each agent.

* **`tools/`**
  Contains customized models used by every functional agent.

* **`long_memory/`**
  Archives agents’ output data alongside real-time information inputs, supporting persistent state and historical analysis.

* **`short_memory/`**
  Maintains transient data generated during each multi-agent execution, facilitating rapid context switching without polluting the long-term archive.

---


