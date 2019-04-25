from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __init__(self, title, body, owner_id):
        self.title = title
        self.body = body
        self.owner = owner

@app.route('/', methods=['POST', 'GET'])
def index():
    blogs = Blog.query.order_by(Blog.id).all()

    return render_template('homepage.html', blogs = blogs)

@app.route('/newpost',methods=['POST', 'GET'])
def newpost():
    
    return render_template('newpost.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.method == "POST":
        title = request.form['title']
        blog = request.form['blog']
        user = request.form['user']
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
        id = new_blog.id

        return redirect ('/pull_blog?id='+str(id))
    else:
        return render_template('newpost.html', title_error = title_error, blog_error = blog_error, title_return = title, blog_return = blog)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        
        password = request.form['password']
        user = User.query.filter_by(id=id).first()
        if user and user.password == password:
            session['user'] = user
            flash("Logged in")
            return redirect('/')
        else:
            flash('User Password Incorrect OR User Does Not EXIST', 'error')

    return render_template('login.html')

@app.route('/pull_blog', methods=['POST', 'GET'])
def pull_blog():
    id = request.args.get('id')
    blog = Blog.query.filter_by(id=id).first()
    
    return render_template('blog.html', title= blog.title, blog = blog.body)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = username
            return redirect('/')
        else:
            # TODO - user better response messaging
            return "<h1> Duplicate user</h1>"

    return render_template('signup.html')



if __name__ == '__main__':
    app.run()