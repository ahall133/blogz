from flask import Flask, request, redirect, render_template, session
from functions import username_func, password_func, ver_pass_func, get_bloggers, get_blogs, new_blog_title, new_blog_body
from app import app, db
from models import Blog, User
import cgi



@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users = users)

@app.route('/allposts')
def all_posts():
    posts = Blog.query.all()
    return render_template('blog.html', posts = posts)

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')
    user_id = request.args.get('userid')
    posts = Blog.query.all()
    print("*************************************")
    print(blog_id)
    print(user_id)
    print("*************************************")

    if blog_id:
        post = Blog.query.filter_by(id=blog_id).first()
        return render_template("post.html", title=post.title, body=post.body, user=post.owner.username, user_id=post.owner_id)
    if user_id:
        entries = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('user.html', entries=entries)

    return render_template('blog.html', posts = posts )

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'GET':
        if 'user' not in session:
            login_error = "please enter a valid username and password combination"
            return render_template('login.html', login_error = login_error)
        return render_template('newpost.html', username = session['user'])
        
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
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        login_error = "please enter a valid username and password combination"
        
        if user and user.password == password:
            session['user'] = username

            return redirect('/newpost')

        return render_template("login.html", login_error=login_error)
    else:
        return render_template('login.html')

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
                session['user'] = username               
                return redirect('/newpost')
            
        elif user:
            return render_template('signup.html', name_error = existing_error )
            
        return render_template('signup.html', name_error = name_error, pass_error = pass_error, ver_pass_error = ver_pass_error)

    return render_template('signup.html')

@app.route('/logout')
def logout():
    if 'user' in session:
        del session['user']
    return redirect('/')

if __name__ == "__main__":
    app.run()
