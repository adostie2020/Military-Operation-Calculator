import re
import uuid
import json
import random
import requests
import pymongo
import datetime
from bson import json_util
from duffel_api import Duffel
from flask_cors import CORS #comment this on deployment
from bs4 import BeautifulSoup
from passlib.hash import sha256_crypt
from flask import Flask, jsonify, request, make_response, send_from_directory


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


@app.route("/api/archive_save", methods=["POST"])
def saveToArchive():
  try:
    #account = accountscoll.find_one({"token": request.cookies.get("token")})
    #if account == None:
      #return jsonify({"success": False, "reason": "unauthorized"}), 401
    while True:
      id = ""
      for num in range(6):
        id += str(random.randint(0, 9))
      if archivecoll.find_one({"uid": id}) == None:
        break
    archived = {"id": id}
    variables = ["exerciseName", "supporters", "fromLocation", "toLocation", "startDate", "endDate", "flightCost", "dataMeals", "dataRate", "peopleCommercialAir", "peopleCommercialMilitary", "governmentLodging", "commercialLodging", "woodsLodging", "peopleperdiemRate", "peopleperdiemFood", "total"]
    for v in variables:
      item = request.json["body"].get(v)
      if item == None:
        return jsonify({"success": False, "reason": f"missing_{v}"}), 400
      if len(str(item)) < 1 or len(str(item)) > 50:
        return jsonify({"success": False, "reason": f"invalid_{v}"}), 400
      if isinstance(item, str) and item.isnumeric():
        item = int(item)
      archived[v] = item
    archived["createdAt"] = datetime.datetime.now().strftime("%Y-%m-%d")
    archivecoll.insert_one(archived)
    return jsonify({"success": True, "reason": "none"})
  except Exception as e:
    print(e)
    return jsonify({"success": False, "reason": "server_error"}), 500

@app.route("/api/archive")
def archiveViewer():
  try:
    query = request.args.get("id")
    account = accountscoll.find_one({"token": request.cookies.get("token")})
    if account == None:
      return jsonify({"success": False, "reason": "unauthorized"}), 401
    try:
      query = int(query)
    except:
      return jsonify({"success": False, "reason": "invalid_id"}), 400
    result = {"success": True, "reason": "none", "archive": {}}
    archive = archivecoll.find_one({"id": query})
    if archive == None:
      return jsonify({"success": False, "reason": "not_found"}), 404
    del archive["_id"]
    result["archive"] = archive
    return jsonify(result)
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500

@app.route("/api/get_drafts") # ROUTE COMPLETE
def drafts():
  try:
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
    return jsonify(drafts), 200
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500
               
@app.route("/api/get_archive") # ROUTE COMPLETE
def archive():
  try:
    account = accountscoll.find_one({"token": request.cookies.get("token")})
    #if account == None:
      #return jsonify({"success": False, "reason": "unauthorized"}), 401
    archive = {"success": True, "reason": "none", "archive": []}
    for finished in archivecoll.find({}, {"_id": 0}):
      #if finished["owner"] == account["uid"]:
      archive["archive"].append(finished)
    if len(archive["archive"]) != 0:
      archive["archive"] = sorted(archive["archive"], key=lambda e:e["createdAt"], reverse=True)
    else:
      archive["archive"] = ["none"]
    return jsonify(archive), 200
  except Exception as e:
    print(e)
    return jsonify({"success": False, "reason": "server_error"}), 500
    
@app.route("/api/empty_archive", methods=["POST"]) # ROUTE COMPLETE
def emptyArchive():
  try:
    account = accountscoll.find_one({"token": request.cookies.get("token")})
    if account == None:
      return jsonify({"success": False, "reason": "unauthorized"}), 401
    archivecoll.delete_many({"owner": account["uid"]})
    return jsonify({"success": True, "reason": "none"}), 200
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500

