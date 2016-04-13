from flask import Flask
from flask import request
from translate import *
from neo4jrestclient import client
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q
from py2neo_functions import *
import json

gdb = GraphDatabase("http://localhost:12345/db/data/",username="neo4j",password="manyata45")
app = Flask(__name__,static_url_path=''	)

def frame_comparator(x,y):
	return x[2]['data']['frame_start']-y[2]['data']['frame_start']

def execute_video_query(query):
	result = list(gdb.query(query))
	result.sort(frame_comparator)
	videos = {}
	for r in result:
		vid_name = r[0]['data']['name']
		if vid_name not in videos.keys():
			videos[vid_name] = {}
			videos[vid_name]['objects'] = {}
		obj_id = r[1]['data']['id']
		if obj_id not in videos[vid_name]['objects'].keys():
			videos[vid_name]['objects'][obj_id] = []
			videos[vid_name]['objects'][obj_id].append({'start':None,'end':None})
		for f in range(r[2]['data']['frame_start'],r[2]['data']['frame_end']+1):
			if videos[vid_name]['objects'][obj_id][-1]['start'] is None:
				videos[vid_name]['objects'][obj_id][-1]['start'] = f
				videos[vid_name]['objects'][obj_id][-1]['end'] = f
			else:
				if videos[vid_name]['objects'][obj_id][-1]['end']+1 == f:
					videos[vid_name]['objects'][obj_id][-1]['end'] = f
				else:
					videos[vid_name]['objects'][obj_id].append({'start':None,'end':None})
	return videos

@app.route("/")
def root():
    return app.send_static_file('ui.html')

@app.route('/nodeQuery',methods=['POST'])
def process_node_query():
	data = request.form['query']
	node_cypher = node_query(data)
	return node_cypher

@app.route('/videoQuery',methods=['POST'])
def process_video_query():
	data = request.form['query']
	video_cypher = video_query(data)
	print video_cypher
	video = execute_video_query(video_cypher)
	return json.dumps(video)

if __name__ == "__main__":
    app.run()
    # raw : SELECT o FROM object o WHERE video="VIRAT_S_010203_10_001092_001121" AND (o.id=12 or o.id=11)
    # execute_video_query("MATCH (v:Video)-[r2:has_obj]->(o:Object), (v)-[rf:has_frame]->(f:Frame)-[rf1:has_obj]->(o) WHERE v.name in ['VIRAT_S_010203_10_001092_001121'] AND (o.id=12 OR o.id=11) RETURN v, o, f, rf1 ")
   