import pandas as pd
import psycopg2
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

conn = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                        password = 'Passw0rd!',
                        port =5432,
                        database= 'phonepe new')
cursor=conn.cursor()
conn.commit()

def format_indian_number(number):
    if number >= 10000000:  # If number is equal to or greater than 1 crore
        return f"{number // 10000000} Cr"
    elif number >= 100000:  # If number is equal to or greater than 1 lakh
        return f"{number // 100000} L"
    else:
        return number

st.set_page_config(layout= "wide",initial_sidebar_state= "expanded")

st.sidebar.header(":violet[Phonepe_pulse]")
with st.sidebar:
    selected = option_menu("Menu", ["Home","Explore Data","About"],
                    icons=["house","bar-chart-line", "exclamation-circle"],
                    menu_icon= "menu-button-wide",
                    default_index=0,
                    styles={"nav-link": {"font-size": "13px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                            "nav-link-selected": {"background-color": "#6F36AD"}})


if selected == "Explore Data":
    explore_data = st.sidebar.selectbox("#### select type", ["overall_stats", "state_stats"])
    if explore_data == "overall_stats":
        st.markdown("## :violet[Overall Statistics]")
        cat = ["Transaction", "User"]
        select_box = st.sidebar.selectbox('#### Select the categories :', cat)
        year = [2018, 2019, 2020, 2021, 2022,2023]
        select_year = st.sidebar.selectbox("#### Select the year :", year)
        quater = ["Q1 (Jan-Mar)", "Q2 (Apr-Jun)", "Q3 (Jul-Sep)", "Q4 (Oct-Dec)"]
        select_quater = st.sidebar.selectbox("#### Select the quater :", quater)

        if select_box == "Transaction":
            tab1, tab2 = st.tabs(["Total_Transaction", "Total_Amount"])

            with tab1:
                col1, col2 = st.columns([2, 1])
                cursor.execute(
                    f"( select categories, sum(total_count) as total_counts, sum(amount) as total_amount from agg_trans_state where year = {select_year} and quater = '{select_quater}' group by categories order by categories)")
                a = pd.DataFrame(cursor.fetchall(), columns=["categories", "total_counts", "total_amount"])

                with col2:
                    col2.markdown("## :violet[Transaction]")
                    trans = a['total_counts'].sum()
                    col2.markdown("#### :violet[All PhonePe transactions (UPI + Cards + Wallets)]")
                    col2.markdown(f"#### :white[{format(trans, ',')}]")
                    col3, col4 = st.columns([1, 1])
                    amount = a['total_amount'].sum()
                    col3.markdown("#### :violet[Total payment value]")
                    col3.markdown(f"#### :white[₹ {format_indian_number(amount)}]")
                    avg = round(amount / trans)
                    col4.markdown("#### :violet[Avg. transaction value]")
                    col4.markdown(f"#### :white[₹ {avg}]")

                    # for showing categories

                    col2.markdown("### :violet[Categories]")
                    col5, col6 = st.columns([2, 1])
                    col5.markdown(f"##### :violet[{a['categories'][1]}]")
                    col6.markdown(f"##### :white[{a['total_counts'][1]}]")
                    col5.markdown(f"##### :violet[{a['categories'][3]}]")
                    col6.markdown(f"##### :white[{a['total_counts'][3]}]")
                    col5.markdown(f"##### :violet[{a['categories'][4]}]")
                    col6.markdown(f"##### :white[{a['total_counts'][4]}]")
                    col5.markdown(f"##### :violet[{a['categories'][0]}]")
                    col6.markdown(f"##### :white[{a['total_counts'][0]}]")
                    col5.markdown(f"##### :violet[{a['categories'][2]}]")
                    col6.markdown(f"##### :white[{a['total_counts'][2]}]")

                with col1:
                    # for showing bar plot

                    a["total_transaction_value"] = a["total_counts"].apply(format_indian_number)
                    fig = px.bar(a,
                                 y="categories",
                                 x="total_counts",
                                 color="total_counts",
                                 orientation="h",
                                 text="total_transaction_value",
                                 labels={"y": "Categories", "x": "Total counts"},
                                 title="Total no transaction",
                                 color_discrete_sequence=px.colors.sequential.Agsunset)
                    fig.update_layout(title_x=0.4)
                    col1.plotly_chart(fig)