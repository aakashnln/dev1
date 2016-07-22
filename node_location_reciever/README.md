trackble-node
==============
Node backend for Android GPS Logger

Installing node in server <https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-an-ubuntu-14-04-server>

# Instructions

You will need:

- Node.js
- Socket.io
- Postgres/mongodb
- Webserver

## Installation

- Clone the project from `git clone https://github.com/rdeguzman/trackble-node.git`
- Install `pg` from npm: `npm install pg`
- Install `socket.io` from npm: `npm install socket.io`
- Install `mongodb` from npm: `npm install mongodb`
- Create the locations table:`psql -d trackble_production -U your_username -f docs/locations.sql`
- Set environment variables for postgres settings:
 
 	```
 	export PGUSER=rupert
 	export PGPASS=password
 	export PGDATABASE=trackable_production
 	```
 
- Change Google Map Key settings and socket_host in `map.html`
- Start the gps_server: `node server.js`





