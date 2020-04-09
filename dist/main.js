"use strict";
exports.__esModule = true;
var express = require("express");
var routes_1 = require("./routes/routes"); // here
var app = express();
var port = 3000;
routes_1.RegisterRoutes(app); // and here
app.listen(port, function () { return console.log("Server started listening to port " + port); });
