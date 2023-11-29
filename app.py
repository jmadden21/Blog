from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    posts = [
        {"title": "First Post", "content": "This is the content of my first post"},
        {"title": "Second Post", "content": "This is the content of my second post"}
    ]
    return render_template('home.html', posts=posts)


@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        # Handle the form submission
        title = request.form['title']
        content = request.form['content']
        print("New Post Created:", title, content)
        # Later, you'll save this data to a database

        return redirect(url_for('home'))  # Redirect to the home page after submission

    return render_template('create_post.html')  # Render the form page for GET requests


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')


@app.route('/advertise')
def advertise():
    return render_template('advertise.html', title='Advertise with Us')


if __name__ == '__main__':
    app.run(debug=True)
