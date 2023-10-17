from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'secret_key'  # Секретный ключ для сессий

# Главная страница
@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
    else:
        username = None
    return render_template('index.html', username=username)

# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Сохранение данных регистрации в txt файл
        with open('registration.txt', 'a') as file:
            file.write(f'{username}:{password}\n')
        return redirect(url_for('login'))
    return render_template('register.html')

# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Проверка, есть ли такой пользователь в личном кабинете
        with open('registration.txt', 'r') as file:
            for line in file:
                if line.strip() == f'{username}:{password}':
                    session['username'] = username
                    return redirect(url_for('index'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        # Сохранение данных поста в txt файл
        with open('posts.txt', 'a') as file:
            file.write(f'{title}:{content}\n')
        return redirect(url_for('index'))
    return render_template('add_post.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            status = request.form['status']
            # Сохранение статуса о семейном положении в txt файл
            with open('status.txt', 'a') as file:
                file.write(f'{username}:{status}\n')
        # Чтение постов из txt файла
        posts = []
        with open('posts.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split(':')
                posts.append({'title': title, 'content': content})
        # Чтение статуса о семейном положении из txt файла, если есть
        status = None
        with open('status.txt', 'r') as file:
            for line in file:
                user, stat = line.strip().split(':')
                if user == username:
                    status = stat
                    break
        return render_template('profile.html', username=username, posts=posts, status=status)
    else:
        return redirect(url_for('login'))


# Страница выхода
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
