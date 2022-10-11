import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

def get_fruit_load_list(my_cnx):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
    return my_cur.fetchall()
  
def insert_row_snowflake(my_fruit,mycnx):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('"+my_fruit+"')")
    return "Thanks for adding "+my_fruit

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

myfruitlist = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
myfruitlist = myfruitlist.set_index("Fruit")
fruits_selected = streamlit.multiselect("Pick some fruits:",list(myfruitlist.index),['Avocado','Strawberries'])
fruits_to_show = myfruitlist.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to continue.")
  else:
    fruityvice_normalized = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()

if streamlit.button("Get Fruit load list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list(my_cnx)
  streamlit.dataframe(my_data_rows)
  
my_fruit = streamlit.text_input("What fruit would you like to add?")
if streamlit.button("Add a fruit to the list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  return_msg= insert_row_snowflake(my_fruit,my_cnx)
  streamlit.write(return_msg)
