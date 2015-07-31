Data Locations
====

- Nodes that are a part of the graph (So things that NodeCollection holds) should all be added to postgres in their own table.
	- Need fast speed for the postitional query.
	- Nodes are also stored in Redis for memory-backed cache of nodes.

- Pathfinding results should be stored in Redis

- Schedules should be stored in postgres (relational database makes searching easier)
	- This will be a very verbose table. Each user will have every. single. class stored. I don't care about disk or memory usage, but speed on this query is absolutely key.