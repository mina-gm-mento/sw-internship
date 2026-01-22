
import streamlit as st
from dataclasses import dataclass, field
import uuid

st.set_page_config(page_title="To-do list", page_icon=":memo:")

state = st.session_state

@dataclass
class Todo:
    text: str
    is_done: bool = False
    uid: uuid.UUID = field(default_factory=uuid.uuid4)

# 초기 목록 한 번만 세팅
if "todos" not in state:
    state.todos = [
        Todo(text="출근"),
        Todo(text="SW 교육"),
        Todo(text="회식"),
    ]

st.title("To-do list")

# 목록 표시만 (아직 입력/버튼 없음)
for todo in state.todos:
    st.write(f"• {todo.text}")
