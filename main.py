from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():
    blogs = Blog.query.order_by(Blog.id).all()

    return render_template('homepage.html', blogs = blogs)

@app.route('/newpost',methods=['POST', 'GET'])
def newpost():
    
    return render_template('newpost.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    title = request.form['title']
    blog = request.form['blog']
    title_error = ''
    blog_error = ''
    if title == '':
        title_error = "You can't make a blog without a cool title."
    if blog == '':
        blog_error = "You forgot to enter a blog!"
    body = request.form['blog']
    new_blog = Blog(title, body)
    db.session.add(new_blog)
    db.session.commit()

    
    if title_error == '' and blog_error == '':
        return render_template('blog.html', title=title, blog=blog)
    else:
        return render_template('newpost.html', title_error = title_error, blog_error = blog_error, title_return = title, blog_return = blog)

@app.route('/pull_blog', methods=['POST', 'GET'])
def pull_blog():
    id = request.args.get('id')
    blog = Blog.query.filter_by(id=id).first()
    
    return render_template('blog.html', title= blog.title, blog = blog.body)

if __name__ == '__main__':
    app.run()