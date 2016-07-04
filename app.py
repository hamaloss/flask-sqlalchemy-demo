#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sales.db'
if 'VCAP_SERVICES' in os.environ:
  import json
  vcap_services = json.loads(os.environ['VCAP_SERVICES'])
  mysql_srv = vcap_services['cleardb'][0]
  cred = mysql_srv['credentials']
  mysql_uri = "mysql+pymysql://"+cred['username']+":"+cred['password']+"@"+cred['hostname']+":"+cred['port']+"/"+cred['name']
  app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
else:
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sales.db'

print(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    postalCode = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    order = db.relationship("Order", backref="customer", lazy="dynamic")

class Item(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    productId = db.Column(db.Integer, nullable=False, unique=True)
    productName = db.Column(db.String, nullable=False)
    productPrice = db.Column(db.Float, nullable=False)
    productRow = db.relationship("Orderrow", backref="itemonrow", lazy="dynamic")

class Order(db.Model):

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String, nullable=False, default="Received")
    orderrow = db.relationship("Orderrow", backref="parentorder", lazy="dynamic")

class Orderrow(db.Model):
    __tablename__ = "orderrow"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    count = db.Column(db.Integer, nullable=False)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( {'error': 'Not found' } ), 404)

@app.route('/report/api/v1.0/orderlist', methods=['GET'])
def get_allOrders():
    orderList = []
    orders = Orderrow.query.all()
    for order in orders:
        thisorderrow = {"rowId":order.id, "user":order.parentorder.customer.name, "item":order.itemonrow.productName, "itemcount":order.count, "belongsToOrder":order.parentorder.id}
        orderList.append(thisorderrow)
    return jsonify(orderList)

@app.route('/report/api/v1.0/ordercount', methods=['GET'])
def get_orderCount():
    orderList = []
    ordercount = Order.query.count()
    oc = {"allTimeOrders":ordercount}
    return jsonify(oc)

@app.route('/report/api/v1.0/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    orderList = []
    orders = Order.query.filter_by(id = order_id).all()
    for order in orders:
        orderList.append({"order id":order.id, "Customer":order.customer.name })
    
    if len(orderList) == 0:
        abort(404)
    
    return jsonify(orderList)

@app.route('/report/api/v1.0/neworder', methods=['POST'])
def new_order():
    if not request.json or not 'userName' in request.json or not 'name' in request.json or not 'streetAddress' in request.json or not 'postNumber' in request.json or not 'city' in request.json or not 'items' in request.json:
        abort(400)

    u = User.query.filter_by(username=request.json['userName']).first()
    if u is None:
        u = User(username=request.json['userName'], name=request.json['name'], address=request.json['streetAddress'], postalCode=request.json['postNumber'], city=request.json['city'])
    db.session.add(u)
    o = Order()
    db.session.add(o)

    for item in request.json['items']:
        i = Item.query.filter_by(productId = item['productid']).first()
        if i is None:
            i = Item(productId=item['productid'], productName=item['productname'], productPrice=item['productprice'])
        db.session.add(i)
        row = Orderrow(count=item['count'])
        i.productRow.append(row)
        o.orderrow.append(row)
        db.session.add(row)

    u.order.append(o)
    db.session.commit()

    return jsonify({'order': 'created'}), 201

if __name__ == '__main__':
    app.run(debug=True)
