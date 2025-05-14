
from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

def save_to_google_sheet(data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key("https://docs.google.com/spreadsheets/d/1keNQIP_PDf9qhearfVRrbru0bQ-dnxrFJ-ElF5duA4A/edit?usp=sharing").sheet1

    row = [
        data['first_name'],
        data['last_name'],
        data['email'],
        data['phone'],
        data['address'],
        data['name_of_deceased'],
        data['place_of_death'],
        data['st_peter_plan'],
        data['memorial_option'],
        data['memorial_other'],
        ', '.join(data['add_ons'])
    ]

    sheet.append_row(row)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        required_fields = [
            'first_name', 'last_name', 'email', 'phone', 'address',
            'name_of_deceased', 'place_of_death',
            'st_peter_plan', 'memorial_option', 'memorial_other'
        ]

        for field in required_fields:
            if not request.form.get(field):
                return f"<h3>Error: '{field}' is required.</h3><a href='/'>Back to form</a>"

        add_ons = request.form.getlist('add_ons')
        if not add_ons:
            return "<h3>Error: Please select at least one add-on.</h3><a href='/'>Back to form</a>"

        data = {
            field: request.form[field] for field in required_fields
        }
        data['add_ons'] = add_ons

        save_to_google_sheet(data)
        return "<h2>Thank you! Your data has been saved to Google Sheets.</h2>"

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
