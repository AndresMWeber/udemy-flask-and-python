from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]
    }
]


@app.route("/")  # 'http://google.com/' is google.com '/' aka root/homepage, actual method name does not matter.
def home():
    return render_template('index.html')


# POST - used to receive data
# GET - used to send data back only

# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


# GET/ /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    # Iterate over stores
    # If the store name matches, return it
    # If none match, return an error message
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'Error, could not locate store resource %s' % name})


# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            store['items'].append(request_data)
            return jsonify(store['items'][-1])
    return jsonify({'message': 'Error, could not locate store resource %s' % name})


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'Error, could not locate store resource %s' % name})


app.run(port=5000)
