"""DevOps kurso starteris: paprastas Flask API su SQLite (numatyta) arba MySQL."""
import os
import socket
import sqlite3

from flask import Flask, jsonify, request, send_from_directory

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=None)


def use_mysql():
    return bool(os.environ.get("DB_HOST"))


def connect():
    """Grąžina (ryšys, parametro ženklas). MySQL, jei nustatytas DB_HOST, kitaip SQLite."""
    if use_mysql():
        import pymysql

        conn = pymysql.connect(
            host=os.environ["DB_HOST"],
            port=int(os.environ.get("DB_PORT", "3306")),
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            database=os.environ["DB_NAME"],
            connect_timeout=3,
        )
        return conn, "%s"
    path = os.environ.get("SQLITE_PATH", os.path.join(BASE, "app.db"))
    return sqlite3.connect(path), "?"


def run_sql_file(cur, name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        for stmt in f.read().split(";"):
            if stmt.strip():
                cur.execute(stmt)


def init_db():
    """Sukuria lentelę ir įkelia pradinius duomenis, jei lentelė tuščia."""
    conn, _ = connect()
    try:
        cur = conn.cursor()
        run_sql_file(cur, "schema.mysql.sql" if use_mysql() else "schema.sqlite.sql")
        cur.execute("SELECT COUNT(*) FROM items")
        if cur.fetchone()[0] == 0:
            run_sql_file(cur, "seed.sql")
        conn.commit()
    finally:
        conn.close()


@app.route("/health")
def health():
    return {"status": "ok"}, 200


@app.route("/status")
def status():
    try:
        conn, _ = connect()
        conn.cursor().execute("SELECT 1")
        conn.close()
        db = "up"
    except Exception:
        db = "down"
    return jsonify(
        version=os.environ.get("APP_VERSION", "dev"),
        color=os.environ.get("APP_COLOR", "blue"),
        env=os.environ.get("APP_ENV", "local"),
        hostname=socket.gethostname(),
        db=db,
        db_type="mysql" if use_mysql() else "sqlite",
    )


@app.get("/items")
def list_items():
    conn, _ = connect()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM items ORDER BY id")
        return jsonify([{"id": i, "name": n} for i, n in cur.fetchall()])
    finally:
        conn.close()


@app.post("/items")
def add_item():
    name = str((request.get_json(silent=True) or {}).get("name", "")).strip()
    if not name or len(name) > 100:
        return jsonify(error="reikia pavadinimo (iki 100 simbolių)"), 400
    conn, ph = connect()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO items (name) VALUES (%s)" % ph, (name,))
        conn.commit()
        return jsonify(id=cur.lastrowid, name=name), 201
    finally:
        conn.close()


@app.route("/")
def index():
    return send_from_directory(os.path.join(BASE, "static"), "index.html")


init_db()
