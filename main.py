from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi


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
    blogs = db.relationship('Blog', backref='user', lazy = True)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    

    def __init__(self, title, body, user_id):
        self.title = title
        self.body = body
        self.user_id = user_id


#@app.before_request
#def require_login():
#    allowed_routes = ['login', 'signup', 'user_specifit_blogs', 'homepage', 'listofusers']
#    if request.endpoint not in allowed_routes and 'user' not in session:
#        return redirect('/login')


@app.route('/justblogs', methods=['POST', 'GET'])
def index():
    blogs = Blog.query.order_by(Blog.id).all()
    user = User.query.order_by(User.username).all()
    
    #user = User.query.order_by(User.id).first()
    return render_template('homepage.html', blogs = blogs, user = user)

@app.route('/userblogs', methods=['POST', 'GET'])
def useblogs():
    id = request.args.get('id')
    user = User.query.filter_by(id = id).first()
    #user = user.username
    blogs = Blog.query.filter_by(user_id = id).all()
    return render_template('user_specific_blogs.html', blogs = blogs, user = user)

@app.route('/', methods=['POST', 'GET'])
def userlist():
    users = User.query.order_by(User.id).all()

    return render_template('listofusers.html', users = users)

@app.route('/newpost',methods=['POST', 'GET'])
def newpost():
    
    return render_template('newpost.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if 'user' not in session:
        flash('You must LOG in to BLOG in.', 'error')
        return redirect ('/login')

    if request.method == "POST":
        title = request.form['title']
        blog = request.form['blog']
        #username = session['user']
            
        user = User.query.filter_by(id = session['user']).first()
        #item = db.session.query(Parts.id).filter(name=form.name.data).one()
            
        user_id = user.id

        title_error = ''
        blog_error = ''
        if title == '':
            title_error = "You can't make a blog without a cool title."
        if blog == '':
            blog_error = "You forgot to enter a blog!"
        body = request.form['blog']
            

        
    if title_error == '' and blog_error == '':
           
        new_blog = Blog(title, body, user_id)
        db.session.add(new_blog)
        db.session.commit()
        id = new_blog.id
        return redirect ('/pull_blog?id='+str(id))
    else:
        return render_template('newpost.html', title_error = title_error, blog_error = blog_error, title_return = title, blog_return = blog)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user'] = user.id
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User Password Incorrect OR User Does Not EXIST', 'error')

    return render_template('login.html')

@app.route('/pull_blog', methods=['POST', 'GET'])
def pull_blog():
    id = request.args.get('id')
    
    blog = Blog.query.filter_by(id=id).first()
    user = User.query.filter_by(id = id).first()
    return render_template('blog.html', title= blog.title, blog = blog.body, id = id, user = user)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        verify = request.form['verify']

        #VERIFY PASSWORD
        passerror = ""
        matcherror = ""
    
        if password != verify:
            matcherror = "Your passwords did not match."
     
        if (len(password) > 20) or (len(password) <3):
            passerror = "Please enter a Password between 3 to 20 characters."

        for char in password:
            if char == " ":
                passerror = "Password cannot contain spaces."        
        #VERIFY USERNAME
        if passerror != "" or matcherror != "":
            return render_template("signup.html", passerror = passerror, matcherror = matcherror)


        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = username
            return redirect('/login')
        else:
            flash('You are already set up as a user', 'error')
            return redirect('/login')
    
# user tries to log in with log in that doesn't exist and is redirected to /login
# user logs in with correct credentials stored in a database and is redirected to create a new blog
# #user logs in with correct username but incorrect password and is advised that password was incorrect

    return render_template('signup.html')

@app.route('/logout')
def logout():
    try:
        del session['user']
        return redirect('/')
    finally:
        return redirect('/')

if __name__ == '__main__':
    app.run()