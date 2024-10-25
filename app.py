from flask import Flask, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')  # Serve index.html directly from static folder

@app.route('/submit', methods=['POST'])
def submit():
    roast_intensity = request.form.get('roast_intensity')
    print(f"Received roast intensity: {roast_intensity}")  # Debugging line

    # Store the roast intensity in a file
    with open('roast_intensity.txt', 'w') as f:
        f.write(roast_intensity)
        print(f"Wrote roast intensity to file: {roast_intensity}")  # Debugging line

    return redirect(url_for('index'))  # Redirect back to the home page

if __name__ == '__main__':
    app.run(debug=True)
