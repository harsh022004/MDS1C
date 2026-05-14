# -*- coding: utf-8 -*-
import os
import json
import urllib.request
from flask import Flask, render_template, request

# Initialize Flask app, pointing template_folder to current directory
app = Flask(__name__, template_folder='.')

@app.route('/', methods=['GET', 'POST'])
def main_handler():
    error_message = None
    if request.method == 'POST':
        pincode = request.form.get('zipCode', '').strip()

        # Validation: Must be 6 digits
        if not pincode or not pincode.isnumeric() or len(pincode) != 6:
            error_message = "Please enter a valid 6-digit PIN code."
            return render_template('index.html', error=error_message)

        # External API Call
        url = f"https://api.postalpincode.in/pincode/{pincode}"
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            # Check if API returned valid data
            if (data and isinstance(data, list) and 
                data[0].get('Status') == 'Success' and 
                data[0].get('PostOffice')):
                
                po = data[0]['PostOffice'][0]
                return render_template('results.html',
                    post_office=po.get('State', 'N/A'),
                    name=po.get('Name', 'N/A'),
                    block=po.get('Block', 'N/A'),
                    district=po.get('District', 'N/A')
                )
            else:
                error_message = "Invalid PIN code. No post office found."
        except Exception:
            error_message = "Error connecting to API. Please try again later."

    return render_template('index.html', error=error_message)

if __name__ == '__main__':
    # Use the port assigned by the environment variable, defaulting to 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='127.0.0.1', port=port, debug=True)
