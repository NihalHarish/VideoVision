from py2neo import authenticate,Graph,Node,Relationship,watch
import re

#set up authentication parameters
authenticate("localhost:12345", "neo4j", "manyata45")
graph = Graph("http://localhost:12345/db/data")
cypher = graph.cypher


########################################## PY2NEO FUNCTIONS #############################################
#CLEAR GRAPH FUNCTIONS
def clear_graph():
	graph.cypher.execute("MATCH (n) DETACH DELETE n")

#CREATE FUNCTIONS
def create_node(label,attrib):
	if attrib is not None:
		query = "CREATE (n:{}{{".format(label)
		for key in attrib.keys():
			if type(attrib[key]) is str:
				query+=" {} : '{}',".format(key,attrib[key])
			else:
				query+=" {}:{},".format(key,attrib[key])
		query=query[:-1]
		query+=" }) RETURN n"
	else:
		query = "CREATE (n:{}) RETURN n".format(label)
	# print "Query : {}\n".format(query)
	rec = graph.cypher.execute(query)

def create_relationship(label1,node1_attrib,label2,node2_attrib,relation_name,relation_attrib):
	if node1_attrib is not None:
		query = "MATCH (n1:{}{{".format(label1)
		for key in node1_attrib.keys():
			if type(node1_attrib[key]) is str:
				query+=" {}:'{}',".format(key,node1_attrib[key])
			else:
				query+=" {}:{},".format(key,node1_attrib[key])
		query=query[:-1]
		query+="}), "
	else:
		query = "MATCH (n1:{}), ".format(label1)

	if node2_attrib is not None:
		query+="(n2:{}{{".format(label2)
		for key in node2_attrib.keys():
			if type(node2_attrib[key]) is str:
				query+=" {}:'{}',".format(key,node2_attrib[key])
			else:
				query+=" {}:{},".format(key,node2_attrib[key])
		query=query[:-1]
		query+="}) "
	else:
		query+="(n2:{}) ".format(label2)
	if relation_attrib is not None:
		query+="CREATE (n1)-[:{}{{".format(relation_name)
		for key in relation_attrib.keys():
			if type(relation_attrib[key]) is str:
				query+=" {}:'{}',".format(key,relation_attrib[key])
			else:
				query+=" {}:{},".format(key,relation_attrib[key])
		query=query[:-1]
		query+="}]->(n2)"
	else:
		query+="CREATE (n1)-[:{}".format(relation_name)
		query+="]->(n2)"
	# print "Query : {}\n".format(query) 
	recList = graph.cypher.execute(query)


#MATCH FUNCTIONS
def get_node(label,attrib):
	''' Will return the first node returned by the graph'''
	rec = _match_node(label,attrib)
	for r in rec:
		return _process_node_record(r)

def get_nodes(label,attrib):
	''' Will return all the nodes returned by the graph'''
	rec = _match_node(label,attrib)
	results = []
	for r in rec:
		results.append(_process_node_record(r))
	return results

def check_node(label,attrib):
	''' Checks if the graph returns atleast one node that matches the query'''
	rec = _match_node(label,attrib)
	for r in rec:
		if _process_node_record(r):
			return True
	return False

def _match_node(label,attrib):
	query = "MATCH (n:{}".format(label)
	if attrib is not None:
		query+="{"
		for key in attrib:
			if type(attrib[key]) is str:
				query+=" {}:'{}',".format(key,attrib[key])
			else:
				query+=" {}:{},".format(key,attrib[key])
		query=query[:-1]
		query+="}) RETURN n"
	else:
		query+=") RETURN n"
	# print "Query : {}\n".format(query)
	return cypher.execute(query)

def _process_node_record(record):
	result = {}
	record = str(record[0])
	try:
		regex = r'^\(([A-z0-9]+):([A-z0-9]+)\s?(?:\{(.*?)\})?\)$'
		match = re.match(regex,record)
		if match is None:
			return None
		result['_id']=match.group(1)
		result['_label']=match.group(2)
		if match.group(3) is None:
			return result
		pairs = match.group(3).split(",")
		for pair in pairs:
			p = pair.split(':')
			result[p[0]] = eval(p[1])
		return result
	except:
		raise Exception("Invalid Node Record")
	

