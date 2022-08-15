import pandas as pd
from flask import Flask, render_template,request
from pathlib import Path
from util import models
from pathlib import Path


############ ********** #################
# this code is not necessary if your main.py is in util folder
template_base=Path(__file__).parent.joinpath('util')
# this is done because templates folder and static folder are not on same location as our running app
template_dir=template_base.joinpath('templates')
static_dir=template_base.joinpath('static')
############ ********** #################


app = Flask(__name__, template_folder=template_dir,static_folder=static_dir)

@app.route('/', methods=['GET','POST'])
def home():
    #queries fetched from dictionary keys
    queries=models.SQL_SELECT.keys()

    #initial query is blank
    squery = ''

    #on Submit
    if request.method=='POST':
        squery=request.form.get('squery')
        df=models.select_query(squery)
        #Dataframe is displayed as html table with no index
        return render_template('Base.html', queries=queries, dataframe=df.to_html(classes="table",index=False), squery=squery,boolean=True)

    #before submit
    else:
        #if there is no submit button click, no table or query will be displayed
        return render_template('Base.html', queries=queries, squery=squery,boolean=False)


if __name__=="__main__":
    app.run(debug=False,port=80)