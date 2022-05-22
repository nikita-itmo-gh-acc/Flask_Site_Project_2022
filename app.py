from flask import render_template, redirect, url_for, request
from forms import RegisterForm, LoginForm, SearchForm
from create_app import app, db, login_manager, migrate
from models import User, Products, Categories
from flask_login import login_user, logout_user, login_required, current_user
from websockets_serv import start_websocket_server
import threading


@app.route('/')
def index():
    p = Products.query.filter_by(id=1).first()
    return render_template("index.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_name, new_email, password = form.data["username"], form.data["email"], form.data["password"]
        if len(list(User.query.filter_by(email=new_email))) > 0:
            print("такой email уже зарегистрирован")
        else:
            new_user = User(name=new_name, email=new_email, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("index"))
    return render_template("register.html", form=form)


@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email, password = form.data["email"], form.data["password"]
        if list(User.query.filter_by(email=email)):
            user = User.query.filter_by(email=email)[0]
            if user.password == password:
                login_user(user)
                return redirect(url_for("index"))
            else:
                print("неверный пароль")
        else:
            print("пользователь не зарегистрирован")
    return render_template("login.html", form=form)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route("/catalog", methods=["POST", "GET"])
def catalog():
    categories = list(Categories.query.all())
    form = SearchForm()
    form.categories.choices = list()
    form.categories.choices.append("all")
    form.categories.choices += [categories[i].title for i in range(len(categories))]
    showed = list()
    if request.method == "POST":
        search = form.data["search"]
        category = form.data["categories"]
        if category == "all":
            if search:
                showed = list(Products.query.filter_by(title=search))
            else:
                showed = Products.query.all()
        else:
            if search:
                benefit = list(Products.query.filter_by(title=search))
                for p in benefit:
                    if p.category.title == category:
                        showed.append(p)
            else:
                category_obj = Categories.query.filter_by(title=category).first()
                showed = list(Products.query.filter_by(category_id=category_obj.id))
    else:
        showed = Products.query.all()
    return render_template("catalog.html", prods=showed, form=form)


@app.route("/product/<int:product_id>")
@login_required
def product(product_id):
    prod = Products.query.filter_by(id=product_id).first()
    return render_template("product.html", prod=prod)


if __name__ == "__main__":
    sock_thread = threading.Thread(target=start_websocket_server)
    sock_thread.start()
    app.run(debug=True, port=5051, use_reloader=False, host='0.0.0.0')
