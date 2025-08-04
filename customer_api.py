from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__, static_folder="static", template_folder="templates")

DATABASE = 'ecommerce.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# 1. List all customers with optional pagination
@app.route('/customers', methods=['GET'])
def get_all_customers():
    limit = request.args.get('limit', 10)
    offset = request.args.get('offset', 0)

    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM users LIMIT ? OFFSET ?', (limit, offset)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in customers]), 200

# 2. Get customer by ID including order count
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    conn = get_db_connection()

    customer = conn.execute('SELECT * FROM users WHERE id = ?', (customer_id,)).fetchone()
    if not customer:
        conn.close()
        return jsonify({'error': 'Customer not found'}), 404

    order_count = conn.execute('SELECT COUNT(*) as count FROM orders WHERE user_id = ?', (customer_id,)).fetchone()
    conn.close()

    customer_data = dict(customer)
    customer_data['order_count'] = order_count['count']
    return jsonify(customer_data), 200

# 3. Handle 404 errors for invalid URLs
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

# 4. Handle 500 internal errors
@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)

from flask import render_template

@app.route('/')
def home():
    return render_template('index.html')


