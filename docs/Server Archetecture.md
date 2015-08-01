Server Archetecture
===

- lighttpd
	- Small, scalable web server that supports running web.py applications natively.
	- varnish-cache is ready to deploy if it helps
		- Varnish will cache certain files and request types to respond much quicker than lighttpd.
- Redis
	- Redis is used as the memory cache for the app.  Redis is a Key-Value store. It uses strings as keys, and stores anything as the value. Redis caches found paths. **JSON is the internal format to be used with complex data and Redis! It makes it easier if we ever need to port the data or backend to something else!**
- PostgreSQL
	- PostgreSQL is a highly efficient and easy scalable DB. It also has great support for geospacial queries and working with Latitude/Longitude coordinates.
- web.py
	- web.py is a very fast, very small, and very easy-to-use Python web framework.
- pathServer
    - Alex wrote PathServer to prevent the web-tier from having to load the massive edge/nex dictionaries from files, instead they are kept in hot memory. Path Server communicates on TCP port 7284 (PATH :) ), and listens only on localhost. It takes as input a comma separated list of two nodes (ie: nodeid1,nodeid2), and returns a JSON array of the path to traverse them. Look at web/services/paths.py for more info on this.

Getting set up
---
Do the usual `pip install -r requirements.txt`.

If you're comfortable working in a VM, or run Linux natively, I highly reccommend it - makes setting up your dev environment much easier.

Postgres is organized into database>tables. We're using the default database.

Install and set up `postgres` and `redis` according to your favourite distro's guide. 


User for postgresql is postgres, get password from Alex. Very temporary, make it obvious and changable in your code! Also, make sure to set up your dev server with the same user and password so you don't end up with any issues:

1. `sudo su postgres`
2. `psql`
3. `alter user postgres with password 'password_from_alex';`
4. `\q`
5. `exit`


You'll need to also set it up to allow connections from localhost:

1. open /var/lib/pgsql/data/pg_hba.conf as root
2. find `# IPv4 local connections:` and `# IPv6 local connections:`
3. change peer/ident to md5




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

Install these schema by running the commands in the postgres prompt. (`sudo su postgres`, then `psql`, then c&p)

Run a local dev server by simply running 


The standard Redis notation uses ':' as a field separator. So, for examples, you might store the result of a path as: 'pathcache:node1:node2'. **All complex values should be in JSON!**

The `psychopg` and `redis` modules are used to connect to the respective datastores. Use `localhost` and default ports.  Redis doesn't use auth, postgres is detailed above.



