var http = require('http');
var url = require('url');
var qs = require('querystring');
var io = require('socket.io');
var fs = require('fs');
var Db = require('mongodb').Db,
    MongoClient = require('mongodb').MongoClient,
    Server = require('mongodb').Server,
    ReplSetServers = require('mongodb').ReplSetServers,
    ObjectID = require('mongodb').ObjectID,
    Binary = require('mongodb').Binary,
    GridStore = require('mongodb').GridStore,
    Grid = require('mongodb').Grid,
    Code = require('mongodb').Code,
//    BSON = require('mongodb').pure().BSON,
    assert = require('assert');
    
    // Set up the connection to the local db
var mongoclient = new MongoClient(new Server("localhost", 27017), {native_parser: true});


//var pg = require('pg');
var port = 8081;

var map_clients = [];

var PGUSER = process.env.PGUSER;
var PGPASS = process.env.PGPASS;
var PGDATABASE = process.env.PGDATABASE;
var connectionString = "postgres://" + PGUSER + ":" + PGPASS + "@localhost/" + PGDATABASE;
//console.log('connectionString:' + connectionString);

var route = {
  routes : {},
  for: function(method, path, handler){
    this.routes[method + path] = handler;
  }
}

route.for("POST", "/location", function(request, response){
  var form_data = "";
  request.on('data', function(chunk){
    form_data += chunk.toString();
  })

  request.on('end', function(){
    console.log(form_data);

    var obj = qs.parse(form_data);
    insertLocationM(obj);
    console.log("Connected clients: " + map_clients.length);

    for(var i=0; i < map_clients.length; i++){
      var client = map_clients[i];
      console.log("client.user_id:" + client.user_id);
      console.log("client.devices:" + client.devices);

      if (typeof client.devices != "undefined") {
        if(isAllowed(client.devices, obj.uuid)){
          console.log("Sending gps to viewer: " + client.user_id);
          console.log("Devices: " + client.devices);

          var jsonString = JSON.stringify({ type:'gps', data:obj});
          client.send(jsonString);
        }
      }

    }

    response.writeHead(200, {"Content-Type": "text/plain"});
    response.write("OK");
    response.end();
  })
});

function onRequest(request, response){
  var pathname = url.parse(request.url).pathname;
  console.log(request.method + " request for " + pathname);

  if(typeof(route.routes[request.method + pathname]) === 'function'){
    route.routes[request.method + pathname](request, response);
  }
  else{
    response.writeHead(404, {"Content-Type": "text/plain"});
    response.end("404 not found");
  }
}

function insertLocationM(loc){
//  pg.connect(connectionString, function(err, client, done) {
    
 // });
  // Connect using the connection string
  MongoClient.connect("mongodb://localhost:27017/test", {native_parser:true}, function(err, db) {
    assert.equal(null, err);
	
	if(err) {
      console.error('error fetching client from pool ', err);
    }
    else{
      if(typeof loc.provider == "undefined") loc.provider = "";
      if(typeof loc.time_interval == "undefined") loc.time_interval = -1;
      if(typeof loc.distance_interval == "undefined") loc.distance_interval = -1;

//     var sqlParams = [loc.uuid, loc.gps_timestamp, loc.gps_latitude, loc.gps_longitude, loc.gps_speed, loc.gps_heading, loc.provider, loc.time_interval];
	 db.collection('location_log').insert({device_uuid:loc.uuid,
                                  trip_uuid:loc.trip_id,//"1",
                                  campaign_id:loc.campaignId,// TODO convert campaignId to Long
	 								                gps_timestamp:loc.gps_timestamp,
                                  gps_loc:{
                                    "type": "Point",
                                    "coordinates": [parseFloat(loc.gps_longitude),parseFloat(loc.gps_latitude)]
                                  },
                                  gps_speed:parseFloat(loc.gps_speed),
                                  gps_heading:parseFloat(loc.gps_heading),
                                  gps_provider:loc.provider}, function(err, result) {
//      assert.equal(null, err);
//      assert.equal(1, result);

      db.close();
    });

      //done();
    }
    

  });
}

function insertLocation(loc){
  pg.connect(connectionString, function(err, client, done) {
    if(err) {
      console.error('error fetching client from pool ', err);
    }
    else{
      if(typeof loc.provider == "undefined") loc.provider = "";
      if(typeof loc.time_interval == "undefined") loc.time_interval = -1;
      if(typeof loc.distance_interval == "undefined") loc.distance_interval = -1;

      var sqlStmt  = "INSERT INTO locations(";
          sqlStmt += "uuid,";
          sqlStmt += "gps_timestamp,";
          sqlStmt += "gps_latitude,";
          sqlStmt += "gps_longitude,";
          sqlStmt += "gps_speed,";
          sqlStmt += "gps_heading,";
          sqlStmt += "provider,";
          sqlStmt += "time_interval,";
          sqlStmt += "distance_interval,";
          sqlStmt += "created_at)";
          sqlStmt += "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, Now())";

      var sqlParams = [loc.uuid, loc.gps_timestamp, loc.gps_latitude, loc.gps_longitude, loc.gps_speed, loc.gps_heading, loc.provider, loc.time_interval, loc.distance_interval];

      var query = client.query(sqlStmt, sqlParams, function(err, result){
        if(err){
          console.error('error inserting ', err);
        }
        else{
          console.log(result);
        }

      });

      done();
    }
  });
}

function isAllowed(devices_array, uuid){
  return devices_array.indexOf(uuid) > -1;
}

var server = http.createServer(onRequest);
server.listen(port);
console.log("Server " + port + " has started.");

io = io.listen(server);

io.sockets.on("connection", function(client){
  // We push the map clients to an array.
  // If a gps is received from a device,
  // we broadcast the gps to all map clients.
  map_clients.push(client);

  client.on('setUserId',function(user_id){
    console.log("Map client connected for user_id: " + user_id);
    client.user_id = user_id;
  });

  client.on('addDevice',function(device_id){
    console.log("Add device_id: " + device_id);

    if (typeof client.devices == "undefined") {
      client.devices = [];
    }

    client.devices.push(device_id);
  });


  client.on('disconnect', function(){
    map_clients.splice(map_clients.indexOf(client), 1);
  })

});


