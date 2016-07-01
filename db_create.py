#!flask/bin/python
from app import db
from app import User
from app import Item
from app import Order
from app import Orderrow

db.create_all()

#prep
u = User(username='john.doe@email.com', name='John Doe', address='homeaddress', postalCode='00100', city='Helsinki')
i1 = Item(productId='1001', productName='Shovel', productPrice='1.1')
i2 = Item(productId='2002', productName='Bucket', productPrice='2.5')
o = Order()
or1 = Orderrow(count='2')
or2 = Orderrow(count='3')

#append
i1.productRow.append(or1)
i2.productRow.append(or2)
o.orderrow.append(or1)
o.orderrow.append(or2)
u.order.append(o)

#add
db.session.add(u)
db.session.add(i1)
db.session.add(i2)
db.session.add(o)
db.session.add(or1)
db.session.add(or2)

#commit
db.session.commit()
