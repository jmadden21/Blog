from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        new_post = Post(title=post_title, content=post_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')


@app.route('/advertise')
def advertise():
    return render_template('advertise.html', title='Advertise with Us')


if __name__ == '__main__':
    app.run(debug=True)
