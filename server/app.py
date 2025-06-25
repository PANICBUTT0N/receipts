import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, render_template, request
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
	return render_template('index.html')


def connect_to_db():
	conn = psycopg2.connect(
			dbname=os.getenv('DB_NAME'),
			user=os.getenv('DB_USER'),
			password=os.getenv('DB_PASSWORD'),
			host=os.getenv('DB_HOST'),
			port=os.getenv('DB_PORT')
	)
	return conn


@app.route('/api/build_schema', methods=['POST'])
def build_schema():
	conn = connect_to_db()
	cur = conn.cursor()
	cur.execute(
			'CREATE TABLE receipts(id SERIAL PRIMARY KEY,'
			'item TEXT,'
			'store TEXT,'
			'price MONEY,'
			'date TIMESTAMP,'
			'image_path TEXT)')
	conn.commit()
	cur.close()
	conn.close()
	return make_response(jsonify({'message': 'Schema built successfully'}), 201)

@app.route('/api/get_receipt', methods=['GET'])
def get_receipt():
	receipt_id = request.args.get('receipt_id')

	conn = connect_to_db()
	cur = conn.cursor()
	cur.execute('SELECT * FROM receipts WHERE id = %s', receipt_id)
	rows = cur.fetchall()
	cur.close()
	conn.close()

	receipts = [{
			'id':         row[0],
			'item':       row[1],
			'store':      row[2],
			'price':      row[3],
			'date':       row[4],
			'image_path': row[5]} for row in rows]
	return make_response(jsonify(receipts), 200)

@app.route('/api/get_all_receipts', methods=['GET'])
def get_all_receipts():
	conn = connect_to_db()
	cur = conn.cursor()
	cur.execute('SELECT * FROM receipts')
	rows = cur.fetchall()
	cur.close()
	conn.close()

	receipts = [{
			'id':         row[0],
			'item':       row[1],
			'store':      row[2],
			'price':      row[3],
			'date':       row[4],
			'image_path': row[5]} for row in rows]
	return make_response(jsonify(receipts), 200)


@app.route('/api/add_receipt', methods=['POST'])
def add_receipt():
	data = request.json
	item = data.get('item')
	store = data.get('store')
	price = data.get('price')
	date = data.get('date')
	image_path = data.get('image_path')

	conn = connect_to_db()
	cur = conn.cursor()
	cur.execute(
			"INSERT INTO receipts (item, store, price, date, image_path) VALUES (%s, %s)",
			(item, store, price, date, image_path))
	conn.commit()
	cur.close()
	conn.close()

	return make_response(jsonify({'message': 'Receipt added successfully'}), 201)
