from flask import Flask, render_template, request, send_file
import subprocess

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to run your email processing script
@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Run the email_script.py file
        subprocess.run(['python', 'email_script.py'], check=True)
        return "Script executed successfully!"
    except Exception as e:
        return f"Error running script: {str(e)}"

# Route to download the generated Excel file
@app.route('/download-excel')
def download_excel():
    path_to_file = 'zoho_email_responses.xlsx'  # Path to the output Excel file
    return send_file(path_to_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)





