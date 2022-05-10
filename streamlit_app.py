import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.header('Fruityvice Fruit Advice!')

fruit_choice = streamlit.text_input('What fruit would you like information about?' , 'Kiwi')
streamlit.write('The user entered' , fruit_choice)

streamlit.title('My Mom\'s healthy new diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect('Pick some Fruits:',list(my_fruit_list.index))

fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)




fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

streamlit.dataframe(fruityvice_normalized)


streamlit.stop()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])

my_cur = my_cnx.cursor()

my_cur.execute("SELECT * FROM fruit_load_list ")

my_data_row = my_cur.fetchall()

streamlit.header("the fruit load list contains:")

streamlit.dataframe(my_data_row)


fruit_add = streamlit.text_input('What fruit would you like to add?' , 'jackfruit')
streamlit.write('Thanks for adding' , fruit_add)


my_cur.execute("insert into fruit_load_list values('from streamlit')")

