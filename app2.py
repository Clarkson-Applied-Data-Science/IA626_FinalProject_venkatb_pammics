import configdbms
import configserver
import ollama
import json
from flask import Flask, request
import pymysql
import time

app = Flask(__name__)


def make_conn():
    try:
        conn = pymysql.connect(
            host=configdbms.mysql["host"],
            port=configdbms.mysql["port"],
            user=configdbms.mysql["user"],
            passwd=configdbms.mysql["password"],
            db=configdbms.mysql["database"],
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print("Database connection error:", str(e))
        return None



def check_key(req):
    key = req.args.get("key")
    return key in configserver.server["allowed_keys"]



@app.route("/", methods=['GET','POST'])
def root():
    res = {'msg': 'news_articles Flask API running', 'status': 'ok'}
    return json.dumps(res, indent=4)

@app.route("/runQuery", methods=['GET'])
def runQuery():
    res = {'req': 'runQuery'}
    try:
        
        if not check_key(request):
            return json.dumps({"code": 0, "msg": "auth error"}, indent=4)

        
        user_word = request.args.get('q')
        if not user_word:
            return json.dumps({"code": 0, "msg": "q must be provided"}, indent=4)

        
        prompt = f"""
You are an SQL generator.

User input: "{user_word}"

TASK:
1. Generate EXACTLY 5 related single-word keywords (keep them internal, DO NOT OUTPUT THEM).
2. Return ONLY ONE THING: a single MySQL SQL statement.
3. The SQL MUST:
   - Use table ia626_articles
   - Select url
   - Search column article_body using LIKE for all 5 generated keywords
   - Contain ONLY the SQL (NO explanation, NO list, NO comments)
   - End with LIMIT 10

STRICT OUTPUT RULE:
Return ONLY this pattern, with real keywords inserted:

SELECT url FROM ia626_articles
WHERE article_body LIKE '%word1%'
OR article_body LIKE '%word2%'
OR article_body LIKE '%word3%'
OR article_body LIKE '%word4%'
OR article_body LIKE '%word5%'
LIMIT 10;
"""


        llm = ollama.generate(
            model="llama3.1",
            prompt=prompt,
            stream=False
        )

        
        sql_generated = llm["response"]
        sql_generated = sql_generated.replace("```sql", "").replace("```", "")
        sql_generated = sql_generated.replace("\n", " ").replace("\r", " ")
        sql_generated = " ".join(sql_generated.split())

       
        conn = make_conn()
        if conn is None:
            return json.dumps({"code": 0, "msg": "database connection failed"}, indent=4)

        cur = conn.cursor(pymysql.cursors.DictCursor)

        start = time.time()
        cur.execute(sql_generated)
        sqltime = time.time() - start

        rows = cur.fetchall()

        
        return json.dumps({
            "code": 1,
            "msg": "ok",
            "input": user_word,
            "sql": sql_generated,
            "sqltime": sqltime,
            "num_results": len(rows),
            "results": rows
        }, indent=4, default=str)

    except Exception as e:
        return json.dumps({
            "code": 0,
            "msg": "error: " + str(e),
            "sqltime": 0
        }, indent=4)


if __name__ == "__main__":
    print("Flask server starting → /runQuery is active")
    app.run(host="0.0.0.0", port=5000, debug=True)
