from flask import request, redirect, render_template
from functions import username_func, password_func
from app import app, db
from models import Blog, User
import cgi

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog')
def blog():
    blog_id = request.args.get('id')

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

@app.route('/login', methods=['POST','GET'])
def errors():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        username = cgi.escape(username)
        password = request.form['password']

        name_error = username_func(username)
        pass_error = password_func(password)

        user_id = request.args.get('id')
        
        ready_to_go = None

        if name_error != '' and pass_error != '':
            return render_template('login.html', name_error=name_error, pass_error=pass_error)

        if user_id == None:
            # add href to create user account
            return render_template('broken.html')
        

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
            


#@app.route('/index')

#@app.route('/logout')

if __name__ == "__main__":
    app.run()
