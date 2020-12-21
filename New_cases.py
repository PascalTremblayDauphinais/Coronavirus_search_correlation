import requests
from datetime import date
import pandas as pd
from pytrends.request import TrendReq
import matplotlib.pyplot as plt


def get_countries():
    # Get list of country, slug and 2 letter code
    r = requests.get("https://api.covid19api.com/countries").json()

    # formats list
    dic = {ele["Country"]: [ele["Slug"], ele["ISO2"]] for ele in r}

    return dic


def show_countries():
    # Get list of country, slug and 2 letter code
    r = requests.get("https://api.covid19api.com/countries").json()

    # formats list
    dic = {ele["Country"]: [ele["Slug"], ele["ISO2"]] for ele in r}
    print([x for x in dic])


def build_url_covid(countries, country):
    # Builds url to access covid19 API
    today = date.today().strftime("%Y-%m-%d")
    url = "https://api.covid19api.com/country/"+countries[country][0] + \
        "/status/confirmed?2020-01-01T00:00:00Z&to="+today+"T00:00:00Z"

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


def get_trend(countries, country):
    today = date.today().strftime("%Y-%m-%d")
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(
        ["covid19"], timeframe="2020-01-01 " + today, geo=countries[country][1])

    return pytrends.interest_over_time()


def assemble_final_df(country):
    # Assembles df with covid API data and Trend data

    # Get list of country
    countries = get_countries()

    # Build covid API data df
    covid_json = requests.get(build_url_covid(countries, country)).json()
    covid_df = build_df_covid(covid_json)

    # Build Trend data df
    trend_df = get_trend(countries, country)

    # Assemble final df
    df = pd.merge(covid_df, trend_df, how="inner",
                  left_on="date", right_index=True)

    return df


def draw_plot(country):
    df = assemble_final_df(country)

    date = df["date"]
    cases = df["cases"]
    trend = df["covid19"]

    fig, ax1 = plt.subplots()
    plt.xticks(date, rotation="vertical")
    ax1.plot(date, cases)
    ax2 = ax1.twinx()
    ax2.bar(date, trend)

    plt.savefig('.\\figures\\test.png')


if __name__ == '__main__':
    draw_plot("Canada")
