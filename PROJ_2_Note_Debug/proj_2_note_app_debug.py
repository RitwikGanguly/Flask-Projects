from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employee.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form["name"]
        title = request.form["title"]
        desc = request.form["desc"]
        note = User(name=name, title=title, desc=desc)
        db.create_all() # as the table is not created so far in db
        db.session.add(note)
        db.session.commit()

    allNote = User.query.all()
    return render_template('index.html', allNote=allNote)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == "POST":
        name = request.form["name"]
        title = request.form['title']
        desc = request.form['desc']
        note = User.query.filter_by(sno=sno).first()
        note.name = name
        note.title = title
        note.desc = desc
        db.session.add(note)
        db.session.commit()
        return redirect("/")

    to_note = User.query.filter_by(sno=sno).first()
    return render_template('update.html', note=to_note)


@app.route('/delete/<int:sno>')
def delete(sno):
    note = User.query.filter_by(sno=sno).first()
    db.session.delete(note)
    db.session.commit()
    return redirect("/")


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)