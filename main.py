from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired
import pycountry
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap(app)


API = os.environ.get('API')
options = ['ae','ar','at','au','be','bg','br','ca','ch','cn','co','cu','cz','de','eg','fr','gb','gr','hk','hu','id','ie','il','in','it','jp','kr','lt','lv','ma','mx','my','ng','nl','no','nz','ph','pl','pt','ro','rs','ru','sa','se','sg','si','sk','th','tr','tw','ua','us','ve','za']
countries = []
countries_dict = {}
for i in options:
    country = pycountry.countries.get(alpha_2=i).name
    countries.append(country)
    countries_dict[country] = i

class CountryForm(FlaskForm):
    country = SelectField(label='Country',validators=[DataRequired()],choices=countries,default='Taiwan, Province of China')
    submit = SubmitField(label='Submit')

class SearchForm(FlaskForm):
    keyword = StringField(label='Keyword', validators=[DataRequired()],default='Ohtani')
    submit = SubmitField(label='Submit')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/headlines',methods=['GET','POST'])
def headlines():
    form = CountryForm()
    target = 'Taiwan, Province of China'
    if form.validate_on_submit():
        target = form.country.data
    news = requests.get(f'https://newsapi.org/v2/top-headlines?country={countries_dict[target]}&apiKey={API}').json()['articles']
    return render_template('headlines.html',form=form, news=news)

@app.route('/search',methods=['GET','POST'])
def search():
    form = SearchForm()
    keyword = 'Ohtani'
    if form.validate_on_submit():
        keyword = form.keyword.data
    news = requests.get(f'https://newsapi.org/v2/everything?q={keyword}&apiKey={API}').json()['articles']
    return render_template('search.html',form=form, news=news)

if __name__ == '__main__':
    app.run(debug=True)