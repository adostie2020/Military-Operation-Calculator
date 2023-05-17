import uuid
import json
import random
import requests
import pymongo
import datetime
from duffel_api import Duffel
from flask_cors import CORS #comment this on deployment
from passlib.hash import sha256_crypt
from flask import Flask, jsonify, request, make_response


app = Flask(__name__, static_folder="fe/fe/build", static_url_path="")
CORS(app) #comment this on deployment
client = Duffel(access_token = "duffel_test_wR7qOeLxoMTMziq7CGRJcKR6as2tvwQnuMoVVR0ESfj")
mongoclient = pymongo.MongoClient("mongodb+srv://Test:Test@cluster0.fkr6war.mongodb.net/?retryWrites=true&w=majority")["PACAF"]
draftscoll = mongoclient["Drafts"]
archivecoll = mongoclient["Archive"]
accountscoll = mongoclient["Accounts"]
aircraftcoll = mongoclient["Aircraft-table"]
exercisecoll = mongoclient["Exercise-table"]
lodgingcoll = mongoclient["Lodging-table"]

"""
-- DRAFTS AND ARCHIVE ROUTES --
"""

@app.route("/api/get_drafts") # ROUTE COMPLETE
def drafts():
  account = accountscoll.find_one({"token": request.cookies.get("token")})
  if account == None:
    return jsonify({"success": False, "reason": "unauthorized"}), 401
  drafts = {"success": True, "reason": "none", "drafts": []}
  for draft in draftscoll.find({}, {"_id": 0}):
    if draft["owner"] == account["uid"]:
      drafts["drafts"].append(draft)
  if len(drafts["drafts"]) != 0:
    drafts["drafts"] = sorted(drafts["drafts"], key=lambda e: e["createdAt"], reverse=True)
  else:
    drafts["drafts"] = ["none"]
  return jsonify(drafts)
               
@app.route("/api/get_archive") # ROUTE COMPLETE
def archive():
  account = accountscoll.find_one({"token": request.cookies.get("token")})
  if account == None:
    return jsonify({"success": False, "reason": "unauthorized"}), 401
  archive = {"success": True, "reason": "none", "archive": []}
  for finished in archivecoll.find({}, {"_id": 0}):
    if archive["owner"] == account["uid"]:
      archive.append(finished)
  if len(archive["archive"]) != 0:
    archive["archive"] = sorted(archive["archive"], key=lambda e:e["createdAt"], reverse=True)
  else:
    archive["archive"] = ["none"]
  return jsonify(archive)
    
@app.route("/api/empty_archive") # ROUTE COMPLETE
def emptyarchive():
  account = accountscoll.find_one({"token": request.cookies.get("token")})
  if account == None:
    return jsonify({"success": False, "reason": "unauthorized"}), 401
  archivecoll.delete_many({"owner": account["uid"]})
  return jsonify({"success": True, "reason": "none"})

@app.route("/api/archive_draft") # ROUTE COMPLETE
def archiveDraft():
  try:
    query = int(request.args.get("id"))
  except:
    return jsonify({"success": False, "reason": "malformed"}), 400
  account = accountscoll.find_one({"token": request.cookies.get("token")})
  if account == None:
    return jsonify({"success": False, "reason": "unauthorized"}), 401
  draft = draftscoll.find_one({"id": query})
  if draft == None:
    return jsonify({"success": False, "reason": "invalid_id"})
  if draft["owner"] == account["uid"]:
    archivecoll.insert_one(draft)
    draftscoll.delete_one({"id": query})
    return jsonify({"success": True, "reason": "none"})
  return jsonify({"success": False, "reason": "unauthorized"}), 401

@app.route("/api/restore_draft") # ROUTE COMPLETE
def restoreDraft():
  try:
    query = int(request.args.get("id"))
  except:
    return jsonify({"success": False, "reason": "malformed"}), 400
  account = accountscoll.find_one({"token": request.cookies.get("token")})
  if account == None:
    return jsonify({"success": False, "reason": "unauthorized"}), 401
  archived = archivecoll.find_one({"id": query})
  if archived == None:
    return jsonify({"success": False, "reason": "invalid_id"})
  if archived["owner"] == account["uid"]:
    draftscoll.insert_one(archived)
    archivecoll.delete_one({"id": query})
    return jsonify({"success": True, "reason": "none"})
  return jsonify({"success": False, "reason": "unauthorized"}), 401


"""
-- ACCOUNT ROUTES --
"""


