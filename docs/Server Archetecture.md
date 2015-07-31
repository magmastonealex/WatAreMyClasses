Server Archetecture
===

- lighttpd
	- Small, scalable web server that supports running web.py applications natively.
	- varnish-cache is ready to deploy if it helps
		- Varnish will cache certain files and request types to respond much quicker than lighttpd.
- Redis
	- Redis is used as the memory cache for the app.  Redis is a Key-Value store. It uses strings as keys, and stores anything as the value. Redis caches found paths. **JSON is the internal format to be used with Redis! It makes it easier if we ever need to port the data or backend to something else!**
- PostgreSQL
	- PostgreSQL is a highly efficient and easy scalable DB. It also has great support for geospacial queries and working with Latitude/Longitude coordinates.
- web.py
	- web.py is a very fast, very small, and very easy-to-use Python web framework.

Getting set up
---
Do the usual `pip install -r requirements.txt`.

If you're comfortable working in a VM, or run Linux natively, I highly reccommend it - makes setting up your dev environment much easier.

Install and set up `postgres` and `redis` according to your favourite distro's guide.

Postgres is organized into database>tables. We're using the default database. User is wat, password is 'uwaterloo'. Very temporary, make it obvious and changable in your code!

Node schema:
```
CREATE TABLE nodes (
    id varchar(30) PRIMARY KEY,
    name varchar(200),
    lat double precision,
    long double precision
);
```
Timetable schema:

```
CREATE TABLE timetable (
    id serial primary key,
    cls varchar(200),
    tpe varchar(10),
    sec varchar(10),
    prof varchar(60),
    uname varchar(200),
    building varchar(10),
    time timestamp,
    time_end timestamp
);

CREATE INDEX uname_index ON timetable USING hash(uname);

```

The standard Redis notation uses ':' as a field separator. So, for examples, you might store the result of a path as: 'pathcache:node1:node2'. **All values should be in JSON!**

The `psychopg` and `redis` modules are used to connect to the respective datastores. Use `localhost` and default ports.  Redis doesn't use auth, postgres is detailed above.

