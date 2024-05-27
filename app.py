# BEGIN CODE HERE
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT
# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])


@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE
    name_parameter = request.args.get("search-product")
    search_result = mongo.db.products.find({'product-name' : {'$regex': name_parameter, '$options': 'i'}})
    
    mylist=[]
    for product in search_result:
        product['_id'] = str(product['_id'])  #converts the id type to string in order to be able to jsonify the dict
        mylist.append(product)

    return jsonify(mylist)
    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    product_data = request.form.to_dict()
    
    existing_product = mongo.db.products.find_one({"product-name": product_data["product-name"]})
    if existing_product:
        mongo.db.products.update_one(
            {"product-name": product_data['product-name']},
            {"$set": {
                "product-price": product_data['product-price'],
                "product-year": product_data['product-year'],
                "product-color": product_data['product-color'],
                "product-size": product_data['product-size']
            }}
        )
    else:
        mongo.db.products.insert_one(product_data)

    return ""
    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE
    return ""
    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    return ""
    # END CODE HERE



app.run(debug=True)
