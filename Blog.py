from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    posts = [
        {"title": "First Post", "content": "This is the content of my first post"},
        {"title": "Second Post", "content": "This is the content of my second post"}
    ]
    return render_template('home.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)
