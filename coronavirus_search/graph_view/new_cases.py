import requests
from datetime import date
import pandas as pd
from pytrends.request import TrendReq
import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots


def get_countries():
    # Returns dictionary of key:country, valuer:slug,2 letter code
    r = requests.get("https://api.covid19api.com/countries").json()

    # formats list
    dic = {ele["Country"]: [ele["Slug"], ele["ISO2"]] for ele in r}

    return dic


def sorted_countries():
    # Returns sorted list of countries
    lcountries = []
    for ele in get_countries():
        lcountries.append(ele)
    return sorted(lcountries)


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

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=df['date'], y=df['covid19'],
            name="Google Trend pour le mot \"Covid19\"",
            opacity=0.8, marker={'color': '#457ec4'}),
        secondary_y=True
    )

    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['cases'],
            name="Cas de Covid19",
            marker={'color': '#a80d0d'}),
        secondary_y=False
    )

    fig.update_layout(
        title_text=f"Correlation cas de Covid19 et recherches sur Google pour le {country}")
    fig.update_xaxes(title_text="Date", dtick="M1", tickangle=-90)
    fig.update_yaxes(title_text="Cas de Covid19",
                     secondary_y=False)
    fig.update_yaxes(
        title_text="Google Trend", secondary_y=True)

    return plot(fig, output_type='div')


if __name__ == '__main__':
    draw_plot("Canada")
