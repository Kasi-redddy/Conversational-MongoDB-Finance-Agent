import streamlit as st
from agent import get_answer
from memory import ConversationMemory

st.set_page_config(layout="wide")
st.title("Conversational MongoDB Finance Agent (Ollama Llama 3)")

with st.sidebar:
    st.header("Conversation History")
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationMemory()
    for h in st.session_state.memory.history:
        st.write(f"**You:** {h['user']}")
        st.markdown(f"**Agent:** {h['agent']}")

st.markdown(
    """
    **How to use:**  
    - Ask any question about your finance data (definitions, filters, aggregations, trends, comparisons, etc.).
    - All answers are generated from your real MongoDB data using RAG.
    """
)

user_input = st.text_input("Ask a question about your finance data:")

if st.button("Ask") and user_input:
    answer = get_answer(user_input, st.session_state.memory)
    st.session_state.memory.add(user_input, answer)
    st.markdown(answer)
