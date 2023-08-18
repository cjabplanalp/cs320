import pandas as pd
from flask import Flask, request, jsonify, Response
import re
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import StringIO

# My data is from the World Happiness Report 2022, which is composed of surveyed perceptions of happiness per country. Each scale is from 0 - 10, with 0 being the least amount of happiness, and 10 being the happiest possible. Most of the data is self explanatory, but there is one column, called Dystopia (a theoretical country), which has values equal to the world’s lowest national averages for each of the six factors plus a residual. This column has no impact on the survey data, simply there for comparison and thought. The overall happiness score is the sum of each column per country, including Dystopia.

# Data gathered from: https://www.kaggle.com/datasets/mathurinache/world-happiness-report (2022)

app = Flask(__name__)
df = pd.read_csv("main.csv")

@app.route('/browse.html')
def table_data_html():
    global df
    return """<html><body><h1>Happiness Score by Country, Ranked Descending</h1><body></html>""" + df.to_html()

num_subscribed = 0
@app.route('/email', methods=["POST"])
def email():
    global num_subscribed
    email = str(request.data, "utf-8")
    
    if re.match(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email):
        with open("emails.txt", "a") as f:
            f.write(email + "\n")
            num_subscribed += 1
        return jsonify(f"thanks, you're subscriber number {num_subscribed}!")
    return jsonify("you entered an invalid email")

vers_a = 0
vers_b = 0
@app.route('/donate.html')
def donations():
    global vers_a
    global vers_b
    
    header = """<h1>Donations Page</h1>"""
    donate_args = dict(request.args)
    a_or_b = donate_args.get("from")
    
    if a_or_b == "A":
        vers_a += 1
    else:
        vers_b += 1
        
    if vers_a > vers_b:
        return header + str(vers_a)
    else:
        return header + str(vers_b)
        
    return header

last_visit = 0
visitors = {}
@app.route('/browse.json')
def table_data_json():
    global df
    global last_visit
    global visitors
    data = jsonify(df.to_dict('records'))

    if request.remote_addr not in visitors:
        visitors[request.remote_addr] = last_visit
        return data
    else:
        if time.time() - visitors[request.remote_addr] < 60:
            last_visit = time.time()
            del visitors[request.remote_addr]
            return data
        else:
            response = "too many requests, try again in 1 minute."
            return Response(response, status = 429, headers = {"Retry-After": 60})

@app.route('/plot1.svg')
def svg_1():
    global df
    fig, ax = plt.subplots()
    
    svg_args = dict(request.args)
    change = svg_args.get("cmap")
    
    if change == "Explained by: Perceptions of corruption":
        df.plot.scatter(x = "Happiness score", y = "Explained by: Freedom to make life choices", ax = ax, cmap = "plasma")
        ax.set_title("Effect of Liberality on Happiness")
        ax.set_xlabel("Overall Happiness Score of Country")
        ax.set_ylabel("Happiness Based on Freedom to Make Life Choices (0-1)")
    else:
        df.plot.scatter(x = "Happiness score", y = "Explained by: Freedom to make life choices", ax = ax, color = "black")
        ax.set_title("Effect of Liberality on Happiness")
        ax.set_xlabel("Overall Happiness Score of Country")
        ax.set_ylabel("Happiness Based on Freedom to Make Life Choices (0-1)")
    
    f = StringIO()
    fig.savefig(f, format = "svg")
    plt.close(fig)
    svg = f.getvalue()
    hdr = {"Content-Type": "image/svg+xml"}
    return Response(svg, headers=hdr)

@app.route('/plot2.svg')
def svg_2():
    global df
    fig, ax = plt.subplots()
    
    df.plot.scatter(x = "Happiness score", y = 'Dystopia (1.83) + residual', ax = ax, color = "red")
    ax.set_title("Happiness Score of Nations Compared to their Dystopia Score")
    ax.set_xlabel("Overall Happiness Score of Country")
    
    f = StringIO()
    fig.savefig(f, format = "svg")
    plt.close(fig)
    svg = f.getvalue()
    hdr = {"Content-Type": "image/svg+xml"}
    return Response(svg, headers=hdr)

counter = 0
@app.route('/')
def home():
    global counter
    global vers_a
    global vers_b
    with open("index.html") as f:
        html = f.read()
        
        if counter < 10:
            counter += 1
            if (counter % 2) == 0:
                html = html.replace("<a href=\"donate.html\">donate!</a>", "<a href=\"donate.html?from=A\" style=\"color:green\">donate!</a>")
            else:
                html = html.replace("<a href=\"donate.html\">donate!</a>", "<a href=\"donate.html?from=B\" style=\"color:red\">donate!</a>")
        else:
            if vers_a > vers_b:
                html = html.replace("<a href=\"donate.html\">donate!</a>", "<a href=\"donate.html?from=A\" style=\"color:green\">donate!</a>")
            else:
                html = html.replace("<a href=\"donate.html\">donate!</a>", "<a href=\"donate.html?from=B\" style=\"color:red\">donate!</a>")        
    return html

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.