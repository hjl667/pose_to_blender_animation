from flask import Flask, jsonify, request, session, redirect, send_from_directory
from passlib.hash import pbkdf2_sha256
from app import db
import uuid
import os
import subprocess


class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
        print(request.form)

        # Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # Check for existing email address
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400

        if db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "Signup failed"}), 400

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):

        user = db.users.find_one({
            "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)

        return jsonify({"error": "Invalid login credentials"}), 401
    def upload_file(self):

        UPLOAD_PATH = '/Users/hongjiji/Documents/Code'
        BLENDER_PATH = '/path/to/blender'
        BLENDER_SCRIPT_PATH = '/Users/hongjiji/Documents/Code/blender_script.py'

        uploaded_file = request.files['file']

        if uploaded_file.filename != '':
            # Save the uploaded file to a fixed location
            uploaded_file.save(os.path.join(UPLOAD_PATH, '01_01.bvh'))

            # Run the Blender script to process the file and generate animation
            cmd = [BLENDER_PATH, '-b', '-P', BLENDER_SCRIPT_PATH]
            subprocess.run(cmd)

        return 'Upload and Conversion Successful', 200

    def download_file(self):
        OUTPUT_PATH = '/Users/hongjiji/Documents'
        OUTPUT_FILENAME = 'Code0001-0020.mp4'

        return send_from_directory(OUTPUT_PATH, OUTPUT_FILENAME, as_attachment=True)