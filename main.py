import json
import pymongo
import datetime
from duffel_api import Duffel
from passlib.hash import sha256_crypt
from flask import Flask, jsonify, request, make_response


app = Flask(__name__, static_folder="fe/fe/build", static_url_path="")
client = Duffel(access_token = "duffel_test_wR7qOeLxoMTMziq7CGRJcKR6as2tvwQnuMoVVR0ESfj")
mongoclient = pymongo.MongoClient("mongodb+srv://Test:Test@cluster0.fkr6war.mongodb.net/?retryWrites=true&w=majority")["PACAF"]
draftscoll = mongoclient["Drafts"]
historycoll = mongoclient["History"]
accountscoll = mongoclient["Accounts"]

@app.route("/api/get_drafts")
def drafts():
  account = accountscoll.find_one({"token": request.cookies.get("token")})
  if account != None:
    drafts = [{"error": "none"}]
    for draft in draftscoll.find({}, {"_id": 0}):
      if draft["owner"] == account["uid"]:
        drafts.append(draft)
    return jsonify(sorted(drafts, key=lambda e: e["createdAt"], reverse=True))
  else:
    return [{"error": "unauthorized"}]
               
@app.route("/api/get_history")
def history():
  return "Work in progress"

@app.route("/hashtest")
def hashtest():
  return '{"hash": "' + sha256_crypt.encrypt(request.args.get("password")) + '"}'

@app.route("/api/login", methods=["POST"])
def login():
  existing = accountscoll.find_one({"token": request.cookies.get("token")})
  if existing != None:
    return jsonify({"error": "loggedin"})
  else:
    account = accountscoll.find_one({"$or": [{"username": request.json.get("username")}, {"email": request.json.get("username")}]}) # Get account with corresponding username or email
    if account != None: # Make sure account was found and isn't None (MongoDB returns None if the query couldn't be found)
      if sha256_crypt.verify(request.json.get("password"), json.loads(account["password"])["hash"]): # Checks password given with password in database (will add hashing later)
        response = make_response(jsonify({"error": "none"}))
        response.set_cookie("token", account["token"], secure=True, httponly=True)
        return response
      else:
        return jsonify({"error": "invalid"})
    else:
      print("Couldnt find account")
      return jsonify({"error": "invalid"})
      
  encryped_password = '{"hash": "' + sha256_crypt.encrypt(password) + '"}'
  return "Work in progress"

@app.route("/api/archive")
def archive():
  return "Work in progress"


@app.route("/api/flight_details")
def flights():
  """
  -- Checks --
  Here, we check that the from, to, and date values are all correct.
  """
  if all([request.args.get("from"), request.args.get("to"), request.args.get("date")]):
    if len(request.args.get("from")) > 4:
      return jsonify({"success": False, "reason": "invalid_from"})
    if len(request.args.get("to")) > 4 or request.args.get("to") == request.args.get("from"):
      return jsonify({"success": False, "reason": "invalid_to"})
    try:
      date = datetime.datetime.strptime(request.args.get("date"), "%Y-%m-%d")
      if datetime.datetime.now() > date:
        return jsonify({"success": False, "reason": "invalid_date"})
    except:
      return jsonify({"success": False, "reason": "invalid_date"})
  else:
    return jsonify({"success": False, "reason": "missing_data"})
  """
  -- Getting Flights --
  This code will only execute if all the above checks passed.
  """
  try:
    offers = (
    client.offer_requests.create()
    .passengers([{"type": "adult"}])
    .slices([{"origin": request.args.get("from"), "destination": request.args.get("to"), "departure_date": request.args.get("date")}])
    .return_offers()
    .execute()).offers if request.args.get("round") != True else (
    client.offer_requests.create()
    .passengers([{"type": "adult"}])
    .slices([{"origin": request.args.get("from"), "destination": request.args.get("to"), "departure_date": request.args.get("date")}, {"origin": request.args.get("to"), "destination": request.args.get("from"), "departure_date": request.args.get("date")}])
    .return_offers()
    .execute()).offers
    flight = []
    for offer in offers: # Go through the offers and put them into a nicer clean list we can return
      flight.append({"id": offer.id, "airline": offer.owner.name, "departs": offer.slices[0].segments[0].departing_at, "cost": offer.total_amount, "currency": offer.total_currency})
    flight.sort(key=lambda e: e["cost"]) # Sort the flights by cost, from cheapest to highest
  except:
    return jsonify({"success": False, "reason": "unexpected_error"}) # Error Handling
  return jsonify({"success": True, "reason": "no_error", "flight": flight[0]}) # If everything was successful, return the result and the cheapest flight


# f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=5000&type=lodging&key={api_key}"
@app.route("/api/hotels")
def hotels():
  """
  -- Checks --
  Here, we check that the user provided a valid IATA code.
  """
  if request.args.get("code") != None:
    if len(request.args.get("code")) > 4:
      return jsonify({"success": False, "reason": "invalid_iata"})
  else:
    return jsonify({"success": False, "reason": "missing_data"})
  """
  -- Get Nearby Hotels --
  Now that we've confirmed the user provided a valid IATA code, we can now get nearby hotels.
  """
  # This is what needs to be done next.


# Serve the react routes
@app.route("/", defaults={"path": ""})
def react(path):
  return app.send_static_file("index.html")


app.run(host="0.0.0.0", port=8000)
