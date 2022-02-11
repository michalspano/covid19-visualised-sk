#!/usr/bin/env python3

# TODO: Polish the code

import json
import requests
from flask import Flask, render_template, redirect, request


app = Flask(__name__)


# Routes
# TODO: Add multiple routes and handle them
# Hint: `request.url_rule`
@app.route("/")
def index():
    url: str = 'https://data.korona.gov.sk/api/vaccinations/in-slovakia'
    fetched_session = fetch(url)
    if not fetched_session:
        return render_template('error.html')
    return render_template('index.html', data=fetched_session,
                        keys = [
                            ["dose1_count", "Daily Increase - First Dose"], 
                            ["dose2_count", "Daily Increase - Second Dose"],
                        ])

# TODO: get rid of foo, bar, baz etc.
@app.route("/foo")
def foo():
    url: str = 'https://data.korona.gov.sk/api/hospital-patients/in-slovakia'
    fetched_session = fetch(url)
    if not fetched_session:
        return render_template('error.html')
    return render_template("index.html", data=fetched_session, 
    keys=[["non_covid", "Non-covid"], 
    ["confirmed_covid", "Confirmed Covid"]])


@app.route("/bar")
def bar():
    url: str = 'https://data.korona.gov.sk/api/hospital-beds/in-slovakia'

    fetched_session = fetch(url)
    if not fetched_session:
        return render_template('error.html')
    return render_template("index.html", data=fetched_session, 
                           keys=[["occupied_oaim_covid", "Occupied OAIM - Covid"],
                                 ["occupied_jis_covid", "Occupied by JIS Covid"]
                            ])


@app.route("/baz")
def baz():
    url: str = 'https://data.korona.gov.sk/api/ag-tests/in-slovakia'

    fetched_session = fetch(url)
    if not fetched_session:
        return render_template('error.html')
    return render_template("index.html", data=fetched_session,
                           keys=[["positives_sum", "Positive Test Rate"],
                                 ["negatives_sum", "Negative Tests"]
                            ])


@app.route("/doctor")
def doctor():
    url: str = 'https://data.korona.gov.sk/api/hospital-staff'

    fetched_session = fetch(url)
    if not fetched_session:
        return render_template('error.html')
    return render_template("index.html", data=fetched_session,
                           keys=[["out_of_work_ratio_doctor", "Doctors out of work"],
                                 ["out_of_work_ratio_nurse", "Nurses out of work"]
                            ])


# Fetch data from the API
def fetch(URL: str):
    """Contact the API"""

    try:
        response = requests.get(URL)
    except requests.RequestException:
        return None

    try:
        raw = response.json()['page']
    except (json.JSONDecodeError, KeyError):
        return None

    data: dict = {}

    try:
        for item in raw:
            data[item['id']] = item
    except KeyError:
        return None

    return data


if __name__ == '__main__':
    app.run(debug=True)