from flask import Flask, render_template, session, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from produce_report import ProduceReport
import configuration

app = Flask(__name__)

app.config['SECRET_KEY'] = 'abc'

class ReportSelect(FlaskForm):

    report_date = DateField('DatePicker', format = '%Y-%m-%d')
    submit = SubmitField('Produce Report')


@app.route('/', methods = ['GET','POST'])
def index():
    report_date = False
    report_results = {}
    report_run = False
    form = ReportSelect()
    if form.validate_on_submit():
        report_date = form.report_date.data
        session['report_date'] = form.report_date.data
        try:
            report = ProduceReport(configuration.report, 
                                   form.report_date.data, 
                                   configuration.client, 
                                   configuration.file_source, 
                                   file_path = configuration.file_path,
                                   )
            report_results = report.produce_report()
            report_run = True
        except Exception as e:
            flash(e)
            report_date = False         
        
    return render_template('home_page.html', form=form, report_date=report_date, report_results=report_results, report_run=report_run)

@app.route('/requirements_page')
def report():
    return render_template('requirements_page.html')


if __name__ == '__main__':
    app.run()