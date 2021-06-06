from flask import Flask
import asyncio
app = Flask(__name__)

@app.route('/')
async def hello_world():
    return '<img src="https://i.kym-cdn.com/photos/images/newsfeed/000/176/526/yo-dawg-yo-yos.jpg">'