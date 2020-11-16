import requests
import json
from datetime import date
import pandas as pd


def build_url(country_name):
    # Builds url to access API
    today = date.today().strftime("%Y-%m-%d")

    url = "https://api.covid19api.com/country/"+country_name + \
        "/status/confirmed?2020-03-01T00:00:00Z&to="+today+"T00:00:00Z"
    return url


def build_df(json):
    # Builds dataframe using json from API

    dic = {}
    for ele in json:
        if ele["Date"] in dic:
            dic[ele["Date"]] = dic[ele["Date"]] + ele['Cases']
        else:
            dic[ele["Date"]] = ele['Cases']

    return dic


r = requests.get(build_url("canada"))
api_data = r.json()
print(build_df(api_data))
