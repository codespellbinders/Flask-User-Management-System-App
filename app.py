from flask import Flask, request, render_template
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    time_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'{self.sno} - {self.fname}'
# Create the database
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        user = User(fname=fname, lname=lname)
        db.session.add(user)
        db.session.commit()
    allusers = User.query.all()
    return render_template("home.html", allusers=allusers)

@app.route('/delete/<int:sno>')
def delete(sno):
    user = User.query.filter_by(sno=sno).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("home"))
@app.route('/update/<int:sno>', methods=['GET' , 'POST'])
def update(sno, methods=['GET', 'POST']):
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        user = User.query.filter_by(sno=sno).first()
        user.fname = fname
        user.lname = lname
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
    user = User.query.filter_by(sno=sno).first()
    return render_template("update.html", user=user)
if __name__ == '__main__':
    app.run(debug=True)