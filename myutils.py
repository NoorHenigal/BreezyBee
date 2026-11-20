# this file is for my logic functions for my BreezyBee weather tracker
# BreezyBee.py imports this file and calls out these functions

import pandas as pd

# I set my file name and column names here to be used everywhere throughout the website process
FILE_NAME = "weather.csv"  # this the csv file where my weather data is saved
COLUMNS = ["Date", "Temperature", "Conditions", "Humidity", "Wind_Speed"]


def clean_dates(data):
    """makes every date look the same so like 2026-11-19, even if Excel or anything else that changed the format."""
    # reads the dates day first, like 19/11/2026
    data["Date"] = pd.to_datetime(data["Date"], dayfirst=True)
    # writes them back as year/month/day so search can be able to find them 
    data["Date"] = data["Date"].dt.strftime("%Y-%m-%d")
    return data


def load_data():
    """loads weather data from the csv file so if the file doesn't exist yet it will return an empty table."""
    try:
        # this reads the CSV file into a table
        data = pd.read_csv(FILE_NAME)
        # makes sure all the dates are in the same format
        data = clean_dates(data)
    except FileNotFoundError:
        # here a  condition is set out the first time so that if there is no file yet to make an empty table
        data = pd.DataFrame(columns=COLUMNS)
    return data


def save_data(data):
    """saves the weather table to the csv file and returns True if it worked and False if it didn't."""
    try:
        # this will write the table to the csv so if index=False it would stop an extra number column
        data.to_csv(FILE_NAME, index=False)
        return True  # here it means the saving worked
    except Exception:
        # if any problem occurs while saving the data so that means saving failed 
        return False  


def validate_input(date, temperature, conditions, humidity, wind_speed, data):
    """checks the form values before saving so it returns (True, "OK") if all is fine or (False, error message)."""
    # I check here if date is already in the table as well as turn it both into text to compare
    if str(date) in data["Date"].astype(str).values:
        return False, "This date is already logged"
    # checks that a weather condition was chosen
    if conditions == "":
        return False, "Please choose a condition"
    # checks the temperature is realistic
    if temperature < -50 or temperature > 60:
        return False, "Temperature is not realistic"
    # humidity is a percentage so it must be between 0 and 100
    if humidity < 0 or humidity > 100:
        return False, "Humidity must be between 0 and 100"
    # wind speed can't be below 0
    if wind_speed < 0:
        return False, "Wind speed can't be negative"
    # if all checks pass the input is therefore valid
    return True, "OK"


def validate_table(data):
    """checks every row of the edited table before saving so returns (True, "OK") or (False, error message)."""
    # goes through the table one row at a time
    for index, row in data.iterrows():
        if row["Temperature"] < -50 or row["Temperature"] > 60:
            return False, "Temperature is not realistic on " + str(row["Date"])
        if row["Humidity"] < 0 or row["Humidity"] > 100:
            return False, "Humidity must be between 0 and 100 on " + str(row["Date"])
        if row["Wind_Speed"] < 0:
            return False, "Wind speed can't be negative on " + str(row["Date"])
    # if no row broke a rule the table is good to go
    return True, "OK"


def get_stats(data):
    """returns the average, minimum and maximum temperature."""
    # this takes the temperature column and makes sure it is numbers
    temps = data["Temperature"].astype(float)
    return temps.mean(), temps.min(), temps.max()


def search_by_date(data, date):
    """returns all rows that match the chosen date."""
    # here this keeps only the rows where the date matches the chosen date
    return data[data["Date"].astype(str) == str(date)]


def get_records(data):
    """returns the hottest day and the coldest day."""
    # sorts the table from coldest to hottest
    data_sorted = data.sort_values("Temperature")
    coldest = data_sorted.iloc[0]   # first row is the coldest day
    hottest = data_sorted.iloc[-1]  # last row is the hottest day
    return hottest, coldest


def get_alerts(row):
    """my innovation is to add weather alerts with a bee fun fact so it then  returns a list of (type, message, bee_fact)."""
    # takes the values from this one day and make them numbers
    temperature = float(row["Temperature"])
    humidity = float(row["Humidity"])
    wind_speed = float(row["Wind_Speed"])
    conditions = row["Conditions"]

    alerts = []  # has to be empty list to collect the alerts

    # temperature alerts in degree celcius only as one of these can happen due to if / elif
    if temperature > 40:
        alerts.append(("error", "Extreme heat! Stay indoors!",
                       "Even the bees are staying home fanning the hive"))
    elif temperature > 35:
        alerts.append(("warning", "Very hot must drink water",
                       "Bees are carrying water to cool the hive"))
    elif temperature < 13:
        alerts.append(("info", "Cold, wear a jacket",
                       "Too chilly for bees to fly!"))

    # these are separate ifs so that means more than one can show at the same time
    if conditions == "Rainy":
        alerts.append(("info", "Take an umbrella",
                       "No bees outside, rain keeps them in the hive"))

    if wind_speed > 25:
        alerts.append(("warning", "Strong winds",
                       "Too windy for bees, they're grounded"))

    if humidity > 80:
        alerts.append(("warning", "Very humid, stay cool",
                       "Sticky air slows down honey drying"))

    # if no alerts were added that means the weather is nice
    if len(alerts) == 0:
        alerts.append(("success", "Nice weather, enjoy your day",
                       "Perfect pollinating weather, the bees are buzzing!"))


    return alerts