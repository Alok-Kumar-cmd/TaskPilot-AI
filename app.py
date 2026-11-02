
import streamlit as st

from agent import run_agent


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="TaskPilot AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 TaskPilot AI")
st.caption("Your intelligent agentic AI assistant")

st.markdown("""
I can help you with:
- Mathematical calculations
- Task management
- AI and programming knowledge
- General questions
""")


# -----------------------------
# SESSION MANAGEMENT
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# DISPLAY CHAT HISTORY
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# USER INPUT
# -----------------------------

prompt = st.chat_input("Ask TaskPilot anything...")


if prompt:

    # Preserve previous conversation for the agent
    history = st.session_state.messages.copy()

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("TaskPilot is thinking..."):

            try:
                answer = run_agent(prompt, history)
                st.markdown(answer)

            except Exception as e:
                answer = f"Something went wrong: {str(e)}"
                st.error(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.header("TaskPilot AI")

    st.write("Agent capabilities")

    st.write("🧮 Calculator")
    st.write("📝 Task Manager")
    st.write("📚 Knowledge Search")
    st.write("🧠 LLM Reasoning")

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()
