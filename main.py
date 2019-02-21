from flask import Flask, request, redirect, render_template, session
from functions import username_func, password_func, ver_pass_func, get_bloggers, get_blogs, new_blog_title, new_blog_body
from app import app, db
from models import Blog, User
import cgi

@app.route('/')
def index():
    users = get_bloggers()
    return redirect('/blog')
# todo: fix this
@app.route('/blog')
def blog():
    blog_id = request.args.get('id')
    user_id = request.args.get('user_id')
    exist_blogs = get_blogs()

    if blog_id == None:
        posts = Blog.query.all()
        return render_template('blog.html', posts=posts, title='Build-a-blog')
    else:
        post = Blog.query.get(blog_id)
        return render_template('entry.html', post=post, title='My Blog Entry')
# possibly working
@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'GET':
        if 'user' not in session:
            login_error = "please enter a valid username and password combination"
            return render_template('login.html', login_error = login_error)
        

    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-entry']
        title_error = new_blog_title(blog_title)
        body_error = new_blog_body(blog_body)
        
        owner_id = User.query.filter_by(username=session['user']).first()

        if body_error == '' and title_error == '':
            new_entry = Blog(blog_title, blog_body, owner_id)     
            db.session.add(new_entry)
            db.session.commit()        
            return redirect('/blog?id={}'.format(new_entry.id)) 
        else:
            return render_template('newpost.html', title_error=title_error, body_error=body_error, blog_title=blog_title, blog_body=blog_body)
    
    
# possibly working
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        login_error = "please enter a valid username and password combination"
        
        if user and user.password == password:
            session['user'] = username
            print(username)
# issue with redirect: 'no return statment' error. probably line 64. see same error on line 89
            return render_template('newpost.html')

        return render_template("login.html", login_error=login_error)
    else:
        return render_template('login.html')
# possibly working
@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_pw = request.form['verpass']
        user = User.query.filter_by(username=username).first()

        name_error = username_func(username)
        pass_error = password_func(password)
        ver_pass_error = ver_pass_func(password,verify_pw)
        existing_error = "username is already taken"

        if not user:
            if name_error == '' and pass_error == '' and ver_pass_error == '':
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
# problem right here with redirect: 'no return statement' error. probably issue with line 89. redirect issue?               
                return redirect('/newpost')
            return render_template('signup.html', name_error = name_error, pass_error = pass_error, ver_pass_error = ver_pass_error)
        
        elif user:
            return render_template('signup.html', name_error = existing_error )
    return render_template('signup.html')
# probably working but not implemented in html
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

if __name__ == "__main__":
    app.run()
