# BreezyBee 🐝-  Weather Tracker

A Streamlit web app built for a local meteorology club to log daily weather observations and see climate patterns over time.

**Live app:** https://breezybee-noor.streamlit.app/
**Video Link:** https://youtu.be/Uwr0Gm4Vxfo
---

## About the project

This is my project for the General Assembly Data Science Bootcamp. The client who is a local meteorology club needed a simple web dashboard where members can:

- log the weather each day
- see key temperature stats
- search for a specific day
- view, edit, upload and download the full history

## Features

### Pages

| Page | What it does |
|---|---|
| Log Observation | A form to record the date, temperature, conditions, humidity and wind speed  |
| Dashboard | Average, min and max temperature (`st.metric`), a temperature trend line chart, record hottest and coldest days, a conditions bar chart, and a humidity and wind chart |
| Search | Pick a date to see that day's weather |
| View All Data | Full history in a sortable table, plus csv upload and download |
| Edit Data | Edit the data like a spreadsheet (`st.data_editor`), including adding or deleting rows |
| Alerts | My phase 3 innovation |

### Phase 2

- Temperature trend over time with `st.line_chart`
- The record hottest day highlighted and the record coldest day highlited as well

### Phase 3 innovation: weather alerts with bee fun facts

Pick a day and BreezyBee gives weather advice in colored alert boxes, each with a bee fun fact.

- On a nice day, an animated bee appears
- On a hot day, honey drips from the top of the page

The bee facts are based on research about how weather affects bee flight (see in `references.txt`).

## How it works

- **Modularity:** all logic functions (loading, saving, validation, stats, search, records and alerts) are in `myutils.py`. `BreezyBee.py` imports them and builds the screens.
- **State management:** the data is stored in `st.session_state` so it isn't lost when Streamlit reruns.
- **CSV loop:** the user can upload a csv, edit it in the app, and download it back to their computer.
- **Error handling:**
  - the app doesn't crash if `weather.csv` is missing (it starts with an empty table)
  - form inputs are validated (no duplicate dates, a condition must be chosen, humidity 0–100, no negative wind, realistic temperatures)
  - edited tables are checked before saving
  - broken csv uploads show an error message instead of crashing
  - dates changed by spreadsheet apps (like `19/11/2026`) are converted back to `2026-11-19` to be readable

## Project files

```
├── BreezyBee.py          # main Streamlit app
├── myutils.py            # logic functions
├── weather.csv           # sample weather data
├── bee.gif               # bee animation
├── honey.gif             # honey drip animation
├── references.txt        # sources for bee facts and images and any outsider reference
├── requirements.txt      # libraries needed to run the app
├── .gitignore            # files Git should ignore
└── .streamlit/
    └── config.toml       # bee colour theme
```

## How to run it on your computer

1. Download the project:
   - Click the green code button at the top of this page, then download zip and then unzip it
   - or just click on the live demo link (if you don't want to download)

2. Open your terminal and go into the project folder:
   ```
   cd BreezyBee-Noor-Mohamed-main
   ```
  
3. Install the libraries:
   ```
   pip install -r requirements.txt
   ```

4. Run the app:
   ```
   streamlit run BreezyBee.py
   ```

The app opens in your browser and it will start with the sample data in weather.csv.

## Tools used

- Python
- Streamlit
- pandas


## Creator

Noor Mohamed: General Assembly Bahrain, Data Science Bootcamp DSB4
