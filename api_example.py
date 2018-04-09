from flask import Flask,render_template,jsonify
import requests
from google_credential_key import key

app = Flask(__name__)

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"

@app.route("/",methods=["GET"])
def retreive():
	return render_template('layout.html')

@app.route("/sendRequest/<string:query>")
def results(query):
	search_payload = {"key":key, "query":query}
	search_req = requests.get(search_url,params=search_payload)
	#take json object from response
	search_json = search_req.json()

	place_id = search_json["results"][1]["place_id"]

	#now send request to "details_url" using placez-id
	details_payload = {"key":key, "placeid":place_id}
	details_resp = requests.get(details_url,params=details_payload)
	#get json object 
	details_json = details_resp.json()


	url = details_json["result"]["url"]
	return jsonify({'result' : url})



if __name__ == '__main__':
	app.run(debug=True)


