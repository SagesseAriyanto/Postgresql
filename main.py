from flask import Flask, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = 'ASKDLJFLASJFDLJ'

os.makedirs('instance', exist_ok=True)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "instance", "data.db")}'

bootstrap = Bootstrap5(app)

# Create database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(db.Model):
    __tablename__ = "Registered Users"
    id: Mapped[int]= mapped_column(Integer, primary_key=True)
    username: Mapped[str]= mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "age": self.age
        }


with app.app_context():
    db.create_all()

class userForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    submit = SubmitField('Submit')
    get_users = SubmitField('Get Users')


@app.route("/", methods=["GET", "POST"])
def home():
    form = userForm()
    if form.validate_on_submit():
        if form.submit.data:
            user = User(
                username=form.username.data,
                age=int(form.age.data)
            )
            db.session.add(user)
            db.session.commit()
            flash('User added successfully!')
            return redirect(url_for('home'))
        elif form.get_users.data:
            return redirect(url_for('get_users'))
    return render_template('index.html', form=form)

@app.route("/users")
def get_users():
    users = db.session.execute(db.select(User)).scalars().all()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)
    

if __name__ == '__main__':
    app.run(debug=True)