@app.route("/api/registration", methods=["POST"]) # ROUTE COMPLETE
def registerUser():
  username = request.json.get("username")
  password = request.json.get("password")
  email = request.json.get("email")
  existing = accountscoll.find_one({"token": request.cookies.get("token")})
  if existing != None:
    return jsonify({"success": False, "reason": "loggedin"})
  if all([username, password, email]):
    existing = accountscoll.find_one({"$or": [{"username": username}, {"email": email}]})
    if existing != None:
      return jsonify({"success": False, "reason": "invalid_data"})
    if len(username) < 4 or len(username) > 20:
      return jsonify({"success": False, "reason": "invalid_username"})
    if len(email) < 4 or len(email) > 20 or not "@" in list(email):
      return jsonify({"success": False, "reason": "invalid_email"})
    if len(password) < 8 or len(password) > 20 or password.isalpha() or password.lower() == password:
      return jsonify({"success": False, "reason": "invalid_password"})
    else:
      while True:
        uid = ""
        for num in range(6):
          uid = uid + str(random.randint(0, 9))
        if accountscoll.find_one({"uid": uid}) == None:
          break
      token = uuid.uuid1().hex
      accountscoll.insert_one({"username": request.json.get("username"), "password": '{"hash": "' + sha256_crypt.hash(password) + '"}', "email": email, "token": token, "uid": int(uid), "admin": False})
      response = make_response(jsonify({"success": True, "reason": "none"}))
      response.set_cookie("token", token, secure=True, httponly=True)
      return response

@app.route("/api/login", methods=["POST"]) # ROUTE COMPLETE
def login():
  username = request.json.get("username")
  password = request.json.get("password")
  existing = accountscoll.find_one({"token": request.cookies.get("token")})
  if existing != None:
    return jsonify({"success": False, "reason": "loggedin"})
  account = accountscoll.find_one({"$or": [{"username": username}, {"email": username}]})
  if account == None:
    return jsonify({"success": False, "reason": "invalid"})
  if sha256_crypt.verify(password, json.loads(account["password"])["hash"]):
    response = make_response(jsonify({"success": True, "reason": "none"}))
    response.set_cookie("token", account["token"], secure=True, httponly=True)
    return response
  else:
    return jsonify({"success": False, "reason": "invalid"})
      

"""
-- AIRCRAFT ROUTES -- (Needs delete route)
"""


@app.route("/api/add_aircraft", methods=["POST"]) # ROUTE COMPLETE
def addAircraft():
  type = request.json.get("type")
  number = request.json.get("number")
  personnel = request.json.get("personnel")
  print(personnel)
  existing = accountscoll.find_one({"token": request.cookies.get("token")})
  #if existing == None:
    #return jsonify({"success": False, "reason": "unauthorized"}), 401
  if all([type, number, personnel]) and isinstance(number, int) and isinstance(personnel, int):
    if number < 0 or number > 100:
      return jsonify({"success": False, "reason": "invalid_number"})
    if personnel < 1 or personnel > 100:
      return jsonify({"success": False, "reason": "invalid_personnel"})
    if len(type) < 2 or len(type) > 20:
      return jsonify({"success": False, "reason": "invalid_type"})
    while True:
      id = ""
      for num in range(6):
        id = id + str(random.randint(0, 9))
      if exercisecoll.find_one({"uid": id}) == None:
        break
    aircraftcoll.insert_one({"aircraft-type": type, "aircraft-number": number, "number-personnel": personnel, "id": id})
    return jsonify({"success": True, "reason": "none"})
  else:
    return jsonify({"success": False, "reason": "missing_data"})

@app.route("/api/get_aircraft") # ROUTE COMPLETE
def getAircraft():
  existing = accountscoll.find_one({"token": request.cookies.get("token")})
  #if existing == None:
    #return jsonify({"success": False, "reason": "unauthorized"}), 401
  aircrafts = []
  for aircraft in aircraftcoll.find({}, {"_id": 0}):
    aircrafts.append({"type": aircraft["aircraft-type"], "number": aircraft["aircraft-number"], "personnel": aircraft["number-personnel"], "id": aircraft["id"]})
  return jsonify({"success": True, "reason": "none", "aircrafts": aircrafts})


"""
-- EXERCISE ROUTES -- (Needs delete route)
"""


@app.route("/api/add_exercise", methods=["POST"]) 
def addExercise():
  name = request.json.get("name")
  location = request.json.get("location")
  existing = accountscoll.find_one({"token": request.cookies.get("token")})
  #if existing == None:
    #return jsonify({"success": False, "reason": "unauthorized"}), 401
  if all([name, location]):
    if len(name) < 2 or len(name) > 40:
      return jsonify({"success": False, "reason": "invalid_name"})
    if len(location) < 4 or len(location) > 4:
      return jsonify({"success": False, "reason": "invalid_location"})
    while True:
      id = ""
      for num in range(6):
        id = id + str(random.randint(0, 9))
      if exercisecoll.find_one({"uid": id}) == None:
        break
    exercisecoll.insert_one({"name": str(name), "location": str(location), "id": id})
    return jsonify({"success": True, "reason": "none"})
  else:
    return jsonify({"success": False, "reason": "missing_data"})

