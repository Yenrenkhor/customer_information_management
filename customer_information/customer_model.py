from flask_sqlalchemy import SQLAlchemy

customer_db = SQLAlchemy()


class Customer(customer_db.Model):
    __tablename__ = 'customer'
    id = customer_db.Column(customer_db.Integer, primary_key=True)
    first_name = customer_db.Column(customer_db.String(), nullable=False)
    last_name = customer_db.Column(customer_db.String(), nullable=False)
    email = customer_db.Column(customer_db.String(), nullable=False)
    phone = customer_db.Column(customer_db.String(), nullable=False)
    address = customer_db.Column(customer_db.String(), nullable=False)

    def __init__(self, first_name, last_name, email, phone, address):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address

    def to_dict(self):
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "phone": self.phone,
                "address": self.address}
