from flask import request, redirect, render_template, flash, session
from functions import username_func, password_func, get_bloggers
from app import app, db
from models import Blog, User
import cgi

#@app.before_request
#def require_login():
#    
#    have_permission = ['login', 'signup', 'blog', 'index',]
#    if request.endpoint not in have_permission and 'username' not in session:
#        return redirect('/login')
#THE ABOVE KEEPS GIVING ME error 302
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users = users)

@app.route('/blog')
def blog():
    blog_id = request.args.get('id')
    user_id = request.args.get('user_id')

    if blog_id == None:
        posts = Blog.query.all()
        return render_template('blog.html', posts=posts, title='Build-a-blog')
    else:
        post = Blog.query.get(blog_id)
        return render_template('entry.html', post=post, title='My Blog Entry')



@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-entry']
        title_error = ''
        body_error = ''

        if len(blog_title) < 1:
            title_error = "Please enter a blog title"
        if  len(blog_body) < 1:
            body_error = "Please create a blog entry"

        if body_error == '' and title_error == '':
            new_entry = Blog(blog_title, blog_body)     
            db.session.add(new_entry)
            db.session.commit()        
            return redirect('/blog?id={}'.format(new_entry.id)) 
        else:
            return render_template('newpost.html', title='New Entry', title_error=title_error, body_error=body_error, 
                blog_title=blog_title, blog_body=blog_body)
    
    return render_template('newpost.html', title='New Entry')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        login_error = "please enter a valid username and password combination"
        
        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')

        return render_template("login.html", login_error=login_error)
    else:
        return render_template('login.html')
        
        

@app.route('/signup',  methods=['POST','GET'])
def singup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form['username']
        username = cgi.escape(username)
        password = request.form['password']

        user_id = request.args.get('id')
        print(user_id)
# 2/18/2019 MAJOR PROBLEM HERE user_id should not be 'None' as 'alec' and 'alec' are in database
        if user_id == None:
            new_entry = User(username, password)     
            db.session.add(new_entry)
            db.session.commit()        
            return render_template('blog.html', my_login = username)
        else:
            return render_template('signup.html', name_error = "username already exists")

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

if __name__ == "__main__":
    app.run()