@app.route("/api/archive_draft", methods=["POST"]) # ROUTE COMPLETE
def archiveDraft():
  try:
    query = request.json.get("id")
    if not isinstance(query, int):
      return jsonify({"success": False, "reason": "invalid_id"}), 400
    account = accountscoll.find_one({"token": request.cookies.get("token")})
    if account == None:
      return jsonify({"success": False, "reason": "unauthorized"}), 401
    draft = draftscoll.find_one({"id": query})
    if draft == None:
      return jsonify({"success": False, "reason": "invalid_id"}), 400
    if draft["owner"] == account["uid"]:
      archivecoll.insert_one(draft)
      draftscoll.delete_one({"id": query})
      return jsonify({"success": True, "reason": "none"}), 200
    return jsonify({"success": False, "reason": "unauthorized"}), 401
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500

@app.route("/api/restore_draft", methods=["POST"]) # ROUTE COMPLETE
def restoreDraft():
  try:
    query = request.json.get("id")
    if not isinstance(query, int):
      return jsonify({"success": False, "reason": "invalid_id"}), 400
    account = accountscoll.find_one({"token": request.cookies.get("token")})
    if account == None:
      return jsonify({"success": False, "reason": "unauthorized"}), 401
    archived = archivecoll.find_one({"id": query})
    if archived == None:
      return jsonify({"success": False, "reason": "invalid_id"}), 400
    if archived["owner"] == account["uid"]:
      draftscoll.insert_one(archived)
      archivecoll.delete_one({"id": query})
      return jsonify({"success": True, "reason": "none"}), 200
    return jsonify({"success": False, "reason": "unauthorized"}), 401
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500


"""
-- ACCOUNT ROUTES --
"""


@app.route("/api/registration", methods=["POST"]) # ROUTE COMPLETE
def registerUser():
  try:
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")
    existing = accountscoll.find_one({"token": request.cookies.get("token")})
    if existing != None:
      return jsonify({"success": False, "reason": "loggedin"}), 200
    if all([username, password, email]):
      existing = accountscoll.find_one({"$or": [{"username": username}, {"email": email}]})
      if existing != None:
        return jsonify({"success": False, "reason": "invalid_data"}), 400
      if len(username) < 4 or len(username) > 20:
        return jsonify({"success": False, "reason": "invalid_username"}), 400
      if len(password) < 8 or len(password) > 40 or password.isalpha() or password.lower() == password:
        return jsonify({"success": False, "reason": "invalid_password"}), 400
      if len(email) < 4 or len(email) > 20 or not "@" in list(email):
        return jsonify({"success": False, "reason": "invalid_email"}), 400
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
        return response, 200
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500

@app.route("/api/login", methods=["POST"]) # ROUTE COMPLETE
def login():
  try:
    username = request.json.get("username")
    password = request.json.get("password")
    existing = accountscoll.find_one({"token": request.cookies.get("token")})
    if existing != None:
      return jsonify({"success": False, "reason": "loggedin"}), 200
    account = accountscoll.find_one({"$or": [{"username": username}, {"email": username}]})
    if account == None:
      return jsonify({"success": False, "reason": "invalid"}), 400
    if sha256_crypt.verify(password, json.loads(account["password"])["hash"]):
      response = make_response(jsonify({"success": True, "reason": "none"}))
      response.set_cookie("token", account["token"], secure=True, httponly=True)
      return response, 200
    return jsonify({"success": False, "reason": "invalid"}), 400
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500

@app.route("/api/validate") # ROUTE COMPLETE
def validate():
  try:
    existing = accountscoll.find_one({"token": request.cookies.get("token")})
    if existing != None:
      return jsonify({"success": True, "reason": "valid_token"}), 200
    return jsonify({"success": False, "reason": "invalid_token"}), 400
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500
      

  
"""
-- AIRCRAFT ROUTES --
"""


