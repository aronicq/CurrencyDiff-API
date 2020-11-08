import time

from flask import request, render_template
from bs4 import BeautifulSoup as bs, Tag
import requests
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list')
def hello_world():
    all_curr_page = requests.get("http://www.cbr.ru/scripts/XML_valFull.asp").text
    parser = bs(all_curr_page, features="html5lib")
    all_names = parser.find_all("name")
    all_codes = parser.find_all("iso_char_code")

    res = [{"name": all_names[i].string,
            "code": all_codes[i].string} for i in range(len(all_names))]
    return {"currencies": res}


def convert_date(date):
    result = date.split("-")
    result.reverse()
    return "-".join(result)


@app.route('/difference')
def get_difference():
    start_date = convert_date(request.args.get("start_date"))
    end_date = convert_date(request.args.get("end_date"))
    currency = request.args.get("currency")
    start_curr_value = end_curr_value = Tag(name="tag")
    start_currencies = requests.get("http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + start_date).text
    end_currencies = requests.get("http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + end_date).text
    try:
        start_curr_value = bs(start_currencies, features="html5lib").find("charcode", string=currency).parent
        end_curr_value = bs(end_currencies, features="html5lib").find("charcode", string=currency).parent
    except AttributeError:
        print(start_currencies)
        print(start_date)
        print(end_currencies)
        print(end_date)

    start_rate = float(start_curr_value.find("value").string.replace(",", ".")) / float(
        start_curr_value.find("nominal").string.replace(",", "."))
    end_rate = float(end_curr_value.find("value").string.replace(",", ".")) / float(
        end_curr_value.find("nominal").string.replace(",", "."))

    return {"start_rate": start_rate,
            "end_rate": end_rate,
            "rate_difference": '{:.1f}'.format(start_rate - end_rate)}

