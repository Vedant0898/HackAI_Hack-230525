import streamlit as st
import json  
from streamlit import session_state as ss
import os
def show_data(username, json_data):
   #  json_data = json.load(json_data)
    for datas in [json_data]:
      #   print("data",datas['name'])
        if datas["name"] == username:
            return datas
        
def create_file():
   file1 = open("userdata.json", "a")  # append mode
   file1.close()

def check_value(data, val):
    return any(player['email']==val for player in len(data))



st.title("This is PageOne Geeks.") 
st.sidebar.success("You are currently viewing Page One Geek")
def create_form():
    # with open('userdata.json', 'r') as openfile:
    #        json_object = json.load(openfile)
    username = st.text_input("Name", key='name')
    email = st.text_input("Email",key='email')
    base_currency = st.selectbox('base currency',['INR','USD','CAD'])
    traget_currency = st.multiselect('target currency',['INR','CAD','USD','YEN'])
    lst = []

    for i in range(len(traget_currency)):
        number_min = st.number_input(traget_currency[i],key=str(traget_currency[i])+"_min")
        number_max = st.number_input(traget_currency[i],key=str(traget_currency[i])+"_max")
        lst.append({traget_currency[i] : [number_min,number_max]})

    with st.form('tar',clear_on_submit=True):
        st.write(lst)
        submit = st.form_submit_button('Submit')
    if submit:
        dct = {
                   'name' : username,
                   'email': email,
                   'base_currency': base_currency,
                   'target_currency': lst,
            }
        json_object = json.dumps(dct, indent=4)
        with open("userdata.json", "w") as outfile: 
           outfile.write(json_object)
        with open('userdata.json', 'r') as openfile:
           json_object = json.load(openfile)
        ss["show_form"] = False

if ('userdata.json' in os.listdir()):

    with open('userdata.json', 'r') as openfile:
       json_object = openfile.readlines()
    if len(json_object) ==0:
        # newScenario = st.button("Create New Scenario", key="a")

        create_form()
    else:
        with open('userdata.json', 'r') as openfile:
            json_object = json.load(openfile)
        st.write(show_data(json_object['name'],json_object))


else:
    create_file()

    name_in_dct = False
    newScenario = st.button("Create New Scenario", key="a")

    if "show_form" not in ss:
        ss["show_form"] = False
    if newScenario:
        ss["show_form"] = True

    if not ss["show_form"] :
        create_form()
