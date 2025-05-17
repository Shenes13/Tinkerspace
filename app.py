from flask import Flask, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
# Define the maximum number of entries to keep
MAX_ENTRIES = 20

@app.route('/')
def index():
    return app.send_static_file('index.html')  # Serve index.html directly from static folder

@app.route('/submit', methods=['POST'])
def submit():
    roast_intensity = request.form.get('roast_intensity')

    print(f"Received roast intensity: {roast_intensity}")  # Debugging line

    # Store the roast intensity in a file (append mode)
    with open('roast_intensity.txt', 'a+') as f:
        # Move to the beginning of the file for reading
        f.seek(0)

        # Read all existing lines
        lines = f.readlines()

        # If the file is empty, write headers
        if not lines:
            f.write("+---------------------+-------------+-------------+-------------+\n")  # Top border
            f.write("|      Timestamp      |  Mild Roast | Medium Roast|  High Roast |\n")  # Headers
            f.write("+---------------------+-------------+-------------+-------------+\n")  # Divider

        # Create a new entry
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mild_value = roast_intensity if roast_intensity == "Mild" else ""
        medium_value = roast_intensity if roast_intensity == "Medium" else ""
        high_value = roast_intensity if roast_intensity == "High" else ""

        new_entry = f"| {timestamp} | {mild_value:<11} | {medium_value:<11} | {high_value:<11} |\n"
        
        # Append the new entry
        f.write(new_entry)
        f.write("+---------------------+-------------+-------------+-------------+\n")  # Divider after new entry
        
        print(f"Wrote roast intensity to file: {roast_intensity}")  # Debugging line

        # Remove old entries if the number of entries exceeds MAX_ENTRIES
        if len(lines) >= (MAX_ENTRIES * 2 + 4):  # Check if the current count exceeds the limit
            # Keep only the last MAX_ENTRIES entries (2 lines per entry)
            lines = lines[:2] + lines[-(MAX_ENTRIES * 2):]  # Keep headers and the last MAX_ENTRIES entries

            # Write back to the file, keeping the latest entries
            f.seek(0)  # Go back to the start of the file
            f.truncate()  # Clear the file
            f.writelines(lines)  # Write the kept lines back to the file

    return redirect(url_for('index'))  # Redirect back to the home page

if __name__ == '__main__':
    app.run(debug=True)
