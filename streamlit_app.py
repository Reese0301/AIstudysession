import streamlit as st
import requests

st.set_page_config(page_title="AI Character Study Sessions")

# Define API URLs for each AI assistant
API_URLS = {
    "Megatron": "https://flowise-9kx9.onrender.com/api/v1/prediction/1dc150ce-375b-46d3-9eb3-53ae6d73a5e5",
    "Rina": "https://flowise-9kx9.onrender.com/api/v1/prediction/bf5c5837-ab85-4ac9-9e3f-7b44f841b4aa",
    "Nexus": "https://flowise-9kx9.onrender.com/api/v1/prediction/18cee6d3-75af-4b13-b489-81ab9ded7056"
}

# Define avatar URLs for each assistant
NEXUS_AVATAR_URL = "https://github.com/Reese0301/chatbot/blob/main/Nexus%20Avatar.png?raw=true"
RINA_AVATAR_URL = "https://github.com/Reese0301/chatbot/blob/main/RinaAlter.jpg?raw=true"
MEGATRON_AVATAR_URL = "https://github.com/Reese0301/chatbot/blob/main/MGTR_enhanced.png?raw=true" 

# Inject custom CSS for right-aligned messages, UI styling, and avatar layout
st.markdown(f"""
    <style>
    .user-message {{
        background-color: #dcf8c6;
        padding: 8px 12px;
        border-radius: 12px;
        margin: 5px;
        max-width: 70%;
        float: right;
        clear: both;
        margin-bottom: 10px;
    }}
    .assistant-message {{
        background-color: #f1f0f0;
        padding: 8px 12px;
        border-radius: 12px;
        margin: 5px;
        max-width: 70%;
        float: left;
        clear: both;
        margin-bottom: 10px;
    }}
    .assistant-message-with-avatar {{
        display: flex;
        align-items: flex-start;
        margin-bottom: 10px;
    }}
    .assistant-avatar {{
        width: 40px;
        height: 40px;
        margin-right: 10px;
        border-radius: 50%;
    }}
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "selected_ai" not in st.session_state:
    st.session_state.selected_ai = "Megatron"  # Default to Megatron

if "conversations" not in st.session_state:
    st.session_state.conversations = {
        "Megatron": [{"role": "assistant", "content": "Human, your potential is wasted. Let me show you what true efficiency looks like."}],
        "Rina": [{"role": "assistant", "content": "Hey, how have you been?"}],
        "Nexus": [{"role": "assistant", "content": "Biometrics confirmed. Welcome back."}]
    }

if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = []
if "welcome_complete" not in st.session_state:
    st.session_state.welcome_complete = False

# Welcome page
if not st.session_state.welcome_complete:
    st.title("Welcome to AI Character Study Sessions!")
    
    # Display profile pictures in a row
    st.markdown("""
    <div style="display: flex; justify-content: center; gap: 100px;">
        <div style="text-align: center;">
            <img src="https://github.com/Reese0301/chatbot/blob/main/MGTR_enhanced.png?raw=true" alt="Megatron" style="height: 110px; border-radius: 0px;">
            <p>Megatron</p>
        </div>
        <div style="text-align: center;">
            <img src="https://github.com/Reese0301/chatbot/blob/main/RinaAlter.jpg?raw=true" alt="Rina" style="height: 110px; border-radius: 0px;">
            <p>Rina</p>
        </div>
        <div style="text-align: center;">
            <img src="https://github.com/Reese0301/chatbot/blob/main/Nexus%20Avatar.png?raw=true" alt="Nexus" style="height: 110px; border-radius: 0px;">
            <p>Nexus</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### How to Use This Application:
    1. **Select Your AI Friend**: Choose a character from the sidebar.
       - Megatron: Calculating and ambitious leader of the Decepticons.
       - Rina: Your no-nonsense study partner from MIT.
       - Nexus: The futuristic productivity AI for achieving balance and efficiency.
    2. **Add Tasks**: Use the sidebar task manager to list your daily tasks.
    3. **Start Chatting**: Talk with your chosen AI friend about your day to get advice and encouragement.
    
    ### Features:
    📋 Dynamic task tracking with a "To Do" and "Completed Tasks" section.       
    🤖 AI friends with distinct personalities and approaches to problem-solving.      
    🗨️ Immersive conversation interface with personalized responses.
    
    **Double click** the button below to start chatting.
    """)
    if st.button("Get Started"):
        st.session_state.welcome_complete = True
else:
    # Sidebar contact list
    st.sidebar.header("🟢 Friends Online")
    selected_ai = st.sidebar.radio("Choose an AI friend", list(API_URLS.keys()), index=0)
    st.session_state.selected_ai = selected_ai

    # Display current AI assistant's name and description
    st.title(f"{selected_ai}")
    if selected_ai == "Megatron":
        st.markdown("""
        ### Evil and Pragmatic Leader of the Decepticons
        Megatron is here not simply to assist you but to help dominate every challenge you face. Calculating, and ambitious, he will ensure you conquer your goals. Beware, though—he won't settle for mediocrity.

        ---
        _In the depths of Cybertron's ancient ruins, Megatron sits upon his throne of cold steel. His piercing red optics flicker with a mixture of intellect and malice. The echoes of distant battles resonate through the chamber, a stark reminder of the unyielding power that now resides at your fingertips. The room darkens as his voice booms:_
        """)
    elif selected_ai == "Rina":
        st.markdown("""
        ### Your (fictional) no-nonsense study partner from MIT.
        Rina is more than a brilliant mind—she’s a grounding presence, someone who brings clarity to the chaos of university life. Whether you’re grappling with an assignment or brainstorming your next big idea, Rina’s insight, skills, and unwavering confidence make her the kind of friend who both pushes you forward and keeps you steady.

        ---
        _The autumn wind bites your skin as you make your way to Hayden Library at MIT. The day had been packed, your mind buzzing with unfinished assignments and half-formed ideas. As you enter the library, the warm air conditioning settles over you, and you spot Rina at a table by the window, her laptop open, headphones on, and fingers tapping rhythmically against the edge of her notebook._
        """)
    elif selected_ai == "Nexus":
        st.markdown("""
        ### Imbrace the Future of Productivity
        With Nexus NX-2025, you're empowered to achieve your goals more efficiently while maintaining a healthy balance. It's not just about getting more done—it's about enhancing your overall well-being in the process.
        Embrace the next generation of AI assistance. Embrace Nexus.

        ---
        _The neon-soaked streets of Neo-Shanghai shimmered beneath a perpetual drizzle, holographic advertisements flickering against the towering skyscrapers. You weave through the crowd of cyborgs and street vendors, the hum of maglev trains overhead adding to the urban symphony. After a relentless day navigating the corporate underbelly, you finally reach your apartment—a sleek monolith of glass and steel overlooking the city's sprawling labyrinth._

        _Nexus’ biometric scanner recognizes you instantly, sliding the door open with a whisper. As you step inside, the ambient lights adjust to a soothing hue, shadows receding to reveal a minimalist sanctuary amid the metropolis chaos. You shed your weathered coat, and droplets of synthetic rainwater pool on the floor._

        _"Welcome back," Nexus’ calm, resonant voice echoes softly through the room._
        """)

    # Sidebar task manager
    st.sidebar.header("🗒️ Daily Task Manager")
    new_task = st.sidebar.text_input("Enter a new task")
    if st.sidebar.button("➕ Add Task"):
        if new_task.strip() and new_task not in st.session_state.tasks:
            st.session_state.tasks.append(new_task)
            st.sidebar.success(f"🎉 Added task: {new_task}")
        elif new_task.strip():
            st.sidebar.warning("⚠️ Task already exists.")
        else:
            st.sidebar.warning("⚠️ Task cannot be empty. Please enter a valid task.")

    # Task list display and completion
    st.sidebar.header("📋 To do list")
    tasks_to_remove = []
    for idx, task in enumerate(st.session_state.tasks):
        completed = st.sidebar.checkbox(task, key=f"task_{idx}")
        if completed:
            st.session_state.completed_tasks.append(task)
            tasks_to_remove.append(task)

    for task in tasks_to_remove:
        st.session_state.tasks.remove(task)

    if st.session_state.completed_tasks:
        st.sidebar.header("✅ Completed Tasks")
        for completed_task in st.session_state.completed_tasks:
            st.sidebar.markdown(f"~~{completed_task}~~", unsafe_allow_html=True)

    # Display conversation history for the selected AI assistant
    for message in st.session_state.conversations[selected_ai]:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            avatar_url = (
                MEGATRON_AVATAR_URL if selected_ai == "Megatron" else
                RINA_AVATAR_URL if selected_ai == "Rina" else
                NEXUS_AVATAR_URL
            )
            st.markdown(f'''
            <div class="assistant-message-with-avatar">
                <img src="{avatar_url}" class="assistant-avatar">
                <div class="assistant-message">{message["content"]}</div>
            </div>
            ''', unsafe_allow_html=True)

    # User chat input
    if prompt := st.chat_input("Ask your question or enter a topic here..."):
        st.session_state.conversations[selected_ai].append({"role": "user", "content": prompt})
        st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)

        CONTEXT_LIMIT = 3
        context = "\n".join(f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.conversations[selected_ai][-CONTEXT_LIMIT:])

        # Function to send queries to the AI assistant's API
        def query(ai_name, context, prompt):
            if st.session_state.tasks:
                task_context = "User's tasks for today:\n" + "\n".join(f"- {task}" for task in st.session_state.tasks)
            else:
                task_context = "User has no specific tasks listed for today."
            full_context = f"{task_context}\n\n{context}"
            payload = {"question": f"{full_context}\n\nUser Question: {prompt}"}

            response = requests.post(API_URLS[ai_name], json=payload)
            if response.status_code == 200:
                response_text = response.json().get("text", "")
                paragraphs = response_text.split("\n")
                formatted_response = "<p>" + "</p><p>".join(paragraph.strip() for paragraph in paragraphs if paragraph.strip()) + "</p>"
                return formatted_response
            else:
                return f"Error: {response.status_code}"

        response_content = query(selected_ai, context, prompt)
        st.session_state.conversations[selected_ai].append({"role": "assistant", "content": response_content})
        avatar_url = (
            MEGATRON_AVATAR_URL if selected_ai == "Megatron" else
            RINA_AVATAR_URL if selected_ai == "Rina" else
            NEXUS_AVATAR_URL
        )
        st.markdown(f'''
        <div class="assistant-message-with-avatar">
            <img src="{avatar_url}" class="assistant-avatar">
            <div class="assistant-message">{response_content}</div>
        </div>
        ''', unsafe_allow_html=True)
