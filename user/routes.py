from flask import Flask
from app import app
from user.models import User

@app.route('/user/signup', methods=['POST'])
def signup():
  return User().signup()

@app.route('/user/signout')
def signout():
  return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
  return User().login()

@app.route('/upload', methods=['POST'])
def upload_file():
  return User().upload_file()

@app.route('/download')
def download_file():
  return User().download_file()
