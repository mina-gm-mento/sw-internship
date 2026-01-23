import streamlit as st

st.title("🚗 GM SW Intern Streamlit Demo 4")

st.write("안녕하세요! Streamlit으로 만든 네 번째 앱입니다.")

name = st.text_input("이름을 입력하세요")

if name:
    st.success(f"{name}님, 반갑습니다! 🎉")

st.button("버튼")