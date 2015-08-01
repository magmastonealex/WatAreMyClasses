How to Import data from process.py
===

Once you've run the script, you're left with three new files: `buildings.redis`, `nodes.redis`, `nodes.sql`. The `.redis` files are for Redis, and the `.sql` files are for Postgres.

To load them:

```
redis-cli < buildings.redis
redis-cli < nodes.redis
```

Then, as the postgres user on Linux (`sudo su postgres`):

```
psql -f nodes.sql
```
