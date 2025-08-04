from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'ecommerce.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# 1. Get all orders for a specific customer
@app.route('/customers/<int:customer_id>/orders', methods=['GET'])
def get_orders_for_customer(customer_id):
    conn = get_db_connection()

    # Check if customer exists
    customer = conn.execute('SELECT * FROM users WHERE id = ?', (customer_id,)).fetchone()
    if not customer:
        conn.close()
        return jsonify({'error': 'Customer not found'}), 404

    # Get their orders
    orders = conn.execute('SELECT * FROM orders WHERE user_id = ?', (customer_id,)).fetchall()
    conn.close()
    return jsonify([dict(order) for order in orders]), 200

# 2. Get a specific order by order_id
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    conn = get_db_connection()
    order = conn.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,)).fetchone()
    conn.close()

    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(dict(order)), 200

# 3. Handle errors globally
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)


