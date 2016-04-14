from flask import Flask
from flask import request
import translate
import DBCommonFunctions as db
import json

'''				RAW QUERIES
1. SELECT o FROM object o WHERE video="VIRAT_S_010203_10_001092_001121" AND (o.id=12 or o.id=11)
2. 
'''



app = Flask(__name__,static_url_path='')


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

@app.route("/")
def root():
    return app.send_static_file('ui.html')

@app.route('/nodeQuery',methods=['POST'])
def process_node_query():
	data = request.form['query']
	node_cypher = translate.node_query2(data)
	return node_cypher

@app.route('/videoQuery',methods=['POST'])
def process_video_query():
	data = request.form['query']
	video_cypher = translate.video_query(data)
	video = db.execute_video_query(video_cypher)
	return json.dumps(video)

if __name__ == "__main__":
    app.run(host= '0.0.0.0')
    # execute_video_query("MATCH (v:Video)-[r2:has_obj]->(o:Object), (v)-[rf:has_frame]->(f:Frame)-[rf1:has_obj]->(o) WHERE v.name in ['VIRAT_S_010203_10_001092_001121'] AND (o.id=12 OR o.id=11) RETURN v, o, f, rf1 ")
   