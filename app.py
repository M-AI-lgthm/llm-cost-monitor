# Step 1: Install the necessary libraries
!pip install -q streamlit pyngrok litellm

# Step 2: Write the Streamlit app code to a file
app_code = """
import streamlit as st
import litellm
import pandas as pd
import os
import time
import threading
import json
from pyngrok import ngrok

MODEL_PROVIDERS = {
    "OpenAI": {
        "models": ["gpt-4o", "gpt-4", "gpt-3.5-turbo"],
        "key_env_var": "OPENAI_API_KEY",
    },
    "Google": {
        "models": ["gemini/gemini-1.5-pro-latest", "gemini/gemini-1.5-flash-latest", "gemini/gemini-1.0-pro"],
        "key_env_var": "GEMINI_API_KEY",
    },
    "Gemma": {
        "models": ["gemma/gemma-7b"],
        "key_env_var": "GEMINI_API_KEY",
    },
    "Anthropic": {
        "models": ["claude-3-opus-20240229", "claude-3-sonnet-20240229"],
        "key_env_var": "ANTHROPIC_API_KEY",
    },
    "Mistral AI": {
        "models": ["mistral/mistral-large-latest", "mistral/mistral-small-latest"],
        "key_env_var": "MISTRAL_API_KEY",
    },
    "Cohere": {
        "models": ["command-r", "command-r-plus"],
        "key_env_var": "COHERE_API_KEY",
    },
    "Groq": {
        "models": ["groq/llama3-70b-8192", "groq/llama3-8b-8192", "groq/mixtral-8x7b-32768"],
        "key_env_var": "GROQ_API_KEY",
    },
    "Hugging Face": {
        "models": [
            "huggingface/meta-llama/Llama-3-8b-chat-hf",
            "huggingface/meta-llama/Llama-3-70b-chat-hf",
            "huggingface/meta-llama/Llama-2-7b-chat-hf",
            "huggingface/meta-llama/Llama-2-13b-chat-hf",
            "huggingface/meta-llama/Llama-2-70b-chat-hf"
        ],
        "key_env_var": "HUGGING_FACE_API_KEY",
    },
}

st.set_page_config(layout="wide", page_title="LLM Cost Monitor & Analyzer")
st.title("LLM & Framework Cost Monitor")
st.subheader("Your central hub for tracking AI development costs.")

st.info("💡 **How it works:** This app uses the LiteLLM library to abstract away different APIs. You select a model, provide its API key, and the app makes a call. The response automatically includes cost and usage data, which is then displayed here.")

# Function to load data from file
def load_usage_log():
    if os.path.exists("usage_log.json"):
        with open("usage_log.json", "r") as f:
            return json.load(f)
    return []

# Function to save data to file
def save_usage_log():
    with open("usage_log.json", "w") as f:
        json.dump(st.session_state.usage_log, f)

# Function to clear the history
def clear_history():
    if os.path.exists("usage_log.json"):
        os.remove("usage_log.json")
    st.session_state.usage_log = []
    st.rerun()

# Initialize session state with data from file
if 'usage_log' not in st.session_state:
    st.session_state.usage_log = load_usage_log()

col1, col2 = st.columns([1, 2])

with col1:
    st.header("1. Select & Test an LLM")

    selected_provider = st.selectbox("Select a Provider", list(MODEL_PROVIDERS.keys()))

    selected_model_list = MODEL_PROVIDERS[selected_provider]["models"]
    selected_model = st.selectbox("Select an LLM", selected_model_list)

    api_key_env_var = MODEL_PROVIDERS[selected_provider]["key_env_var"]
    user_api_key = st.text_input(f"Enter your `{api_key_env_var}`", type="password")

    prompt = st.text_area("Enter a prompt to test the model:", "What is the new model in OpenAI?")

    if st.button("Run & Get Cost"):
        if not user_api_key:
            st.error("Please enter your API key to proceed.")
        else:
            try:
                os.environ[api_key_env_var] = user_api_key

                with st.spinner("Generating response..."):
                    response = litellm.completion(
                        model=selected_model,
                        messages=[{"role": "user", "content": prompt}]
                    )

                cost = response.get("response_cost", 0)
                if cost is None:
                    cost = 0

                tokens_used = response.get("usage", {}).get("total_tokens", 0)

                st.session_state.usage_log.append({
                    "model": selected_model,
                    "cost": f"${cost:.6f}",
                    "tokens": tokens_used,
                    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                    "provider": selected_provider,
                })
                save_usage_log()

                if cost > 0:
                    st.success("Call successful! Cost and usage data logged.")
                else:
                    st.warning("Cost data not available in the response. Call logged with $0 cost.")

            except Exception as e:
                st.error(f"Error during API call: {e}")
                st.warning("Double-check your API key and model name.")

with col2:
    st.header("2. Usage & Cost Dashboard")

    if st.session_state.usage_log:
        df = pd.DataFrame(st.session_state.usage_log)

        st.subheader("Recent API Calls")
        st.dataframe(df.sort_values(by="timestamp", ascending=False))

        df['cost_float'] = df['cost'].str.replace('$', '').astype(float)
        total_cost = df['cost_float'].sum()
        st.metric("Total Cost", f"${total_cost:.4f}")

        st.subheader("Cost by Model")
        cost_by_model = df.groupby('model')['cost_float'].sum().reset_index()
        st.bar_chart(cost_by_model, x='model', y='cost_float')

        st.subheader("Tokens by Model")
        tokens_by_model = df.groupby('model')['tokens'].sum().reset_index()
        st.bar_chart(tokens_by_model, x='model', y='tokens')
    else:
        st.info("No LLM calls have been made yet. Use the section on the left to get started.")

    st.markdown("---")
    st.button("Clear History", on_click=clear_history)

st.markdown("---")
st.header("3. How to Monitor Costs for Other Tools")

markdown_content = '''
For frameworks like **CrewAI** and tools like **Docker**, cost is tied to the LLM or server they use. **LiteLLM** provides a proxy server to centralize all costs in one place.
'''
st.markdown(markdown_content)
"""
with open('app.py', 'w') as f:
    f.write(app_code)

# Step 3: Authenticate ngrok
# Replace 'YOUR_NGROK_AUTHTOKEN' with your actual token from ngrok.com
!ngrok authtoken 31VLY1GLH4Qf0f3CoWmRLvx57ej_2C93Sd1YgD9n8ZKmbHoKy

# Step 4: Run the Streamlit app and create the ngrok tunnel
def run_streamlit():
    os.system('streamlit run app.py --server.port 8501 --server.address 0.0.0.0')

# Start Streamlit in a new thread
thread = threading.Thread(target=run_streamlit)
thread.start()

# Wait for Streamlit to start and then create the ngrok tunnel
time.sleep(5)
public_url = ngrok.connect(addr='8501')
print("Streamlit app is running at:", public_url)

Initial commit of app.py file
