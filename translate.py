import re
from collections import defaultdict
qs = [
        'SELECT o FROM object o WHERE video="vid1.mp4,vid2.mp4, vid3.mp4" AND o.id=21',
        'SELECT o1 FROM object o1 WHERE o1.id=21 AND o1.gender="male"',
        'SELECT o FROM object o, event e WHERE video="*" AND o1.id=21 AND o1.gender="male" AND e.id="0"',
        'SELECT o1 FROM object o1, event e WHERE video="vid1.mp4" AND o1.id=21 AND o1.gender="male" AND e.id="0"',
        'SELECT o FROM object o WHERE video="vid1.mp4"',
        'SELECT e FROM event e WHERE video="vid1.mp4"',
        'SELECT o1 FROM object o1, object o2, event e WHERE video="vid1.mp4" AND o1.id=21 AND o1.gender="male" AND e.id="0"']

eqs = [
        'MATCH (v:Video)-[r:has_obj]->(o:Object) WHERE o.id=21 AND v.name in ["vid1.mp4", "vid2.mp4", "vid3.mp4"] RETURN o',
        'MATCH (v:Video)-[r2:has_obj]->(o1:Object) WHERE o1.id=21 AND o1.gender="male" RETURN o1',
        'MATCH (v:Video)-[r1:has_event]->(e:Event)-[r2:has_obj]->(o:Object) WHERE e.id = 0 and o.id = 1 RETURN o',
        'MATCH (v:Video)-[r1:has_event]->(e:Event)-[r2:has_obj]->(o:Object) WHERE v.name in ["vid1.mp4"] AND o1.id=21 AND o1.gender="male" AND e.id="0" RETURN o1',
        'MATCH (v:Video)-[r:has_obj]->(o:Object) WHERE v.name in ["vid1.mp4"] RETURN o',
        'MATCH (v:Video)-[r1:has_event]->(e:Event) WHERE v.name in ["vid1.mp4"] RETURN e',
        'MATCH (v:Video)-[r1:has_event]->(e:Event)-[r2:has_obj]->(o1:Object), (e)-[r3:has_obj]->(o2:Object) WHERE o1.id <> o2.id RETURN *']

cy_q = ""

def find_between(query, frm, to):
    try:
        start = query.index(frm) + len(frm)
        if to!="":
            end = query.index(to, start)
        else:
            end = len(query)
        return query[start:end]
    except ValueError:
        return ""

def find_select_phrase(query):
    return find_between(query, "SELECT ", "FROM").strip()

def find_from_phrase(query):
    return find_between(query, "FROM ", "WHERE").strip()

def find_where_phrase(query):
    return find_between(query, "WHERE ", "").strip()

def create_match_phrase(from_phrase, obj_alias, select_phrase, is_frame_query):
    match_phrase = ""
    if "object" in from_phrase and "event" in from_phrase:
        match_phrase = "MATCH (v:Video)-[r1:has_event]->(e:Event)-[r2:has_obj]->(o:Object)".replace("e:", obj_alias["event"][0]+":").replace("o:", obj_alias["object"][0]+":")
    elif "object" in from_phrase:
        match_phrase = "MATCH (v:Video)-[r2:has_obj]->(o:Object)".replace("o:", obj_alias["object"][0]+":")
    elif "event" in from_phrase:
        match_phrase = "MATCH (v:Video)-[r1:has_event]->(e:Event)".replace("o:", obj_alias["event"][0]+":")

    if len(obj_alias["object"]) > 1:
        match_phrase += ", (e)-[r3:has_obj]->(o2:Object)".replace("(e)", "(" + obj_alias["event"][0] + ")").replace("o2:", obj_alias["object"][1]+":")
    
    if is_frame_query:
        qtype = ""
        for key in obj_alias:
            if select_phrase in obj_alias[key]:
                qtype = key

        if qtype == "event":
            match_phrase += ", (v)-[rf:has_frame]->(f:frame)-[rf1:has_event]->(e)".replace("(e)", "(" + select_phrase + ")")
        else:
            match_phrase += ", (v)-[rf:has_frame]->(f:frame)-[rf1:has_object]->(o)".replace("(o)", "(" + select_phrase + ")")
    

    return match_phrase

def create_where_phrase(where_phrase, obj_alias):
    def repl(matchobj):
        if matchobj.group(1) == "*":
            return ""
        retstr = "v.name in ["
        for i, name in enumerate(matchobj.group(1).split(",")):
            name = name.strip()
            retstr += "'" + name + "'"
            if i != len(matchobj.group(1).split(","))-1 :
                retstr += ", "
        retstr += "]"

        if len(obj_alias["object"]) > 1:
            retstr += " AND " + obj_alias["object"][0] + "<>" + obj_alias["object"][1]
        return retstr
    vid_names = ""
    if "video" in where_phrase:
        where_phrase = re.sub(r'video="(.*?)"', repl, where_phrase)
    return " WHERE " + where_phrase

def create_return_phrase(select_phrase, is_frame_query):
    if is_frame_query:
        return " RETURN f, rf1 "

    return " RETURN " + select_phrase

def video_query(query):
    obj_alias = defaultdict(list)
    select_phrase = find_select_phrase(query)
    from_phrase = find_from_phrase(query)
    where_phrase = find_where_phrase(query)

    for sp in from_phrase.strip().split(","):
        sp = sp.strip()
        o_type, alias = sp.split(" ")
        obj_alias[o_type].append(alias)

    match_phrase = create_match_phrase(from_phrase, obj_alias, select_phrase, True)
    where_phrase = create_where_phrase(where_phrase, obj_alias)
    return_phrase = create_return_phrase(select_phrase, True)
    vid_q = match_phrase + where_phrase + return_phrase


    return vid_q


def node_query(query):
    obj_alias = defaultdict(list)
    select_phrase = find_select_phrase(query)
    from_phrase = find_from_phrase(query)
    where_phrase = find_where_phrase(query)

    for sp in from_phrase.strip().split(","):
        sp = sp.strip()
        o_type, alias = sp.split(" ")
        obj_alias[o_type].append(alias)

    match_phrase = create_match_phrase(from_phrase, obj_alias, select_phrase, False)
    where_phrase = create_where_phrase(where_phrase, obj_alias)
    return_phrase = create_return_phrase(select_phrase, False)
    cy_q = match_phrase + where_phrase + return_phrase

    return cy_q

for i in range(len(qs)):
    q = qs[i]
    print(q + "\n")
    eq = eqs[i]
    print(eq + "\n")
    cy_q = node_query(qs[i])
    print(cy_q + "\n")
    vid_q = video_query(qs[i])
    print(vid_q + "\n")
    print(50 * "*")
