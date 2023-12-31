import os
import json
import pickle
import re

import streamlit as st
from streamlit import session_state as ss

st.set_page_config(page_title="pip.ai")

file = open("currencies.pkl", "rb")
CURRENCIES = pickle.load(file)

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"


# Define a function for validating an Email
def check_email(email):
    # pass the regular expression
    # and the string into the fullmatch() method
    if re.fullmatch(regex, email):
        return True

    else:
        return False


def show_data(username, json_data):
    for datas in [json_data]:
        if datas["name"] == username:
            return datas


def create_file():
    file1 = open("data.json", "a")  # append mode
    file1.close()


def check_value(data, val):
    return any(player["email"] == val for player in len(data))


# Define a function for creating a form
def create_form():
    username = st.text_input("Name", key="name")
    email = st.text_input("Email", key="email")
    base_currency = st.selectbox("base currency", CURRENCIES)
    target_currency = st.multiselect("target currency", CURRENCIES)
    lst = []

    for i in range(len(target_currency)):
        number_min = st.number_input(
            str(target_currency[i]) + " min",
            key=str(target_currency[i]) + "_min",
            value=0.0000001,
            format="%.5f",
        )
        number_max = st.number_input(
            str(target_currency[i]) + " max",
            key=str(target_currency[i]) + "_max",
            value=0.0000001,
            format="%.5f",
        )
        lst.append({target_currency[i]: [number_min, number_max]})

    with st.form("tar", clear_on_submit=True):
        st.write(lst)
        submit = st.form_submit_button("Submit")
    if submit:
        if check_email(email):
            dct = {
                "name": username,
                "email": email,
                "hasChanged": True,
                "base_currency": base_currency,
                "target_currency": lst,
            }
            json_object = json.dumps(dct, indent=4)
            with open("data.json", "w") as outfile:
                outfile.write(json_object)
            with open("data.json", "r") as openfile:
                json_object = json.load(openfile)
            ss["show_form"] = False
        else:
            st.error("Please enter the valid email address")


if "data.json" in os.listdir():
    # if "data.json" exists then show the data
    with open("data.json", "r") as openfile:
        json_object = openfile.readlines()
    if len(json_object) == 0:
        st.title("Please fill the preference and threshold value.")
        create_form()
    else:
        st.title("Your set data.")
        with open("data.json", "r") as openfile:
            json_object = json.load(openfile)
        st.write(show_data(json_object["name"], json_object))


else:
    # Else ask user to create new preference
    create_file()

    name_in_dct = False
    newScenario = st.button("Create New Scenario", key="a")

    if "show_form" not in ss:
        ss["show_form"] = False
    if newScenario:
        ss["show_form"] = True

    if not ss["show_form"]:
        create_form()
