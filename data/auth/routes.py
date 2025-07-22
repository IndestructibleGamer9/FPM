from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth_bp
from .forms import LoginForm, RegisterForm, VerifyForm
import random


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    from models import User
    from extensions import db
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Logged in successfully.', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid Password', 'danger')
                return render_template('auth/login.html', form=form)
        else:
            flash('Invalid email.', 'danger')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    from models import User
    from extensions import db  
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('An account with this email already exists.', 'danger')
            return redirect(url_for('auth.signup'))
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.', 'warning')
            return redirect(url_for('auth.signup'))

        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=16)
        new_user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()
        
        # Login user and redirect to verification
        login_user(new_user)
        flash('Account created successfully! Please verify your email.', 'success')
        return redirect(url_for('index'))

    return render_template('auth/signup.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    from models import User
    from extensions import db
    user_id = current_user.id
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('auth.login'))
