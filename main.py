import pymysql
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
db = pymysql.connect(host='localhost', port=3306, user='root',
                     password='kms900326', db='library', charset='utf8')
cursor = db.cursor()


@app.route("/save", methods=["GET"])
def save_page():
    return render_template('save.html')


@app.route("/list", methods=["GET"])
def list_page():
    return render_template('list.html')


@app.route("/contents", methods=["POST"])
def save_review():
    req = request.get_json()
    name = req["name"]
    date = req["date"]
    contents_type = req["type"]
    score = req["score"]
    review = req["review"]
    sql = (
        f"INSERT INTO review (name, date, type, score, review) VALUES ('{name}', '{date}', '{contents_type}', '{score}', '{review}')")
    cursor.execute(sql)
    db.commit()
    return "OK"


@app.route("/contents", methods=["GET"])
def list_review():
    read_sql = "SELECT * FROM review"
    cursor.execute(read_sql)
    reviews = cursor.fetchall()
    results = []
    for review in reviews:
        results.append({
            "id": review[0],
            "name": review[1],
            "date": review[2],
            "type": review[3],
            "score": review[4],
            "review": review[5],
        })

    return jsonify(results)


@app.route("/contents", methods=["PUT"])
def update_review():
    req = request.get_json()
    index = req["id"]
    score = req["score"]
    review = req["review"]
    sql = f"UPDATE review SET score = {score}, review = '{review}' where id = {index}"
    cursor.execute(sql)
    db.commit()
    return "OK"


@app.rout("/contents/stat", methods=["GET"])
def get_review_score():
    sql = "SELECT type, count(1), round(avg(grade), 1) from review group by type"
    cursor.execute(sql)
    res = cursor.fetchall()

    dict = {}
    for group in res:
        r_type = group[0]
        cnt_type = group[1]
        avg_type = group[2]
        dict[r_type] = [cnt_type, avg_type]

    return jsonify(dict)


if __name__ == '__main__':
    app.run(debug=True)
