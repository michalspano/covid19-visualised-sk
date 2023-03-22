#!/usr/bin/env python3

import json
from requests import get
from flask import Flask, render_template, redirect, request


# Create a Flask app
app = Flask(__name__)


# Accepted routes and their associated data
@app.route("/")
@app.route("/foo")
@app.route("/bar")
@app.route("/baz")
@app.route("/doctor")
def index():
    # TODO: remove foo, bar, baz and other exemplary routes

    """
    Current supported routes:
    / | /foo | /bar | /baz | /doctor 
    """

    # Load the API details
    api: dict = load_JSON_API('static/api.json')

    # Create route specific data
    route_specific_api: dict = api[request.url_rule.rule]

    # Fetch data from the API 
    fetched_session = fetch(route_specific_api['URL'])

    # Check response
    if not fetched_session:
        return render_template('error.html', error='API error')

    # Render the template
    return render_template('index.html', data=fetched_session, keys=[
        [
            route_specific_api['graph1']['key'], 
            route_specific_api['graph1']['description']
        ],

        [
            route_specific_api['graph2']['key'], 
            route_specific_api['graph2']['description']
        ],
    ])


# Fetch data from the API
def fetch(URL: str):
    """Contact the API"""

    # Handle API errors requests
    try:
        response = get(URL)
    except requests.RequestException:
        return None

    # Handle response possible errors
    try:
        raw = response.json()['page']
    except (json.JSONDecodeError, KeyError):
        return None

    data: dict = {}

    # Parse the data to a dictionary of dictionaries
    # Handle possible key errors
    try:
        for item in raw:
            data[item['id']] = item
    except KeyError:
        return None

    # Return parsed data
    return data


def load_JSON_API(path: str) -> dict:
    """Load API from a JSON file"""
    return json.load(open(path))


if __name__ == '__main__':
    # TODO: get rid of the debug operand
    app.run(debug=True)