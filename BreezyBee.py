# BreezyBee is a weather tracker website created for the local meteorology club
# This file BreezyBee.py focuses on building all the screens and all the logic functions are in myutils.py

import streamlit as st  
import pandas as pd     
import myutils          # contains the file with all the functions

# The name and little bee icon that show on the browser tab 
# my bee colours are set in .streamlit/config.toml 
st.set_page_config(page_title="BreezyBee", page_icon="🐝")

# Streamlit reruns the whole script every time the user interacts with the app, so I load my data only once per session and keep it safe in session_state
if "data" not in st.session_state:
    st.session_state.data = myutils.load_data()

# I sort the data by date so every page shows the days in order (error handling occured here)
data = st.session_state.data.sort_values("Date", ignore_index=True)

# this is the sidebar page
st.sidebar.title(":orange[BreezyBee] 🐝")
st.sidebar.caption("Weather tracker for the meteorology club")

# The menu that lets the user move between the 6 pages
page = st.sidebar.radio("Go to", ["📝 Log Observation", "📊 Dashboard", "🔍 Search",
                                  "📋 View All Data", "✏️ Edit Data", "🚨 Alerts"])


# this the log observation page
if page == "📝 Log Observation":
    st.title("Log Observation")
    st.write("Fill in today's weather and press Submit.")

    # I put the inputs in a form so the app doesn't rerun while I'm still typing, and clear_on_submit empties the boxes after each save
    with st.form("log_form", clear_on_submit=True):
        date = st.date_input("Date")
        temperature = st.number_input("Temperature (°C)", step=0.5)
        conditions = st.selectbox("Conditions", ["", "Sunny", "Cloudy", "Rainy", "Windy", "Stormy"])
        humidity = st.number_input("Humidity (%)")
        wind_speed = st.number_input("Wind speed (km/h)")
        submitted = st.form_submit_button("Submit")

    # everything below only happens once Submit is pressed
    if submitted:
        # First I check the values make sense before saving anything
        ok, message = myutils.validate_input(date, temperature, conditions,
                                             humidity, wind_speed, data)
        if not ok:
            st.error(message)  # tells the user what is wrongg
        else:
            # I turn the new day into a one row table
            new_row = pd.DataFrame([{"Date": str(date),
                                     "Temperature": temperature,
                                     "Conditions": conditions,
                                     "Humidity": humidity,
                                     "Wind_Speed": wind_speed}])
            # Then here I add it to my data and keep it in session_state and save it to the CSV
            data = pd.concat([data, new_row], ignore_index=True)
            st.session_state.data = data
            myutils.save_data(data)
            st.success("Saved! 🐝")


# this is the dashboard page 
elif page == "📊 Dashboard":
    st.title("Dashboard")

    # If nothing is logged yet I show a message instead of it crashing
    if len(data) == 0:
        st.info("No data yet. Log a few days first 🐝")
    else:
        # My function gives me the average, lowest and highest temperature
        avg, low, high = myutils.get_stats(data)

        # Three metric cards to show side by side
        col1, col2, col3 = st.columns(3)
        col1.metric("Average (°C)", round(avg, 1))
        col2.metric("Min (°C)", low)
        col3.metric("Max (°C)", high)

        st.divider()

        # Line chart of temperature over time, this would need atleast 2 days to draw the line (for comparison reasons)
        st.subheader("Temperature trend")
        if len(data) >= 2:
            chart_data = data.set_index("Date")["Temperature"]
            st.line_chart(chart_data, color="#FFD700")  # here changed color of charts to appeal with website visuals 
        else:
            st.info("Log at least 2 days to see the chart")

        st.divider()

        # The record hottest and coldest days
        with st.container(border=True):
            st.subheader("Records")
            hottest, coldest = myutils.get_records(data)
            st.markdown(f":red[Hottest: {hottest['Temperature']} °C on {hottest['Date']}]")
            st.markdown(f":blue[Coldest: {coldest['Temperature']} °C on {coldest['Date']}]")

        st.divider()

        # A bar chart counting how many sunny, rainy, cloudy whatever condition days we have had 
        st.subheader("Weather conditions")
        st.bar_chart(data["Conditions"].value_counts(), color="#FFD700")  # here as well color for visuals for the chart 

        # Humidity and wind on one chart so the club can compare them
        st.subheader("Humidity and wind")
        st.line_chart(data.set_index("Date")[["Humidity", "Wind_Speed"]])


