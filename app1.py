import config
import json, pymysql, time
from flask import Flask, request

app = Flask(__name__)


def make_conn():
    try:
        conn = pymysql.connect(
            host=config.mysql["host"],
            port=config.mysql["port"],
            user=config.mysql["user"],
            passwd=config.mysql["password"],
            db=config.mysql["database"],
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print("Database connection error:", str(e))
        return None



@app.before_request
def global_auth():
    if request.path == "/":
        return
    key = request.args.get("key")
    if key != config.api['key']:
        res = {
            "req": request.path,
            "code": 0,
            "msg": "auth error"
        }
        return json.dumps(res, indent=4), 401



@app.route("/", methods=['GET','POST'])
def root():
    res = {"msg": "News Search API running", "status": "ok"}
    return json.dumps(res, indent=4)


@app.route("/ByKeyword", methods=['GET','POST'])
def ByKeyword():
    res = {"req": "ByKeyword"}

    try:
        keyword = request.args.get("keyword")
        if not keyword:
            res["code"] = 0
            res["msg"] = "keyword must be provided"
            return json.dumps(res, indent=4)

        conn = make_conn()
        if conn is None:
            res["code"] = 0
            res["msg"] = "database connection failed"
            return json.dumps(res, indent=4)

        cur = conn.cursor()

        sql = """
            SELECT a.article_id, a.url, a.title
            FROM ia626_articles a
            JOIN ia626_article_keywords ak ON a.article_id = ak.article_id
            JOIN ia626_keywords k ON ak.keyword_id = k.keyword_id
            WHERE k.keyword = %s
            LIMIT 10;
        """

        start = time.time()
        cur.execute(sql, (keyword,))
        res["sqltime"] = round(time.time() - start, 4)

        rows = cur.fetchall()

        res["code"] = 1
        res["msg"] = "ok"
        res["num_results"] = len(rows)
        res["results"] = rows

        return json.dumps(res, indent=4, default=str)

    except Exception as e:
        res["code"] = 0
        res["msg"] = f"error: {str(e)}"
        res["sqltime"] = 0
        return json.dumps(res, indent=4, default=str)



@app.route("/ByAuthor", methods=['GET','POST'])
def ByAuthor():
    res = {"req": "ByAuthor"}

    try:
        author = request.args.get("name")
        if not author:
            res["code"] = 0
            res["msg"] = "name parameter required"
            return json.dumps(res, indent=4)

        conn = make_conn()
        if conn is None:
            res["code"] = 0
            res["msg"] = "database connection failed"
            return json.dumps(res, indent=4)

        cur = conn.cursor()

        sql = """
            SELECT article_id, url, title, author
            FROM ia626_articles
            WHERE author LIKE %s
            LIMIT 10;
        """

        start = time.time()
        cur.execute(sql, (f"%{author}%",))
        res["sqltime"] = round(time.time() - start, 4)

        rows = cur.fetchall()

        res["code"] = 1
        res["msg"] = "ok"
        res["num_results"] = len(rows)
        res["results"] = rows

        return json.dumps(res, indent=4, default=str)

    except Exception as e:
        res["code"] = 0
        res["msg"] = f"error: {str(e)}"
        res["sqltime"] = 0
        return json.dumps(res, indent=4, default=str)


@app.route("/ByDate", methods=['GET','POST'])
def ByDate():
    res = {"req": "ByDate"}

    try:
        date_str = request.args.get("date")
        if not date_str:
            res["code"] = 0
            res["msg"] = "date parameter required (format: YYYY-MM-DD)"
            return json.dumps(res, indent=4)

        conn = make_conn()
        if conn is None:
            res["code"] = 0
            res["msg"] = "database connection failed"
            return json.dumps(res, indent=4)

        cur = conn.cursor()

        sql = """
            SELECT article_id, url, title, date
            FROM ia626_articles
            WHERE DATE(date) = %s
            ORDER BY date DESC
            LIMIT 10;
        """

        start = time.time()
        cur.execute(sql, (date_str,))
        res["sqltime"] = round(time.time() - start, 4)

        rows = cur.fetchall()

        res["code"] = 1
        res["msg"] = "ok"
        res["num_results"] = len(rows)
        res["results"] = rows

        return json.dumps(res, indent=4, default=str)

    except Exception as e:
        res["code"] = 0
        res["msg"] = "error: " + str(e)
        res["sqltime"] = 0
        return json.dumps(res, indent=4, default=str)



@app.route("/ByCategory", methods=['GET','POST'])
def ByCategory():
    res = {"req": "ByCategory"}

    try:
        category = request.args.get("cat")
        if not category:
            res["code"] = 0
            res["msg"] = "category parameter required"
            return json.dumps(res, indent=4)

        conn = make_conn()
        if conn is None:
            res["code"] = 0
            res["msg"] = "database connection failed"
            return json.dumps(res, indent=4)

        cur = conn.cursor()

        sql = """
            SELECT article_id, url, title, category
            FROM ia626_articles
            WHERE category LIKE %s
            LIMIT 10;
        """

        start = time.time()
        cur.execute(sql, (f"%{category}%",))
        res["sqltime"] = round(time.time() - start, 4)

        rows = cur.fetchall()

        res["code"] = 1
        res["msg"] = "ok"
        res["num_results"] = len(rows)
        res["results"] = rows

        return json.dumps(res, indent=4, default=str)

    except Exception as e:
        res["code"] = 0
        res["msg"] = f"error: {str(e)}"
        res["sqltime"] = 0
        return json.dumps(res, indent=4, default=str)



@app.route("/ByRandom", methods=['GET','POST'])
def ByRandom():
    res = {"req": "ByRandom"}

    try:
        conn = make_conn()
        if conn is None:
            res["code"] = 0
            res["msg"] = "database connection failed"
            return json.dumps(res, indent=4)

        cur = conn.cursor()

        sql = """
            SELECT article_id, url, title
            FROM ia626_articles
            ORDER BY RAND()
            LIMIT 1;
        """

        start = time.time()
        cur.execute(sql)
        res["sqltime"] = round(time.time() - start, 4)

        row = cur.fetchone()

        res["code"] = 1
        res["msg"] = "ok"
        res["results"] = row

        return json.dumps(res, indent=4, default=str)

    except Exception as e:
        res["code"] = 0
        res["msg"] = f"error: {str(e)}"
        res["sqltime"] = 0
        return json.dumps(res, indent=4, default=str)




if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
