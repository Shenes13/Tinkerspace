from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/roast/<level>')
def roast(level):
    # You can handle the roast level selection here if needed
    return render_template('index2.html', level=level)

if __name__ == '__main__':
    app.run(debug=True)
