import psycopg2


dbconn=psycopg2.connect("dbname='postgres' host='ssvps.magmastone.net' user='wat' password='uwaterloo'")


cur = dbconn.cursor()
ulat=43.470446
ulong=-80.538695
cur.execute("SELECT nodes.id, nodes.name, earth_distance(ll_to_earth("+str(ulat)+","+str(ulong)+" ), ll_to_earth(nodes.lat, nodes.long)) as distance_from_current_location FROM nodes ORDER BY distance_from_current_location ASC LIMIT 1;")

rows = cur.fetchall()
closestnode=rows[0]
print closestnode[0]