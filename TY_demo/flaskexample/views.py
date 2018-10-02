from flask import render_template
from flask import request
from flaskexample import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2


from utilTy import find_best_data
from a_Model import ModelIt

user = 'tyyano' #add your username here (same as previous postgreSQL)

host = 'localhost'
dbname = 'demo2_db'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database = dbname, user = user)


@app.route('/')
@app.route('/index')
def index():
   user = { 'nickname': 'Twtytee' } # fake user
   return render_template("index.html", title = 'Home', user = user) 


@app.route('/mock')
def mock():
   return render_template("mock.html") 

@app.route('/inputfuncy')
def funcy_input():
    return render_template("inputfuncy.html")

@app.route('/outputfuncy')
def funcy_output():
	#pull 'issue' from input field and store it
	issue_val = request.args.get('issue')
	#select ---- from the ----  dtabase for --- the user inputs
	if issue_val == "Any Issues":
		query = "SELECT index, created_at, handle,twt_url, text_std, log_odds, lc FROM demo_data_table WHERE likely='LIKELY'"
	else:
		query = "SELECT index, created_at, handle,twt_url, text_std, log_odds, lc FROM demo_data_table WHERE likely='LIKELY' AND issue='%s'" % issue_val 
	print(query)
	query_results=pd.read_sql_query(query,con)
	#print(query_results)
	liberal = []
	conserv = []
	births = []
	births_refined = []

	# order by the date 
	for i in range(0,query_results.shape[0]):
		dateStrOrg = query_results.iloc[i]['created_at']
		dateStr = query_results.iloc[i]['created_at'].split()[0]
		dateStr = ''.join(dateStr.split('-'))
		dateInt = int(dateStr)
		handleStr = query_results.iloc[i]['handle']
		twt_url_str = query_results.iloc[i]['twt_url']
		lc_str = query_results.iloc[i]['lc']
		idx_str = query_results.iloc[i]['index']
		log_odds_str = query_results.iloc[i]['log_odds']
		log_odds_float = float(query_results.iloc[i]['log_odds'])
		txt_str =query_results.iloc[i]['text_std']

		color = "blue"
		if lc_str == 'Conservative':
			color = "red"

		if (lc_str =='Liberal'):
			liberal.append((idx_str, log_odds_float, dateInt))
		else:
			conserv.append((idx_str, log_odds_float, dateInt))
		births.append(dict(index=idx_str, created_at=dateStrOrg, handle=handleStr, twt_url=twt_url_str, \
			text_std=txt_str, log_odds=log_odds_str, lc=lc_str, color=color))

	#sort the tuple by date and log odds value 
	liberal_idx = find_best_data(liberal, 7)
	conserv_idx = find_best_data(conserv, 7)

	# return only equal number of liberal and conservative;
	# odds number is liberal, even number is conservative
	limit = min(len(liberal_idx), len(conserv_idx))
	liberal_idx = liberal_idx[:limit]
	conserv_idx = conserv_idx[:limit]

	birth_liberal = []
	birth_conserv = []
	for x in births:
		if x['index'] in liberal_idx:
			birth_liberal.append(x)
		elif x['index'] in conserv_idx: 
			birth_conserv.append(x)

	for i in range(limit):
		births_refined.append((birth_liberal[i], birth_conserv[i]))

	the_result = ModelIt(issue_val,births)

	return render_template("outputfuncy.html", births = births_refined, the_result = the_result, inputVal = issue_val)