def get_relationship(label1,node1_attrib,label2,node2_attrib,relation_name,relation_attrib):
	'''Returns the first relationship returned by the graph'''
	rec = _match_relationship(label1,node1_attrib,label2,node2_attrib,relation_name,relation_attrib)
	for r in rec:
		return _process_relationship_record(r)

def get_relationships(label1,node1_attrib,label2,node2_attrib,relation_name,relation_attrib):
	'''Returns all the relationships returned by the graph'''
	result = []
	rec = _match_relationship(label1,node1_attrib,label2,node2_attrib,relation_name,relation_attrib)
	for r in rec:
		result.append(_process_relationship_record(r))

def check_relationship(label1,node1_attrib,label2,node2_attrib,relation_name,relation_attrib):
	''' Checks if the graph returns atleast one relationship that matches the query'''
	rec = _match_relationship(label1,node1_attrib,label2,node2_attrib,relation_name,relation_attrib)
	for r in rec:
		if _process_relationship_record(r):
			return True
	return False

def _match_relationship(label1,node1_attrib,label2,node2_attrib,relation_name,relation_attrib):
	query = "MATCH (n1:{}".format(label1)
	if node1_attrib is not None:
		query+="{"
		for key in node1_attrib.keys():
			if type(node1_attrib[key]) is str:
				query+=" {}:'{}',".format(key,node1_attrib[key])
			else:
				query+=" {}:{},".format(key,node1_attrib[key])
		query=query[:-1]
		query+="}"
	query+=") -[r:{}".format(relation_name)
	if relation_attrib is not None:
		query+="{"
		for key in relation_attrib.keys():
			if type(relation_attrib[key]) is str:
				query+=" {}:'{}',".format(key,relation_attrib[key])
			else:
				query+=" {}:{},".format(key,relation_attrib[key])
		query=query[:-1]
		query+="}"
	query+="]-> (n2:{}".format(label2)		
	if node2_attrib is not None:
		query+="{"
		for key in node2_attrib.keys():
			if type(node2_attrib[key]) is str:
				query+=" {}:'{}',".format(key,node2_attrib[key])
			else:
				query+=" {}:{},".format(key,node2_attrib[key])
		query=query[:-1]
		query+="}"
	query+=") RETURN r"
	# print "Query : {}\n".format(query)
	return cypher.execute(query)


def _process_relationship_record(record):
	result = {}
	record = str(record[0])
	try:
		regex = r'^\(:([A-z0-9]+)\s?(?:\{(.*?)\})?\s?\)-\[([A-z0-9]+):([A-z0-9]+)\s?(?:\{(.*?)\})?\]\s?->\s?\(:([A-z0-9]+)\s?(?:\{(.*?)\})?\s?\)$'
		match = re.search(regex,record)
		if match is None:
			return None

		result['node_from'] = {}
		result['node_to'] = {}
		result['rel'] = {}

		result['node_from']['_label'] = match.group(1)
		if match.group(2) is not None:
			pairs = match.group(2).split(",")
			for pair in pairs:
				p = pair.split(':')
				result['node_from'][p[0]] = eval(p[1])

		result['node_to']['_label'] = match.group(6)
		if match.group(7) is not None:
			pairs = match.group(7).split(",")
			for pair in pairs:
				p = pair.split(':')
				result['node_to'][p[0]] = eval(p[1])

		result['rel']['_label'] = match.group(4)
		result['rel']['_id'] = match.group(3)
		if match.group(5) is not None:
			pairs = match.group(5).split(",")
			for pair in pairs:
				p = pair.split(':')
				result['rel'][p[0]] = eval(p[1])

	except:
		raise Exception("Invalid Relationship Record")

	return result
###################################### PY2NEO FUNCTIONS ###########################################