@app.route("/api/add_aircraft", methods=["POST"]) # ROUTE COMPLETE
def addAircraft():
  try:
    type = request.json.get("type")
    number = request.json.get("number")
    personnel = request.json.get("personnel")
    print(personnel)
    existing = accountscoll.find_one({"token": request.cookies.get("token")})
    #if existing == None:
      #return jsonify({"success": False, "reason": "unauthorized"}), 401
    if all([type, number, personnel]) and isinstance(number, int) and isinstance(personnel, list):
      if number < 0 or number > 100:
        return jsonify({"success": False, "reason": "invalid_number"}), 400
      if len(personnel) < 1 or len(personnel) > 1000:
        return jsonify({"success": False, "reason": "invalid_personnel"}), 400
      if len(type) < 2 or len(type) > 20:
        return jsonify({"success": False, "reason": "invalid_type"}), 400
      while True:
        id = ""
        for num in range(6):
          id = id + str(random.randint(0, 9))
        if exercisecoll.find_one({"uid": id}) == None:
          break
      aircraftcoll.insert_one({"type": type, "personnel": personnel, "id": int(id)})
      return jsonify({"success": True, "reason": "none"}), 200
    else:
      return jsonify({"success": False, "reason": "missing_data"}), 400
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500

@app.route("/api/get_aircraft") # ROUTE COMPLETE
def getAircraft():
  try:
    existing = accountscoll.find_one({"token": request.cookies.get("token")})
    #if existing == None:
      #return jsonify({"success": False, "reason": "unauthorized"}), 401
    aircrafts = []
    for aircraft in aircraftcoll.find({}, {"_id": 0}):
      aircrafts.append({"type": aircraft["type"], "personnel": aircraft["personnel"], "id": aircraft["id"]})
    return jsonify({"success": True, "reason": "none", "aircrafts": aircrafts}), 200
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500

@app.route("/api/delete_aircraft", methods=["POST"])
def deleteAircraft():
  try:
    query = request.json.get("id")
    existing = accountscoll.find_one({"token": request.cookies.get("token")})
    #if existing == None:
      #return jsonify({"success": False, "reason": "unauthorized"}), 401
    if aircraftcoll.find_one({"id": query}) == None:
      return jsonify({"success": True, "reason": "not_found"}), 404
    aircraftcoll.delete_one({"id": query})
    return jsonify({"success": True, "reason": "none"}), 200
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500

@app.route("/api/edit_aircraft", methods=["POST"])
def editAircraft():
  try:
    query = request.json.get("id")
    newtype = request.json.get("type")
    newpersonnel = request.json.get("personnel")
    existing = accountscoll.find_one({"token": request.cookies.get("token")})
    #if existing == None:
      #return jsonify({"success": False, "reason": "unauthorized"}), 401
    if len(newtype) < 2 or len(newtype) > 40:
      return jsonify({"success": False, "reason": "invalid_type"}), 400
    if len(newpersonnel) < 0:
      return jsonify({"success": False, "reason": "invalid_personnel"}), 400
    old = aircraftcoll.find_one({"id": query})
    if old == None:
      return jsonify({"success": False, "reason": "not_found"}), 404
    old["type"] = newtype
    old["personnel"] = newpersonnel
    aircraftcoll.update_one({"id": query}, {"$set": old})
    return jsonify({"success": True, "reason": "none"}), 200
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500
  

"""
-- EXERCISE ROUTES --
"""


@app.route("/api/add_exercise", methods=["POST"]) 
def addExercise():
  try:
    name = request.json.get("name")
    location = request.json.get("location")
    existing = accountscoll.find_one({"token": request.cookies.get("token")})
    #if existing == None:
      #return jsonify({"success": False, "reason": "unauthorized"}), 401
    if all([name, location]):
      if len(name) < 2 or len(name) > 40:
        return jsonify({"success": False, "reason": "invalid_name"}), 400
      if len(location) < 0 or len(location) > 4:
        return jsonify({"success": False, "reason": "invalid_location"}), 400
      while True:
        id = ""
        for num in range(6):
          id = id + str(random.randint(0, 9))
        if exercisecoll.find_one({"uid": id}) == None:
          break
      exercisecoll.insert_one({"name": str(name), "location": str(location), "id": int(id)})
      return jsonify({"success": True, "reason": "none"}), 200
    else:
      return jsonify({"success": False, "reason": "missing_data"}), 400
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500

