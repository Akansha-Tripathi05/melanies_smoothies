# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)

# option = st.selectbox(
#     "What is your favourite fruit?",
#     ("Banana", "Strawberry", "Peaches"),
# )

# st.write("Your favourite fruit is:", option)
from snowflake.snowpark.functions import col
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect(
    "Choose upto 5 ingredeints:",
    my_dataframe,
    max_selections=5
)
if ingredient_list:
    # st.write(ingredient_list)
    # st.text(ingredient_list)
    ingredients_string=''
    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
    st.write(ingredients_string)
    my_insert_stmt = """
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')
"""
    st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button('Submit Order')
    # st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
