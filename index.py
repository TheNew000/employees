from flask import Flask, render_template, jsonify
from flaskext.mysql import MySQL
from flask_cors import CORS

mysql = MySQL()
app = Flask(__name__)
CORS(app)
app.config['MYSQL_DATABASE_USER'] = 'emp_user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'x'
app.config['MYSQL_DATABASE_DB'] = 'sakila'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route('/customers', methods=['GET'])
def customers():
    # query2 = "SELECT CONCAT(customer.first_name, ' ', customer.last_name), address, city, SUM(amount), CONCAT(staff.first_name, ' ', staff.last_name) AS Staff_Name FROM customer INNER JOIN customer_list ON customer.customer_id = customer_list.id INNER JOIN staff ON staff.store_id = customer.store_id INNER JOIN payment ON payment.customer_id = customer_list.id WHERE customer.store_id = 1 GROUP BY payment.customer_id, customer.first_name, staff.first_name, staff.last_name ORDER BY customer.last_name"
    # cursor.execute(query2)
    cursor.execute("SELECT name, address, city, `zip code`, SUM(payment.amount) AS Total, staff.username FROM customer_list LEFT JOIN payment ON customer_list.id = payment.customer_id LEFT JOIN staff ON customer_list.SID = staff.staff_id LEFT JOIN store ON staff.store_id = store.store_id WHERE store.store_id = 1 GROUP BY name, address, city, `zip code`, staff.username")
    bologna = cursor.fetchall()
    result_as_dictionary = dict(bologna)
    return jsonify(**result_as_dictionary)
    # return render_template('customer.html', bologna=bologna)

@app.route('/customers_view')
def customer_view():
    return render_template('/customer.html')


if __name__ == '__main__':
    app.run(debug=True)
