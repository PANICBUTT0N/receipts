import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify, request
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


@app.route('/api/get_all_receipts', methods=['GET'])
def get_all_receipts():
	conn = connect_to_db()
	cur = conn.cursor()
	cur.execute('SELECT * FROM receipts')
	rows = cur.fetchall()
	cur.close()
	conn.close()

	receipts = [{'id': row[0], 'item': row[1], 'store': row[2],'price': row[3],'date': row[4]} for row in rows]
	return jsonify(receipts)


@app.route('/api/add_receipt', methods=['POST'])
def add_receipt():
	data = request.json
	item = data.get('item')
	price = data.get('price')

	conn = connect_to_db()
	cur = conn.cursor()
	cur.execute("INSERT INTO receipts (item, price) VALUES (%s, %s)",
	            (item, price))
	conn.commit()
	cur.close()
	conn.close()
