from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(name)

app.config['SECRET'] = "secret!123"

socketio = SocketI0(app, cors_allowed_origins="*")

@socketio.on('message')

def handle_message (message):

 print("Received message: " + message) if message != "User connected!":

send(message, broadcast=True)

if __name__=="__main__":

 socketio.run(app, host="localhost")
