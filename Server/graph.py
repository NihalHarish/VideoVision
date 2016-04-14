from neo4jrestclient import client
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q
from py2neo_functions import *

import collections
import os

path = "VIRAT/Virat/Public Projects/VIRAT/Public Dataset/VIRAT Video Dataset Release 2.0/VIRAT Ground Dataset/annotations"

gdb = GraphDatabase("http://localhost:12345/db/data/",username="neo4j",password="manyata45")

video_nodes = None
object_nodes = None
frame_nodes = None
event_nodes = None
location_nodes = None

#VIRAT RELATED ENUMS
object_type = {
				1: 'person',
				2: 'car',
				3: 'large vehicle',
				4: 'object',
				5: 'bike'
			 }
event_type = {
				1:'loading object to vehicle',
				2:'unloading an object from a vehicle',
				3:'opening a vehicle trunk',
				4:'closing a vehicle trunk',
				5:'getting into a vehicle',
				6:'getting out of a vehicle',
				7:'gesturing',
				8:'digging',
				9:'carrying an object',
				10:'running',
				11:'entering a facility',
				12:'exiting a facility'
			}


def initialize_labels():
	global video_nodes,object_nodes,frame_nodes,event_nodes,location_nodes
	object_nodes = gdb.labels.create("Object")
	frame_nodes = gdb.labels.create("Frame")
	event_nodes = gdb.labels.create("Event")
	location_nodes = gdb.labels.create("Location")
	video_nodes = gdb.labels.create("Video")


