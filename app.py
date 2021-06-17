from flask import Flask, render_template, jsonify
import pandas as pd
import datetime

app = Flask(__name__)

@app.route('/')
def index():
	data = pd.read_csv('SacramentocrimeJanuary2006.csv')
	# list_index = []
	daily_case = {}
	case_by_district = {}
	for index, row in data.iterrows():
		tanggal = datetime.datetime.strptime(row['cdatetime'],'%m/%d/%y %H:%M')
		
		case = {
			'cdatetime':tanggal,
			'address':row['address'],
			'district':row['district'],
			"beat":row['beat'],
			"grid":row['grid'],
			"crimedescr":row['crimedescr'],
			'ucr_ncic_code':row['ucr_ncic_code'],
			"latitude": row['latitude'],
			"longitude": row['longitude']
		}

		# if tanggal.day in list_index:
		# 	pass
		# else:
		# 	list_index.append(tanggal.day)

		# Append data for daily_case
		if tanggal.day in daily_case:
			daily_case[tanggal.day]['total'] +=1
			daily_case[tanggal.day]['case'].append(case)
		else:
			daily_case[tanggal.day] = {
				"total": 1,
				"case":[case]
			}

		# APpend Data for case by district
		if row['district'] in case_by_district:
			case_by_district[row['district']]['total'] +=1
			case_by_district[row['district']]['case'].append(case)
		else:
			case_by_district[row['district']] = {
				'total': 1,
				"case": [case]
			}

	data = {
		"total_data":len(data),
		"daily_case":daily_case,
		"case_by_district":dict(sorted(case_by_district.items()))
	}

	return jsonify(case_by_district)
	return render_template('index.html',data=data)

if __name__ == '__main__':
	app.run(debug=True)