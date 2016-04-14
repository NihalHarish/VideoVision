from neo4jrestclient import client
from neo4jrestclient.client import GraphDatabase

gdb = GraphDatabase("http://localhost:12345/db/data/",username="neo4j",password="manyata45")


def execute_video_query(query):

	def frame_comparator(x,y):
		return x[2]['data']['frame_start']-y[2]['data']['frame_start']

	videos = {}
	try:
		result = list(gdb.query(query))
	except:
		print "DB ERROR"
	if result is None:
		return videos
	result.sort(frame_comparator)

	# print r[0]['data']['name'],r[1]['data']['id'],r[2]['data']['frame_start'],r[2]['data']['frame_end']

	# for r in result:
	# 	print r[1]['data']['id'],r[2]['data']['frame_start'],r[2]['data']['frame_end']

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
	results = []
	for video in videos.keys():
		for node in videos[video]['objects'].keys():
			for clip in videos[video]['objects'][node]:
				d={}
				d['video'] = video
				d['node'] = node
				d['start'] = clip['start']
				d['end'] = clip['end']
				results.append(d)
	return results

	
