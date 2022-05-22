from create_app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    price = db.Column(db.Integer)
    description = db.Column(db.String(1024))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    img_path = db.Column(db.String(128))
    category = db.relationship('Categories',
                               backref="prods")

    def __repr__(self):
        return str(self.title)


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    user = db.relationship('User',
                           backref="comments")
    product = db.relationship('Products',
                              backref="comments")


db.create_all()
