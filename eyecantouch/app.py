from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # templates 폴더에서 불러옴

@app.route("/phone-input")
def phone_input():
    return render_template("phone_input.html")

if __name__ == '__main__':
    app.run(port=1999, debug=True)