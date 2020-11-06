from flask import request
from bs4 import BeautifulSoup as bs
import requests
from flask import Flask

app = Flask(__name__)


@app.route('/list')
def hello_world():
    all_curr_page = requests.get("http://www.cbr.ru/scripts/XML_valFull.asp").text
    parser = bs(all_curr_page, features="lxml")
    return {"currencies": list(zip([name.text for name in parser.find_all("name")],
                   [code.text for code in parser.find_all("iso_char_code")]))}


def convert_date(date):
    result = date.split("-")
    result.reverse()
    return "-".join(result)


@app.route('/difference')
def get_difference():
    start_date = convert_date(request.args.get("start_date"))
    end_date = request.args.get("end_date")
    currency = request.args.get("currency")

    start_currencies = requests.get("http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + start_date).text
    end_currencies = requests.get("http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + end_date).text

    start_curr_value = bs(start_currencies, features="lxml").find("charcode", string=currency).parent
    start_rate = float(start_curr_value.find("value").string.replace(",", ".")) / float(start_curr_value.find("nominal").string.replace(",", "."))
    end_curr_value = bs(end_currencies, features="lxml").find("charcode", string=currency).parent
    end_rate = float(end_curr_value.find("value").string.replace(",", ".")) / float(end_curr_value.find("nominal").string.replace(",", "."))

    return {"start_rate": start_rate,
            "end_rate": end_rate,
            "rate_difference": start_rate - end_rate}
