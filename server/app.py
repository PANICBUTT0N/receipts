import json
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, render_template, request
from flask_cors import CORS
from psycopg2 import pool

load_dotenv()
app = Flask(__name__)
CORS(app)

# Initialize connection pool
db_pool = pool.SimpleConnectionPool(
		minconn=1,
		maxconn=10,
		dbname=os.getenv('DB_NAME'),
		user=os.getenv('DB_USER'),
		password=os.getenv('DB_PASSWORD'),
		host=os.getenv('DB_HOST'),
		port=os.getenv('DB_PORT')
)


def connect_to_db():
	return db_pool.getconn()


def release_db(conn):
	db_pool.putconn(conn)


@app.route('/')
def home():
	return render_template('index.html')


@app.route('/receipt/<int:receipt_id>')
def receipt_detail(receipt_id):
	return render_template('receipt.html', receipt_id=receipt_id)


@app.route('/api/build_schema', methods=['POST'])
def build_schema():
	conn = connect_to_db()
	cur = conn.cursor()
	cur.execute(
			'CREATE TABLE receipts (id SERIAL PRIMARY KEY,'
			'date TIMESTAMP,'
			'items JSONB,'
			'total MONEY,'
			'store TEXT,'
			'address TEXT,'
			'phone TEXT,'
			'payment_method TEXT,'
			'image_path TEXT);')
	conn.commit()
	cur.close()
	release_db(conn)
	return make_response(jsonify({'message': 'Schema built successfully'}), 201)


@app.route('/api/get_receipt', methods=['GET'])
def get_receipt():
	receipt_id = request.args.get('receipt_id')

	conn = connect_to_db()
	cur = conn.cursor()
	cur.execute('SELECT * FROM receipts WHERE id = %s', (receipt_id,))
	row = cur.fetchall()
	cur.close()
	release_db(conn)

	receipts = {
			'id':             row[0],
			'date':           row[1],
			'items':          row[2],
			'total':          row[3],
			'store':          row[4],
			'address':        row[5],
			'phone':          row[6],
			'payment method': row[7],
			'image_path':     row[8]}
	return make_response(jsonify(receipts), 200)


@app.route('/api/get_all_receipts', methods=['GET'])
def get_all_receipts():
	conn = connect_to_db()
	cur = conn.cursor()
	cur.execute('SELECT * FROM receipts')
	rows = cur.fetchall()
	cur.close()
	release_db(conn)

	receipts = [{
			'id':             row[0],
			'date':           row[1],
			'items':          row[2],
			'total':          row[3],
			'store':          row[4],
			'address':        row[5],
			'phone':          row[6],
			'payment_method': row[7],
			'image_path':     row[8]}
			for row in rows]
	return make_response(jsonify(receipts), 200)


@app.route('/api/add_receipt', methods=['POST'])
def add_receipt():
	data = request.json
	date = data.get('date')
	items = data.get('items')
	total = data.get('total')
	store = data.get('store')
	address = data.get('address')
	phone = data.get('phone')
	payment_method = data.get('payment_method')
	image_path = data.get('image_path')

	conn = connect_to_db()
	cur = conn.cursor()
	cur.execute(
			"INSERT INTO receipts (date, items, total, store, address, phone, payment_method, image_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
			(date, json.dumps(items), total, store, address, phone, payment_method, image_path)
	)
	conn.commit()
	cur.close()
	release_db(conn)

	return make_response(jsonify({'message': 'Receipt added successfully'}), 201)