# this is the search page 
elif page == "🔍 Search":
    st.title("Search")
    st.write("Pick a date to see the weather for that day.")

    # The user picks a date and my function finds the matching row
    search_date = st.date_input("Choose a date")
    result = myutils.search_by_date(data, search_date)

    if len(result) == 0:
        st.info("No data for this date 🐝")
    else:
        st.dataframe(result)


# this is the view all data page 
elif page == "📋 View All Data":
    st.title("View All Data")

    # part of the CSV loop so the user can upload a starting file
    st.subheader("Upload a CSV")
    uploaded_file = st.file_uploader("Choose a weather CSV file", type="csv")

    if uploaded_file is not None:
        # file only loads when the button is clicked
        if st.button("Load this file"):
            try:
                new_data = pd.read_csv(uploaded_file)
                # the file must have my EXACT 5 columns or the other pages would break
                if list(new_data.columns) != myutils.COLUMNS:
                    st.error("Wrong columns. The file needs: Date, Temperature, Conditions, Humidity, Wind_Speed")
                else:
                    # fix the dates in case Excel changed them (when data is manipulated outside the website ) then it saves it 
                    new_data = myutils.clean_dates(new_data)
                    st.session_state.data = new_data
                    data = new_data
                    myutils.save_data(data)
                    st.success("File loaded! 🐝")
            except Exception:
                # if  file is broken the app shows an error instead of crashing as well
                st.error("This file could not be read")

    # the full history in a table (clicking a column header sorts it)
    st.subheader("All observations")
    if len(data) == 0:
        st.info("No data yet. Log a few days or upload a CSV 🐝")
    else:
        st.dataframe(data)

        # last part of the CSV loop, thsi downloads the data to the computer
        st.download_button("Download CSV", data.to_csv(index=False),
                           "weather.csv", "text/csv")


# this is the edit data page
elif page == "✏️ Edit Data":
    st.title("Edit Data")
    st.write("Click a cell to change it, then press Save changes.")

    if len(data) == 0:
        st.info("No data yet. Log a few days first 🐝")
    else:
        # a table you can edit like Excel(you can add and delete rows)
        edited = st.data_editor(data, num_rows="dynamic")

        if st.button("Save changes"):
            try:
                # keep the dates tidy and then check every row before saving
                edited = myutils.clean_dates(edited)
                ok, message = myutils.validate_table(edited)
                if not ok:
                    st.error(message)
                else:
                    st.session_state.data = edited
                    myutils.save_data(edited)
                    st.success("Changes saved! 🐝")
            except Exception:
                st.error("Something is wrong. Check your dates and numbers.")


# this is the alerts page
elif page == "🚨 Alerts":
    # I saved an empty spot at the very top so the honey can drip from there on hot days (this was done for visuals)
    honey_spot = st.empty()

    st.title("Alerts")
    st.write("Weather alerts and advice, with a bee fun fact 🐝")

    if len(data) == 0:
        st.info("No data yet. Log a few days first 🐝")
    else:
        # dropdown of all my dates that starts on the latest day
        dates = sorted(data["Date"].astype(str))
        chosen_date = st.selectbox("Choose a day", dates, index=len(dates) - 1)

        # gets the row for the chosen day
        row = myutils.search_by_date(data, chosen_date).iloc[0]

        # big weather icon that matches the conditions
        icons = {"Sunny": "☀️", "Cloudy": "☁️", "Rainy": "🌧️", "Windy": "💨", "Stormy": "⛈️"}
        st.markdown(f"# {icons.get(row['Conditions'], '🌤️')} {row['Conditions']}")

        # this is the days numbers as three cards
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature", f"{row['Temperature']} °C")
        col2.metric("Humidity", f"{row['Humidity']} %")
        col3.metric("Wind", f"{row['Wind_Speed']} km/h")

        # go through each alert from my function and shows it 
        for alert_type, message, bee_fact in myutils.get_alerts(row):
            if alert_type == "error":
                st.error(message)     
            elif alert_type == "warning":
                st.warning(message)    
            elif alert_type == "info":
                st.info(message)       
            else:
                st.success(message)    
            st.caption("🐝 " + bee_fact)

            # a nice day the bee comes out to fly 
            if alert_type == "success":
                st.image("bee.gif")

        # a hot day the honey melts and drips from the top of the page
        if float(row["Temperature"]) > 35:
            honey_spot.image("honey.gif")
            st.caption("🍯 It's so hot the honey is melting!")