@app.route("/api/get_exercise")
def getExercise():
  try:
    existing = accountscoll.find_one({"token": request.cookies.get("token")})
    #if existing == None:
      #return jsonify({"success": False, "reason": "unauthorized"}), 401
    exercises = []
    for exercise in exercisecoll.find({}, {"_id": 0}):
      exercises.append({"name": exercise["name"], "location": exercise["location"], "id": exercise["id"]})             
    return jsonify({"success": True, "reason": "none", "exercises": exercises}), 200
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500

@app.route("/api/exercise")
def exercise():
  try:
    id = request.args.get("id")
    existing = accountscoll.find_one({"token": request.cookies.get("token")})
    #if existing == None:
      #return jsonify({"success": False, "reason": "unauthorized"}), 401
    if not isinstance(id, int):
      return jsonify({"success": False, "reason": "invalid_id"}), 400
    exercise = exercisecoll.find_one({"id": id})
    if exercise == None:
      return jsonify({"success": False, "reason": "not_found"}), 404
    return jsonify({"success": True, "reason": "none", "exercise": {"name": exercise["name"], "location": exercise["location"], "id": exercise["id"]}}), 200
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500

@app.route("/api/delete_exercise", methods=["POST"])
def deleteExercise():
  try:
    query = request.json.get("id")
    existing = accountscoll.find_one({"token": request.cookies.get("token")})
    #if existing == None:
      #return jsonify({"success": False, "reason": "unauthorized"}), 401
    if exercisecoll.find_one({"id": query}) == None:
      return jsonify({"success": False, "reason": "not_found"}), 404
    exercisecoll.delete_one({"id": query})
    return jsonify({"success": True, "reason": "none"}), 200
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500

@app.route("/api/edit_exercise", methods=["POST"])
def editExercise():
  try:
    query = request.json.get("id")
    newname = request.json.get("name")
    newlocation = request.json.get("location")
    existing = accountscoll.find_one({"token": request.cookies.get("token")})
    #if existing == None:
      #return jsonify({"success": False, "reason": "unauthorized"}), 401
    if len(newname) < 2 or len(newname) > 40:
      return jsonify({"success": False, "reason": "invalid_name"}), 400
    if len(newlocation) < 0 or len(newlocation) > 4:
      return jsonify({"success": False, "reason": "invalid_location"}), 400
    old = exercisecoll.find_one({"id": query})
    if old == None:
      return jsonify({"success": False, "reason": "not_found"}), 404
    old["name"] = newname
    old["location"] = newlocation
    exercisecoll.update_one({"id": query}, {"$set": old})
    return jsonify({"success": True, "reason": "none"}), 200
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500


"""
-- FORM ROUTES -- (WIP)
""" # very great code (approved for use as of now)




@app.route("/api/flight_details") # ROUTE COMPLETE
def flights():
  key = "AIzaSyCiw7ggDVbJ3R9KJsO04rC8MpZUYOynxpQ"
  fromloc = request.args.get("from").lower()
  toloc = request.args.get("to").lower()
  date = request.args.get("date")
  data = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={fromloc}&key={key}").json()
  fromloc = requests.get(f'http://iatageo.com/getCode/{data["results"][0]["geometry"]["location"]["lat"]}/{data["results"][0]["geometry"]["location"]["lng"]}').json()["IATA"]
  data = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={toloc}&key={key}").json()
  toloc = requests.get(f'http://iatageo.com/getCode/{data["results"][0]["geometry"]["location"]["lat"]}/{data["results"][0]["geometry"]["location"]["lng"]}').json()["IATA"]
  if all([fromloc, toloc, date]):
    if len(fromloc) < 1:
      return jsonify({"success": False, "reason": "invalid_from"}), 400
    if len(toloc) < 1 or fromloc == toloc:
      return jsonify({"success": False, "reason": "invalid_to"}), 400
    try:
      dateobject = datetime.datetime.strptime(date, "%Y-%m-%d")
      if datetime.datetime.now() > dateobject:
        return jsonify({"success": False, "reason": "invalid_date"}), 400
    except:
      return jsonify({"success": False, "reason": "invalid_date"}), 400
  else:
    return jsonify({"success": False, "reason": "missing_data"}), 400
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
      flight.append({"id": offer.id, "airline": offer.owner.name, "departs": offer.slices[0].segments[0].departing_at, "cost": offer.total_amount, "currency": offer.total_currency,  "from": fromloc, "to": toloc})
    flight.sort(key=lambda e: e["cost"])
  except Exception as e:
    return jsonify({"success": False, "reason": "server_error"}), 500
  return jsonify({"success": True, "reason": "none", "flight": flight[0]}), 200


