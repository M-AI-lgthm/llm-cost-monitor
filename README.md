# llm-cost-monitor

## Title: LLM & Framework Cost Monitor

### A Dashboard for Tracking AI Development Expenses

Owner : Mary-AI-lgthm

<img width="1808" height="908" alt="image" src="https://github.com/user-attachments/assets/b7ce7f81-5fbf-4712-8455-53bca0b316d6" />
<img width="608" height="553" alt="image" src="https://github.com/user-attachments/assets/dfa2449f-3cb5-457a-8e42-ec5a79504baf" />
<img width="1812" height="592" alt="image" src="https://github.com/user-attachments/assets/c55ada02-7e31-4a1a-a9dd-5f323cab1062" /> <img width="1221" height="754" alt="image" src="https://github.com/user-attachments/assets/79a201c0-a898-4fae-aa64-1cef410291c2" />

## The Problem We're Solving
Problem: Building with large language models (LLMs) can be unpredictable. When using different APIs and frameworks, it's hard to centralize and track costs, leading to unexpected bills.

Solution: We created a single, unified dashboard to monitor and analyze all LLM usage and costs in one place.

## App Overview & Key Features
App Overview: This app uses LiteLLM, a library that provides a unified API to over 100 LLM providers. Instead of learning different APIs, we use one single command to talk to all of them.

Key Features:

Multi-Provider Support: Supports all major LLM providers like OpenAI, Google, Anthropic, Groq, and Hugging Face.

Cost Tracking: Automatically extracts cost data from API responses and logs it.

Usage Dashboard: Visualizes total costs, costs per model, and token usage with an intuitive dashboard.

Data Persistence: Saves all call history to a local JSON file (usage_log.json), so data is never lost, even if you close the app.

Reset Functionality: Includes a "Clear History" button to reset the dashboard for new demonstrations or projects.

## How It Works: The Architecture
Core Components:

Streamlit: The web framework used to build the interactive user interface. It handles the front-end and user interaction.

LiteLLM: The crucial backend library. It acts as a wrapper around all the different LLM APIs, allowing us to make a single function call (litellm.completion()) regardless of the provider. It's also the component that provides the cost data.

Data Persistence: A simple JSON file (usage_log.json) acts as a database to store all API call records. This ensures data is persistent across sessions.

## The Code in Action: A Walkthrough
The Code: Show the app running in the browser.

Demonstrate a call: Select a provider (e.g., Groq), enter a key and a prompt, and click "Run & Get Cost."

Explain the output: Point out the "Call successful!" message, the updated tables, and the charts.

Show the "Clear History" button: Click it and demonstrate how the dashboard instantly resets to a blank state.

## Conclusion & Benefits
Benefits: This app saves time, prevents surprise bills, and provides a centralized view of all LLM expenses.

Final Thoughts: This simple application demonstrates the power of using a standardized library like LiteLLM to build robust, multi-provider solutions for managing AI costs.

## LLM Cost Monitor Dashboard
This tool features automatic API response parsing with pandas-powered data processing for aggregating usage metrics, performing cost analysis calculations, and generating statistical insights across different LLM providers. The system uses pandas DataFrames for efficient data manipulation and filtering, enabling real-time visualization of token usage, cost per model trends, and comparative analysis without manually accessing individual provider consoles. This is built for the ML/AI development community.
 - Tech Stack: Python, Streamlit, LiteLLM, Pandas, JSON Storage
- Data Processing: pandas for aggregating usage metrics
- Analysis: Cost analysis calculations and statistical insights
- Data Manipulation: Efficient filtering and trend analysis using DataFrames
- Comparative Analysis: Cross-provider cost comparison

```mermaid
graph TD
    A[Start App / User Opens Browser] --> B{Is usage_log.json file present?};
    B -->|Yes| C[Load data from usage_log.json into session_state];
    B -->|No| D[Initialize empty session_state.usage_log];
    C --> E[Display UI with Dashboard];
    D --> E;
    E --> F[User Clicks Run & Get Cost Button];
    F --> G[Make API Call with LiteLLM];
    G --> H{Call Successful?};
    H -->|Yes| I[Extract Cost & Tokens from Response];
    H -->|No| J[Display Error Message];
    I --> K[Append new data to session_state.usage_log];
    K --> L[Save usage_log to usage_log.json];
    L --> M[Refresh Dashboard with New Data];
    J --> M;
    M --> N{User Clicks Clear History?};
    N -->|Yes| O[Delete usage_log.json file];
    O --> P[Reset session_state.usage_log];
    P --> Q[Restart App (Rerun)];
    Q --> B
