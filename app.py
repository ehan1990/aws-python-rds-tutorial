import datetime
import logging
import os
import mysql.connector

from flask import Flask, jsonify, request

# constants
VERSION = "1.0.0"

app = Flask(__name__)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(filename)s:%(lineno)d %(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

db_user = os.environ.get("DB_USER", "root")
db_pw = os.environ.get("DB_PW", "rootroot")
db = mysql.connector.connect(host="localhost", user=db_user, password=db_pw,
                             database="wallstreet")


def db_list_stocks():
    cursor = db.cursor()
    sql_cmd = f"select * from stocks"
    cursor.execute(sql_cmd)
    res = cursor.fetchall()

    stocks = []
    for item in res:
        stock = {"ticker": item[0], "name": item[1]}
        stocks.append(stock)
    return stocks


def db_add_one_stock(ticker, name):
    cursor = db.cursor()
    sql_cmd = f"insert into stocks (ticker, name) values (%s, %s);"
    vals = (ticker, name)
    cursor.execute(sql_cmd, vals)
    db.commit()


@app.route("/stocks", methods=["POST"])
def add_one_stock():
    req_data = request.get_json(force=True)
    ticker = req_data["ticker"]
    name = req_data["name"]
    db_add_one_stock(ticker, name)
    req_data["msg"] = f"added stock {ticker}, {name}"
    return jsonify(req_data), 200


@app.route("/stocks", methods=["GET"])
def list_stocks():
    stocks = db_list_stocks()
    return jsonify(stocks), 200


@app.route("/healthcheck", methods=["GET"])
def healthcheck_endpoint():
    db_connected = db.is_connected()
    data = {
        "msg": f"Running version {VERSION}",
        "date": f"{datetime.datetime.utcnow().isoformat()[0:19]}Z",
        "is_db_connected": db_connected
    }
    return jsonify(data)


def main():
    app.run(host='0.0.0.0', port=8080, threaded=True)


if __name__ == "__main__":
    main()
