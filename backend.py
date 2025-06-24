import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)


def connect_to_db():
	conn = psycopg2.connect(
		dbname=os.getenv('DB_NAME'),
		user=os.getenv('DB_USER'),
		password=os.getenv('DB_PASSWORD'),
		host=os.getenv('DB_HOST'),
		port=os.getenv('DB_PORT')
	)
	return conn


@app.route('/api/receipts', methods=['GET'])
def get_receipts():
	conn = connect_to_db()
	cur = conn.cursor()
	cur.execute('SELECT * FROM receipts')
	rows = cur.fetchall()
	cur.close()
	conn.close()

	receipts = [{'id': row[0], 'name': row[1], 'email': row[2]} for row in rows]
	return jsonify(receipts)
