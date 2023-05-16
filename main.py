import pymongo
import datetime
from duffel_api import Duffel
from flask import Flask, jsonify, request


app = Flask(__name__, static_folder="fe/fe/build", static_url_path="")
client = Duffel(access_token = "duffel_test_wR7qOeLxoMTMziq7CGRJcKR6as2tvwQnuMoVVR0ESfj")
mongoclient = pymongo.MongoClient("mongodb+srv://pacafroot:1234@pacafdb.s5eitfs.mongodb.net/?retryWrites=true&w=majority")


@app.route("/api/flight_details")
def flights():
  """
  -- Checks --
  Here, we check that the from, to, and date values are all correct.
  """
  if request.args.get("from") != None and request.args.get("to") != None and request.args.get("date") != None:
    if len(request.args.get("from")) > 4:
      return jsonify({"success": False, "reason": "invalid_from"})
    if len(request.args.get("to")) > 4:
      return jsonify({"success": False, "reason": "invalid_to"})
    if request.args.get("from") == request.args.get("to"):
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
    .execute()).offers # Get the offers from the duffle API
    flight = []
    for offer in offers: # Go through the offers and put them into a nicer clean list we can return
      flight.append({"id": offer.id, "airline": offer.owner.name, "departs": offer.slices[0].segments[0].departing_at, "cost": offer.total_amount, "currency": offer.total_currency})
    flight.sort(key=lambda e: e["cost"]) # Sort the flights by cost, from cheapest to highest
  except Exception as e:
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
