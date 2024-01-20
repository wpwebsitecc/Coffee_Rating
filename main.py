from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TimeField, URLField
from wtforms.validators import DataRequired
import csv
from datetime import time


'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    map = URLField(label="Location URL", validators=[DataRequired()])
    open_time = TimeField(label="Opening Time", validators=[DataRequired()], default=time(7, 0))
    close_time = TimeField(label="Closing Time", validators=[DataRequired()], default=time(23, 0))
    coffee = SelectField(label="Coffee Rating",
                         choices=[("☕️☕️☕️☕️☕️", "☕️☕️☕️☕️☕️"), ("☕️☕️☕️☕️", "☕️☕️☕️☕️"), ("☕️☕️☕️️", "☕️☕️☕️️"),
                                  ("☕️☕️", "☕️☕️"), ("☕️", "☕️"), ("✘", "✘")],
                         validators=[DataRequired()])
    wifi = SelectField(label="Wifi Signal",
                       choices=[("💪💪💪💪💪️", "💪💪💪💪💪️"), ("💪💪💪💪️", "💪💪💪💪️"), ("💪💪💪️", "💪💪💪️"), ("💪💪", "💪💪"), ("💪", "💪"),
                                ("✘", "✘")],
                       validators=[DataRequired()])
    power = SelectField(label="Power Outlet Accessibility",
                        choices=[("🔌🔌🔌🔌🔌️", "🔌🔌🔌🔌🔌️"), ("🔌🔌🔌🔌", "🔌🔌🔌🔌"), ("🔌🔌🔌", "🔌🔌🔌"), ("🔌🔌", "🔌🔌"), ("🔌", "🔌"),
                                 ("✘", "✘")],
                        validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])  # Allow both GET and POST requests
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        # Extract data from form
        cafe_data = [
            form.cafe.data,
            form.map.data,
            form.open_time.data.strftime("%I:%M %p"),  # Format time as string
            form.close_time.data.strftime("%I:%M %p"),  # Format time as string
            form.coffee.data,
            form.wifi.data,
            form.power.data
        ]

        # Write data to CSV
        with open('cafe-data.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(cafe_data)

        # Redirect or handle the successful form submission here
        return redirect(url_for('home'))  # Replace with your desired route

    # Render the form page
    return render_template('add.html', form=form)



@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        next(csv_data, None)
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
