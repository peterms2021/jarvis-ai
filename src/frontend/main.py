import streamlit as st
import json
import requests

API_URL = "http://0.0.0.0:8000/agents"  # We will use our local URL and port defined of our microservice for this example

def get_agents():
    """
    Get the list of available agents from the API
    """
    response = requests.get(API_URL + "/get-agents")
    if response.status_code == 200:
        agents = response.json()
        return agents

    return []

def create_first_agent(payload:str):
    """
    Create first agent
    """
    response = requests.post(API_URL + "/create-agent", json = payload)
    if response.status_code == 200:
        #print("Successfully created agent: ", response.json())
        return True

    print(" Error creating agent: ", response.json())
    return False

def create_first_conversation(agent_id:str, name:str):
    """
    Create first conversation on an agent
    """
    payload = {"agent_id": agent_id, "name": name}
    
    response = requests.post(API_URL + "/create-conversation", json = payload)
    #print("create_first_conversation response: ",json.dump(response.json()))
    
    if response.status_code == 200:
        print("Successfully created first conversaition: ", response.json())
        return True

    print(" Error creating first conversation: ", payload)
    return False

def get_conversations(agent_id: str):
    """
    Get the list of conversations for the agent with the given ID
    """
    response = requests.get(API_URL + "/get-conversations", params = {"agent_id": agent_id})
    if response.status_code == 200:
        conversations = response.json()
        return conversations

    return []

def get_messages(conversation_id: str):
    """
    Get the list of messages for the conversation with the given ID
    """
    response = requests.get(API_URL + "/get-messages", params = {"conversation_id": conversation_id})
    if response.status_code == 200:
        messages = response.json()
        return messages

    return []

def send_message(agent_id, message):
    """
    Send a message to the agent with the given ID
    """
    payload = {"conversation_id": agent_id, "message": message}
    print("send_message:", json.dumps(message))
    response = requests.post(API_URL + "/chat-agent", json = payload)
    if response.status_code == 200:
        return response.json()

    return {"response": "Error"}



def read_json_file(filename):
    # Try to open and load the file
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        # Return the data
        return data
    # Catch any IOError exception
    except IOError as e:
        # Print the error message
        print(f"Error: {e}")
        # Return None
        return None

def create_first_agent_and_coversation():
    # Call the function with a valid filename
    data = read_json_file('prompts/first.json')
    # Print the data
    # print('First Prompt data:', data)

    if data is None:
        st.write("Unable to read initial prompt data.")
        return None
    

    if create_first_agent(data):
        #get the agent ID
        agents = get_agents()
        print(" AGENTS RETURNED: ",json.dumps(agents, indent=4))
        if len(agents) == 0:
            st.write("No agent created after initializing.")
        else:
            
            # create first conversation
            agent = agents[0]
            print("AGENT ID:", json.dumps(agent, indent=4))
            if create_first_conversation(agent["id"], "Conv_1"):
                return True
            else:
                 print("Failed to create first conversation")
                 return False
    
    else:
        st.write("Unable to initialize agent.")    
        return None

def main():
    st.set_page_config(page_title = "🤗💬 A-Jarvis AIChat")

    with st.sidebar:
        st.title("Architecture Agent Chat")

        # Dropdown to select agent
        agents = get_agents()
        
        if len(agents) == 0:
            print("Initializing conversations")
            if create_first_agent_and_coversation():
                 #reload the agents
                 agents = get_agents()
             
        print(" AGENTS RETURNED: ",json.dumps(agents, indent=4))
        agent_ids = [agent["id"] for agent in agents]
        selected_agent = st.selectbox("Select an Agent:", agent_ids)
        
        for agent in agents:
            if agent["id"] == selected_agent:
                selected_agent_context = agent["context"]
                selected_agent_first_message = agent["first_message"]

        # Dropdown to select conversation
        conversations = get_conversations(selected_agent)      
        conversation_ids = [conversation["id"] for conversation in conversations]
        selected_conversation = st.selectbox("Select a Conversation:", conversation_ids)

        if selected_conversation is None:
            st.write("Please select a conversation from the dropdown.")
        else:
            st.write(f"**Selected Agent**: {selected_agent}")
            st.write(f"**Selected Conversation**: {selected_conversation}")

    # Display chat messages
    st.title("Chat")
    st.write("This is a chat interface for the selected agent and conversation. You can send messages to the agent and see its responses.")
    st.write(f"**Agent Context**: {selected_agent_context}")

    messages = get_messages(selected_conversation)
    with st.chat_message("assistant"):
        st.write(selected_agent_first_message)

    for message in messages:
        with st.chat_message("user"):
            st.write(message["user_message"])
        with st.chat_message("assistant"):
            st.write(message["agent_message"])

    # User-provided prompt
    if prompt := st.chat_input("Send a message:"):
        with st.chat_message("user"):
            st.write(prompt)
        with st.spinner("Thinking..."):
            response = send_message(selected_conversation, prompt)
            with st.chat_message("assistant"):
                st.write(response["response"])

if __name__ == "__main__":
    main()