def migrate_video(vid_name,event_file,mapping_file,object_file):
	print "Migrating Video {}".format(vid_name)
	frames = {}	  # dictionary of frames, with the frame number as key
	objects = {} # dictionary of objects with the id as key
	events = {}  #dictionary of events with the id as key

	lines = []
	with open(object_file,'r') as f:
		lines = f.readlines()
	for idx,line in enumerate(lines):
		data = line.split(' ')
		data = [eval(i) for i in data]
		#check if object exists, if it doesn't add it to the dictionary
		if data[0] not in objects.keys():
			objects[data[0]] = {}
			objects[data[0]]['type'] = data[7]
			objects[data[0]]['duration'] = data[1]
			if(len(data)==10):
				objects[data[0]]['color'] = data[8]
				objects[data[0]]['gender'] = data[9]

		#check if frame exists, if it doesn't exist, create and intialize it
		if data[2] not in frames.keys():
			frames[data[2]] = {}
			frames[data[2]]['objects'] = []
			frames[data[2]]['events'] = []
		#add the object data to the frame as a tuple of (id,topLeft_x,topLeft_y,width,height)
		frames[data[2]]['objects'].append((data[0],data[3],data[4],data[5],data[6])) 
	print "Finished reading object file data"
	
	lines = []
	with open(event_file,'r') as f:
		lines = f.readlines()
	for idx,line in enumerate(lines):
		data = line.split(' ')
		data = [eval(i) for i in data[:-1]]
		# cehck if the event exists, if it doesn't add it to the dictionary
		if data[0] not in events.keys():
			events[data[0]] = {}
			events[data[0]]['type'] = data[1]
			events[data[0]]['duration'] = data[2]
			events[data[0]]['start_frame'] = data[3]
			events[data[0]]['end_frame'] = data[4]
			events[data[0]]['objects'] = set()
		#check if frame exists, if it doesn't create and initialize it
		if data[5] not in frames.keys():
			frames[data[5]] = {}
			frames[data[5]]['objects'] = []
			frames[data[5]]['events'] = []
		#add the event data to the frame as a tuple of (id,topLeft_x,topLeft_y,width,height)
		frames[data[5]]['events'].append((data[0],data[6],data[7],data[8],data[9]))
	print "Finished reading event file data"


	lines = []
	with open(mapping_file,'r') as f:
		lines = f.readlines()
	for idx,line in enumerate(lines):
		data = line.split(' ')
		d = []
		for i in data:
			try:
				d.append(int(i))
			except:
				pass
		data = d
		for j,i in enumerate(data[6:]):
			if i!=0:
				events[data[0]]['objects'].add(j)
	print "Finished reading mapping file"

	#Store the data read from the file into the graph
	#Create video node
	video = gdb.nodes.create(name=vid_name,path=video_path+"/"+vid_name+".mp4")
	video_nodes.add(video)

	#optimize number of frames, if two frames are identical, represent them by a single node
	opt_frames = {}
	prev_key = None
	print "Optimizing  Frames"
	for key in collections.OrderedDict(frames).keys():
		if prev_key is not None and frames[key]==frames[prev_key]:
			opt_frames[prev_key]['end']=key
		else:
			opt_frames[key]=frames[key].copy()
			opt_frames[key]['start']=key
			opt_frames[key]['end']=key
			prev_key = key
	print "Original number : {}\nOptimized number : {}".format(len(frames),len(opt_frames))


	obj_graph_ref = {} #Store references to all the created object nodes, so that they may quickly accessed without querying the graph
	event_graph_ref = {} #Store references to all the created event nodes, so that they may quickly accessed without querying the graph
	frame_graph_ref = []

	#Open a transaction
	with gdb.transaction() as tx:
		# print "Object Keys : {}".format(objects)
		#create all the object nodes
		for key in objects.keys():
			obj = gdb.nodes.create(type=objects[key]['type'],id=key,duration=objects[key]['duration'])
			#create a relationship between the video and the object
			video.relationships.create("has_obj",obj)
			obj_graph_ref[key] = obj
		print "Number of object nodes : {}".format(len(obj_graph_ref))
		# print "Dictionary : {}".format(obj_graph_ref[1])
		# print obj_graph_ref

		#create all event nodes
		for key in events.keys():
			event = gdb.nodes.create(type=events[key]['type'],id=key,duration=events[key]['duration'],start_frame=events[key]['start_frame'],end_frame=events[key]['end_frame'])
			#create a relationship between the video and the event
			video.relationships.create("has_event",event)
			event_graph_ref[key]=event
			# create relationship between event and object
			for o in events[key]['objects']:
				# print o,type(o)
				# print obj_graph_ref[o],type(obj_graph_ref[o])
				event.relationships.create("has_obj",obj_graph_ref[o])
		print "Number of event nodes : {}".format(len(event_graph_ref))

		#create all frame nodes and all the relationships
		prev_frame = None
		prev_key = None
		for i,key in enumerate(collections.OrderedDict(opt_frames).keys()):
			frame = gdb.nodes.create(frame_start = opt_frames[key]['start'],frame_end = opt_frames[key]['end'])
			frame_graph_ref.append(frame)
			#Create relationship between video and frame
			if i == 0 : 
				video.relationships.create("first_frame",frame)
			video.relationships.create("has_frame",frame)
			#Create relationship between previous frame and current frame
			if prev_frame is not None:
				prev_frame.relationships.create("next_frame",frame)
			prev_frame = frame
			#Create relationship between frame and objects
			for obj in opt_frames[key]['objects']:
				#create relationship between the frame and object
				frame.relationships.create("has_obj",obj_graph_ref[obj[0]],topLeft_x=obj[1],topLeft_y=obj[2],width=obj[3],height=obj[4])
			#Create relationship between frame and events
			for evt in opt_frames[key]['events']:
				#create relationship between the frame and event
				frame.relationships.create("has_event",event_graph_ref[evt[0]],topLeft_x=evt[1],topLeft_y=evt[2],width=evt[3],height=evt[4])
		print "Number of frame nodes : {}".format(len(frame_graph_ref))


	print "Committing changes to the graph"
	object_nodes.add(*obj_graph_ref.values())
	event_nodes.add(*event_graph_ref.values())
	frame_nodes.add(*frame_graph_ref)
	print "Migrated {} Sucessfully\n\n".format(vid_name)

def migrate_virat_dataset():
	files = []
	migrated_files = []
	for f in os.listdir(path):
		files.append(f)
	for f in files:
		vid_name = f.split(".")[0]
		if vid_name in migrated_files:
			continue
		migrate_video(vid_name,path+"/"+vid_name+".viratdata.events.txt",path+"/"+vid_name+".viratdata.mapping.txt",path+"/"+vid_name+".viratdata.objects.txt")
		migrated_files.append(vid_name)

	

if __name__ == '__main__':
	# clear_graph()
	initialize_labels()
	migrate_virat_dataset()
	# migrate_video("VIRAT_S_000002.mp4","Virat Videos/VIRAT_S_000002/VIRAT_S_000002.viratdata.objects.txt","Virat Videos/VIRAT_S_000002/VIRAT_S_000002.viratdata.events.txt","Virat Videos/VIRAT_S_000002/VIRAT_S_000002.viratdata.mapping.txt")
