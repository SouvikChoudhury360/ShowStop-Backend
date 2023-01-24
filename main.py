from flask import Flask, make_response, jsonify, request
import dataset

app = Flask(__name__)
db = dataset.connect('sqlite:///db1.db')

table = db['venues']
user_table = db['users']
shows_table = db['shows']
bookings_table = db['bookings']
ratings_table = db['ratings']

@app.route('/api/ratings', methods=['GET', 'POST'])
def ratings_api():
    if request.method == "GET":
        ratings = []
        for rating in ratings_table:
            ratings.append(rating)
        return make_response(jsonify(ratings), 200)
    elif request.method == "POST":
        content = request.json
        ratings_table.insert(content)
        return make_response(jsonify(content), 201)

@app.route('/api/ratings/show/<show_id>', methods=['GET'])
def rating_from_user(show_id):
    if request.method == "GET":
        ratings = []
        selected_ratings = db.query("SELECT * FROM ratings WHERE show_id = " + str(show_id) + ";")
        for rating in selected_ratings:
            ratings.append(rating)
        return make_response(jsonify(ratings))

@app.route('/api/ratings/user/<user_id>', methods=['GET'])
def rating_from_show(user_id):
    if request.method == "GET":
        ratings = []
        selected_ratings = db.query("SELECT * FROM ratings WHERE user_id = " + str(user_id) + ";")
        for rating in selected_ratings:
            ratings.append(rating)
        return make_response(jsonify(ratings))

@app.route('/api/ratings/<rating_id>', methods=['GET', 'PUT', 'DELETE'])
def api_individual_ratings(rating_id):
    if request.method == "GET":
        return make_response(jsonify(ratings_table.find_one(id=rating_id)))
    elif request.method == "PUT":
        content = request.json
        ratings_table.update(content, ['id'])
        ratings_obj = ratings_table.find_one(id=rating_id)
        return make_response(jsonify(ratings_obj), 200)
    elif request.method == "DELETE":
        ratings_table.delete(id=rating_id)
        return make_response(jsonify({}), 204)

@app.route('/api/bookings', methods=['GET', 'POST'])
def booking_api():
    if request.method == "GET":
        bookings = []
        for booking in bookings_table:
            bookings.append(booking)
        return make_response(jsonify(bookings))
    elif request.method == "POST":
        content = request.json
        bookings_table.insert(content)
        return make_response(jsonify(content), 201)

@app.route('/api/bookings/show/<show_id>', methods=['GET'])
def get_booking_by_show_id(show_id):
    if request.method == "GET":
        bookings = []
        selected_bookings = db.query("SELECT * FROM bookings WHERE show_id = " + str(show_id) + ";")
        for booking in selected_bookings:
            bookings.append(booking)
        return make_response(jsonify(bookings), 200)

@app.route('/api/bookings/user/<user_id>', methods=['GET'])
def get_booking_by_user_id(user_id):
    if request.method == "GET":
        bookings = []
        selected_bookings = db.query("SELECT * FROM bookings WHERE user_id = " + str(user_id) + ";")
        for booking in selected_bookings:
            bookings.append(booking)
        return make_response(jsonify(bookings), 200)

@app.route('/api/shows', methods=['GET', 'POST'])
def api_shows():
    if request.method == "GET":
        shows = []
        for show in shows_table:
            shows.append(show)
        return make_response(jsonify(shows))
    elif request.method == "POST":
        content = request.json
        content["booking_count"] = 0
        content["rating_count"] = 0
        selected_venue = db.query("SELECT * FROM venues WHERE id = " + str(content["venue_id"]) + ";")
        selected_capacity = 0
        for venue in selected_venue:
            selected_capacity = venue["capacity"]
        content["capacity_left"] = selected_capacity
        shows_table.insert(content)
        return make_response(jsonify(content), 201)

@app.route('/api/shows/<show_id>', methods=['GET', 'PUT', 'DELETE'])
def api_individual_shows(show_id):
    if request.method == "GET":
        return make_response(jsonify(shows_table.find_one(id=show_id)))
    elif request.method == "PUT":
        content = request.json
        shows_table.update(content, ['id'])
        show_obj = shows_table.find_one(id=show_id)
        return make_response(jsonify(show_obj), 200)
    elif request.method == "DELETE":
        shows_table.delete(id=show_id)
        return make_response(jsonify({}), 204)

@app.route('/api/venues', methods=['GET', 'POST'])
def api_venues():
    if request.method == "GET":
        venues = []
        for venue in table:
            venues.append(venue)
        return make_response(jsonify(venues), 200)
    elif request.method == 'POST':
        content = request.json
        table.insert(content)
        return make_response(jsonify(content), 201)

@app.route('/api/venues/<venue_id>', methods=['GET', 'PUT', 'DELETE'])
def api_individual_venue(venue_id):
    if request.method == "GET":
        return make_response(jsonify(table.find_one(id=venue_id)))
    elif request.method == "PUT":
        content = request.json
        table.update(content, ['id'])
        venue_obj = table.find_one(id=venue_id)
        return make_response(jsonify(venue_obj), 200)
    elif request.method == "DELETE":
        table.delete(id=venue_id)
        return make_response(jsonify({}), 204)

@app.route('/api/city/<city>', methods=['GET'])
def api_venue_by_city(city):
    if request.method == "GET":
        venue_city = []
        venues= db.query("SELECT * FROM venues WHERE city = '" + city + "';")
        # print(venues)
        for venue in venues:
            venue_city.append(venue)
        return make_response(jsonify(venue_city))

@app.route('/api/users', methods=['GET', 'POST'])
def api_user():
    if request.method == "GET":
        users = []
        for user in user_table:
            users.append(user)
        return make_response(jsonify(users), 200)
    elif request.method == "POST":
        content = request.json
        user_table.insert(content)
        return make_response(jsonify(content), 201)

@app.route('/api/users/<user_id>', methods=['GET', 'PUT'])
def api_individual_user(user_id):
    if request.method == "GET":
        return make_response(jsonify(user_table.find_one(id=user_id)))
    elif request.method == "PUT":
        content = request.json
        user_table.update(content, ['id'])
        user_obj = user_table.find_one(id=user_id)
        return make_response(jsonify(user_obj), 200)

if __name__ == '__main__':
    app.run(debug=True)