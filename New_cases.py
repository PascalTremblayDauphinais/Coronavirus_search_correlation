import requests
import json
from datetime import date
import pandas as pd
from pytrends.request import TrendReq
from matplotlib import pyplot as plt


def build_url_covid(country_name):
    # Builds url to access covid19 API
    today = date.today().strftime("%Y-%m-%d")

    url = "https://api.covid19api.com/country/"+country_name + \
        "/status/confirmed?2020-03-01T00:00:00Z&to="+today+"T00:00:00Z"
    return url


def build_df_covid(json):
    # Builds dataframe using json from API

    # Merges case per regions of a country into one value
    cnt_dic = {}
    for ele in json:
        if ele["Date"] in cnt_dic:
            cnt_dic[ele["Date"]] = cnt_dic[ele["Date"]] + ele['Cases']
        else:
            cnt_dic[ele["Date"]] = ele['Cases']

    # Creates dictionary used in DF creation
    dic = {"date": [], "cases": []}
    for key, value in cnt_dic.items():
        dic["date"].append(key[:10])
        dic["cases"].append(value)

    df = pd.DataFrame(dic)
    df["date"] = pd.to_datetime(df["date"])

    return df


def get_trend(country_2char, date):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(
        ["covid19"], timeframe="2020-03-01 " + date, geo=country_2char)

    return pytrends.interest_over_time()


r = requests.get(build_url_covid("canada"))
api_data = r.json()
df = build_df_covid(api_data)
test = get_trend("CA", "2020-11-20")
df = pd.merge(df, test, how="inner", left_on="date", right_index=True)

date = df["date"]
cases = df["cases"]
trend = df["covid19"]

fig, ax1 = plt.subplots()
cases.plot()
trend.plot(kind="bar")
ax1.set_xticklabels(date)

plt.show()
