
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
    state.new_item_text = ""

def check_todo(i, new_value):
    state.todos[i].is_done = new_value

def remove_todo(i):
    state.todos.pop(i)

st.title("To-do list")

st.text_input("New item", key="new_item_text", placeholder="Add to-do item")
st.button("Add", on_click=add_todo)

for i, todo in enumerate(state.todos):
    c1, c2 = st.columns([0.9, 0.1])
    with c1:
        # ✅ 토글 값을 직접 넘기지 말고 현재 체크 상태를 기준으로 콜백에서 처리
        st.checkbox(
            label=todo.text,
            value=todo.is_done,
            key=f"chk-{todo.uid}",
            on_change=lambda idx=i: check_todo(idx, not state.todos[idx].is_done),
        )
    with c2:
        st.button("🗑️", key=f"del-{todo.uid}", on_click=lambda idx=i: remove_todo(idx))