@app.route("/api/pdrates")
def PDRates():
  try:
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))
    state = request.args.get("state")
    city = request.args.get("city")
  except:
    return jsonify({"success": False, "reason": "invalid_datatype"}), 400
  if len(str(year)) < 0 or len(str(year)) > 4:
    return jsonify({"success": False, "reason": "invalid_year"}), 400
  if len(str(month)) < 0 or len(str(month)) > 2:
    return jsonify({"success": False, "reason": "invalid_month"}), 400
  try:
    datetime.datetime.strptime(f"{year}-0{month}-01", "%Y-%m-%d")
  except:
    return jsonify({"success": False, "reason": "date_error"}), 400
  try:
    currentyear = int(datetime.datetime.now().strftime("%Y"))
    nextyear = month > 8 and currentyear > year
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    if month > 8 and currentyear == year:
      return jsonify({"success": False, "reason": "no_rates_available"}), 200
    if currentyear - 3 > year:
      return jsonify({"success": False, "reason": "no_rates_available"}), 200
    html = requests.get(f"https://www.gsa.gov/travel/plan-book/per-diem-rates/per-diem-rates-results/?fiscal_year={year if nextyear == False else year + 1}&state={state}&perdiemSearchVO_city={city}&action=perdiems_report&zip=&op=Find+Rates&form_build_id=form-GGHt7ZcnOjh5MtzZ4RJnygTl3DivBQfZf_k071phWGU&form_id=perdiem_form")
    page = BeautifulSoup(html.text, "html.parser")
    rate = re.sub(r'\$| USD', '', page.find("td", attrs={"headers": f"maxLodging y{year} {months[month]}"}).text)
    meals = re.sub(r'\$| USD', '', page.find("td", attrs={"headers": "MIE"}).text)
    return jsonify({"success": True, "reason": "none", "rate": rate, "meals": meals, "total": int(rate) + int(meals)}), 200
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500


@app.route("/api/hotels") # ROUTE COMPLETE
def hotels():
  try:
    key = "AIzaSyCiw7ggDVbJ3R9KJsO04rC8MpZUYOynxpQ"
    code = request.args.get("location")
    if code != None:
      if len(code) > 20:
        return jsonify({"success": False, "reason": "invalid_location"}), 400
    else:
      return jsonify({"success": False, "reason": "missing_data"}), 400
    data = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={code}&key={key}").json()
    data = requests.get(f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={data['results'][0]['geometry']['location']['lat']},{data['results'][0]['geometry']['location']['lng']}&radius=32187&type=lodging&key={key}").json()
    hotels = []
    for hotel in data["results"]:
      hotels.append({"name": hotel["name"], "address": hotel["vicinity"], "rating": hotel.get("rating", "No Ratings")})
    return jsonify({"success": True, "reason": "none", "hotels": hotels}), 200
  except:
    return jsonify({"success": False, "reason": "server_error"}), 500


"""
-- REACT ROUTES --
"""

@app.route("/")
@app.route("/<route>")
def routeHandler(route=None):
  return app.send_static_file("index.html"), 200



app.run(host="0.0.0.0", port=8000)