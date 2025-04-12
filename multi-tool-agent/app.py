from flask import Flask, render_template, request
from forms import CityForm
from agent import handle_query

app = Flask(__name__)
app.secret_key = "secret"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    form = CityForm()
    response = None
    if form.validate_on_submit():
        city = form.city.data
        query = f"What is the weather in {city}?"
        response = handle_query(query)
    return render_template("form_page.html", form=form, title="Weather", response=response)

@app.route('/time', methods=['GET', 'POST'])
def time():
    form = CityForm()
    response = None
    if form.validate_on_submit():
        city = form.city.data
        query = f"What is the time in {city}?"
        response = handle_query(query)
    return render_template("form_page.html", form=form, title="Time", response=response)

if __name__ == '__main__':
    app.run(debug=True)