@app.route("/api/get_exercise")
def getExercise():
  existing = accountscoll.find_one({"token": request.cookies.get("token")})
  #if existing == None:
    #return jsonify({"success": False, "reason": "invalid"})
  exercises = []
  for exercise in exercisecoll.find({}, {"_id": 0}):
    exercises.append({"name": exercise["name"], "location": exercise["location"], "id": exercise["id"]})             
  return jsonify({"success": True, "reason": "none", "exercises": exercises})

@app.route("/api/delete_exercise") # WIP
def deleteExercise():
  query = request.json.get("uid")
  existing = accountscoll.find_one({"token": request.cookies.get("token")})
  #if existing == None:
    #return jsonify({"success": False, "reason": "invalid"})
  retval = exercisecoll.find_one({"uid": query})
  if retval["owner"] == existing["uid"]:
    exercisecoll.delete_one({"uid": query})
    return jsonify({"success": True, "reason": "none", "removed": retval})
  else:
    return jsonify({"success": True, "reason": "none", "removed": "none"})

"""
-- FORM ROUTES -- (WIP)
"""


@app.route("/api/flight_details") # ROUTE COMPLETE
def flights():
  fromloc = request.args.get("from")
  toloc = request.args.get("to")
  date = request.args.get("date")
  if all([fromloc, toloc, date]):
    if len(fromloc) > 4:
      return jsonify({"success": False, "reason": "invalid_from"})
    if len(toloc) > 4 or toloc == toloc:
      return jsonify({"success": False, "reason": "invalid_to"})
    try:
      date = datetime.datetime.strptime(date, "%Y-%m-%d")
      if datetime.datetime.now() > date:
        return jsonify({"success": False, "reason": "invalid_date"})
    except:
      return jsonify({"success": False, "reason": "invalid_date"})
  else:
    return jsonify({"success": False, "reason": "missing_data"})
  try:
    offers = (
    client.offer_requests.create()
    .passengers([{"type": "adult"}])
    .slices([{"origin": fromloc, "destination": toloc, "departure_date": date}])
    .return_offers()
    .execute()).offers if request.args.get("round") != True else (
    client.offer_requests.create()
    .passengers([{"type": "adult"}])
    .slices([{"origin": fromloc, "destination": toloc, "departure_date": date}, {"origin": toloc, "destination": fromloc, "departure_date": date}])
    .return_offers()
    .execute()).offers
    flight = []
    for offer in offers:
      flight.append({"id": offer.id, "airline": offer.owner.name, "departs": offer.slices[0].segments[0].departing_at, "cost": offer.total_amount, "currency": offer.total_currency})
    flight.sort(key=lambda e: e["cost"])
  except:
    return jsonify({"success": False, "reason": "unexpected_error"})
  return jsonify({"success": True, "reason": "none", "flight": flight[0]})


# f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=5000&type=lodging&key={api_key}"
@app.route("/api/hotels") # ROUTE COMPLETE
def hotels():
  """
  -- Checks --
  Here, we check that the user provided a valid IATA code.
  """
  code = request.args.get("code")
  if request.args.get("code") != None:
    if len(code) > 4:
      return jsonify({"success": False, "reason": "invalid_iata"})
  else:
    return jsonify({"success": False, "reason": "missing_data"})
  """
  -- Get Nearby Hotels --
  Now that we've confirmed the user provided a valid IATA code, we can now get nearby hotels.
  """
  key = "AIzaSyCiw7ggDVbJ3R9KJsO04rC8MpZUYOynxpQ"
  airport = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={code}+airport").json()
  data = requests.get(f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={float(airport[0]['lat'])},{float(airport[0]['lon'])}&radius=5000&type=lodging&key={key}").json()
  hotels = []
  for hotel in data["results"]:
      hotels.append({"name": hotel["name"], "address": hotel["vicinity"], "rating": hotel.get("rating", "No Ratings")})
  return jsonify({"success": True, "reason": "none", "hotels": hotels})


"""
-- REACT ROUTES --
"""


# Serve the react routes
@app.route("/", defaults={"path": ""})
def react(path):
  return app.send_static_file("index.html")


app.run(host="0.0.0.0", port=8000)