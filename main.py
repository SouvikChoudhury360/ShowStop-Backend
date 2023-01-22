from flask import Flask, make_response, jsonify, request
import dataset

app = Flask(__name__)
db = dataset.connect('sqlite:///venues.db')

table = db['venues']

def fetch_db(venue_id):
    return table.find_one(venue_id=venue_id)


def fetch_db_all():
    venues = []
    for venue in table:
        venues.append(venue)
    return venues


@app.route('/api/venues', methods=['GET', 'POST'])
def api_venues():
    if request.method == "GET":
        return make_response(jsonify(fetch_db_all()), 200)
    elif request.method == 'POST':
        content = request.json
        venue_id = content['venue_id']
        table.insert(content)
        return make_response(jsonify(fetch_db(venue_id)), 201)

@app.route('/api/venues/<venue_id>', methods=['GET', 'PUT', 'DELETE'])
def api_individual_venue(venue_id):
    if request.method == "GET":
        return make_response(jsonify(fetch_db(venue_id)))
    elif request.method == "PUT":
        content = request.json
        table.update(content, ['venue_id'])
        book_obj = fetch_db(venue_id)
        return make_response(jsonify(book_obj), 200)
    elif request.method == "DELETE":
        table.delete(id=venue_id)
        return make_response(jsonify({}), 204)


if __name__ == '__main__':
    app.run(debug=True)