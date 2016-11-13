from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__, template_folder='.')

@app.route('/')
@app.route('/index')
def index(chartID = 'chart_ID', chart_type = 'column', chart_height = 450):
	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
	title = {"text": 'My Title'}
	xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
	yAxis = {"title": {"text": 'yAxis Label'}}
	return render_template('index.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
	chartID = 'chart_ID'
	chart_type = 'line' # default option
	chart_height = 500
	selected_option = None
	try:
		selected_option = str(request.form['charttype'])
		if selected_option:
			chart_type = selected_option
	except:
		print "Chart Type not selected !!!"
	# return selected_option
	if request.method == 'POST':
		file = request.files['file']
		data = file.read()
		d = json.loads(data)
		print str(d['data'][0][0])

		if len(d) < 2:
			return jsonify({"error" : "No Data Found !!!"})

		i = 0
		fields = None
		data = None
		
		# Getting objects contained in the json, ie fields and data (though it can have other name)
		for obj in d:
			if i == 0:
				fields = obj
				i = 1
			else:
				data = obj
				break

		fields = d[fields]
		data = d[data]
		print fields
		print data

		all_series = []
		values = []
		categories = []

		for i in range(len(data)):
			categories.append(str(data[i][0]))

		for i in range(1, len(fields)):
			s = {}
			s["name"] = str(fields[i]["label"])
			value = []
			for j in range(len(data)):
				value.append(float(data[j][i]))
			s["data"] = value
			all_series.append(s)

		# for i in range(len(d['data'])):
		# 	s = {}
		# 	for j in range(1, len(d['fields'])):
		# 		s["name"] = str(d['fields'])
		# 	values.append(float(d['data'][i][8]))
		# 	categories.append(str(d['data'][i][0]))
		# print values, categories
		# return "ok"

		label = "Chart"
		# print label
		# print all_series

		chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "zoomType": "x"}
		#series = [{"name": label, "data": values}, {"name": label, "data": values}]
		series = all_series
		title = {"text": label}
		xAxis = {"categories": categories, "min": 0, "max": 6}
		yAxis = {"title": {"text": 'Values'}}
		return render_template('index.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)
	return jsonify("No Data !!!")

if __name__ == "__main__":
	app.run(debug=True, port=5000, passthrough_errors=True)