import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = os.urandom(24)  # Generate a random secret key
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
        session['temp_post'] = {
            'title': request.form['title'],
            'content': request.form['content']
        }
        return redirect(url_for('preview_post'))

    posts = Post.query.all()  # Fetch all posts from the database
    return render_template('create_post.html', posts=posts)


@app.route('/preview_post', methods=['GET', 'POST'])
def preview_post():
    if request.method == 'POST':
        # Save the post from the session to the database
        new_post_data = session.get('temp_post')
        if new_post_data:
            new_post = Post(title=new_post_data['title'], content=new_post_data['content'])
            db.session.add(new_post)
            db.session.commit()
            session.pop('temp_post', None)  # Clear the temporary post from the session
            return redirect(url_for('create_post'))

    return render_template('preview_post.html', post=session.get('temp_post'))


@app.route("/delete_post/<int:post_id>")
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('create_post'))


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')


@app.route('/advertise')
def advertise():
    return render_template('advertise.html', title='Advertise with Us')


if __name__ == '__main__':
    app.run(debug=True)
