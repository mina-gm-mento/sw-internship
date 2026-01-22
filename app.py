
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

if "todos" not in state:
    state.todos = [Todo("출근"), Todo("SW 교육"), Todo("회식")]

def add_todo():
    text = state.get("new_item_text", "").strip()
    if text:
        state.todos.append(Todo(text=text))
    state.new_item_text = ""  # ✅ 콜백 안에서 리셋

st.title("To-do list")

st.text_input("New item", key="new_item_text", placeholder="Add to-do item")
st.button("Add", on_click=add_todo)  # ✅ 안전

for todo in state.todos:
    st.write(f"- {todo.text}")