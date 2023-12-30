import streamlit as st 
import pandas as pd
import matplotlib as plt
import os

df = pd.read_csv("./data/huracanes.csv")



st.write(df)