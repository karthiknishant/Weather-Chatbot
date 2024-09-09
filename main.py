
from creds import OPENAI_API_KEY, weather_key
import streamlit as st
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent
from agents import reverse_geocoding_tool, geocoding_tool, current_weather_tool,Geography_tool,closest_cities_tool,day5_hour3_forecast_tool,current_datetime_tool
import openai

# Initialize the OpenAI API key
openai.api_key = OPENAI_API_KEY

# Initialize the LLM with the GPT-4 model
llm = OpenAI(model="gpt-4o")

# Initialize the ReAct agent with tools
agent = ReActAgent.from_tools(
    [Geography_tool, geocoding_tool,reverse_geocoding_tool, current_weather_tool,closest_cities_tool,day5_hour3_forecast_tool,current_datetime_tool],
    llm=llm,
    max_iterations=20,
    verbose=True
)

# Streamlit app setup
st.title("Weather Chatbot")

# Create a chat-like interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to handle user input and agent response
def get_agent_response(user_input):
    st.session_state.messages.append({"role": "user", "content": user_input})
    agent_response = agent.chat(user_input)
    st.session_state.messages.append({"role": "assistant", "content": agent_response})

# User input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You: ", "")
    submitted = st.form_submit_button("Send")
    if submitted and user_input:
        get_agent_response(user_input)

# Display the conversation history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Bot:** {message['content']}")