import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from windrose import WindroseAxes
import streamlit as st


def create_timeseries_df(df: pd.DataFrame) -> pd.DataFrame:
    timeseries = df[["date", "PM2.5", "NO2", "WSPM"]].set_index(
        "date").resample("D").mean()

    return timeseries


tiantan_df = pd.read_csv("tiantan_aqi.csv")

tiantan_df.sort_values(by="date", inplace=True)

tiantan_df['date'] = pd.to_datetime(tiantan_df['date'])

min_date = tiantan_df['date'].min()
max_date = tiantan_df['date'].max()


with st.sidebar:
    st.image("weather.png")

    start_date, end_date = st.date_input(
        label="date range", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df: pd.DataFrame = tiantan_df[(tiantan_df["date"] >= str(start_date))
                                   & (tiantan_df["date"] <= str(end_date))]


timeseries_df = create_timeseries_df(main_df)

st.header("Tiantan Station Air Quality")

col1, col2, col3, col4 = st.columns(4)

with col1:
    pmtwo_mean = timeseries_df["PM2.5"].mean().round()
    st.metric(label="PM2.5", value=pmtwo_mean)

with col2:
    notwo_mean = timeseries_df['NO2'].mean().round()
    st.metric(label="NO2", value=notwo_mean)

with col3:
    wind_mean = timeseries_df["WSPM"].mean().round()
    st.metric(label="wind speed", value=f"{wind_mean} mph")

with col4:
    wd = main_df["wd"].mode()[0]
    st.metric(label="wind direction", value=wd)

sns.set_style("whitegrid")
fig = plt.figure(figsize=(16, 6))

plt.plot(timeseries_df.index, timeseries_df['PM2.5'], label="PM2.5")
plt.plot(timeseries_df.index, timeseries_df['NO2'], label="NO2")
plt.tick_params(axis='y', labelsize=14)
plt.tick_params(axis='x', labelsize=14)

plt.legend()
st.pyplot(fig)


st.subheader("polutan based on wind direction")

fig = plt.figure(figsize=(14, 10))

fmt = '%.0f%%'
yticks = mtick.FormatStrFormatter(fmt)

rect = [0.1, 0.5, 0.4, 0.4]
wa = WindroseAxes(fig, rect)
fig.add_axes(wa)
wa.bar(main_df['wda'], main_df['PM2.5'],
       normed=True, opening=0.8, edgecolor='white')
wa.yaxis.set_major_formatter(yticks)
wa.set_title("PM2.5 concencration by wind direction")
wa.legend()

rect = [0.5, 0.5, 0.4, 0.4]
wa1 = WindroseAxes(fig, rect)
fig.add_axes(wa1)
wa1.bar(main_df['wda'], main_df['NO2'],
        normed=True, opening=0.8, edgecolor='white')
wa1.yaxis.set_major_formatter(yticks)
wa1.set_title("NO2 concencration by wind direction")
wa1.legend()

rect = [0.1, 0, 0.4, 0.4]
wa2 = WindroseAxes(fig, rect)
fig.add_axes(wa2)
wa2.bar(main_df['wda'], main_df['WSPM'],
        normed=True, opening=0.8, edgecolor='white')
wa2.yaxis.set_major_formatter(yticks)
wa2.set_title("Wind speed in mph")
wa2.legend()
st.pyplot(fig)
