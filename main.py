import streamlit as st
import ortools

st.sidebar.title("Parameters")
st.sidebar.text("")
st.sidebar.text("")

st.title('Capacitated Vehicle Routing Problem')
print("")
st.header('Using docplex...')

st.sidebar.text("Number of buses = 15")
st.sidebar.text("")
st.sidebar.slider("Number of students on every bus", 0, 100, 10)
st.sidebar.text("")
st.sidebar.text('Capacity of every bus = 100')
st.sidebar.text("")

if st.sidebar.button("Run Algorithm"):
    st.sidebar.text("Some magic!")
