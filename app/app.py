from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myDB'

mongo = PyMongo(app)




@app.route('/', methods=['GET'])
def index():

    # Get current collection and all collections in MongoDB
    active_collection = session.get('collection_name', 'myCollection')
    all_collections = mongo.db.collection_names()

    # Get data in current collection
    mongo_connection = mongo.db[active_collection]
    data = list(mongo_connection.find())
    # print(data)

    return render_template('index.html', active_collection=active_collection, all_collections=all_collections,
                           data=data)


@app.route('/add_data', methods=['POST'])
def add_data():
    """Add data to MongoDB"""

    # Build new document to be inserted
    new_document = {
        'name': request.form['name'],
        'age': int(request.form['age']),
        'location': request.form['location']
    }

    # Connect to MongoDB
    mongo_connection = mongo.db[request.form['collection']]
    insert = mongo_connection.insert_one(new_document)

    # Feedback
    if insert.acknowledged:
        flash('{} added to collection {}'.format(request.form['name'], request.form['collection']))
    else:
        flash('Something went wrong.')

    return redirect(url_for('index'))


@app.route('/delete_data/<id>', methods=['GET', 'POST'])
def delete_data(id):
    """Delete data from MongoDB"""

    # Connect to MongoDB
    mongo_connection = mongo.db[session.get('collection_name', 'myCollection')]

    # Delete data by document unique ObjectID
    delete = mongo_connection.delete_one({'_id': ObjectId(id)})

    # Feedback
    if delete.acknowledged:
        flash('{} deleted from collection {}'.format(id, session.get('collection_name', 'myCollection')))
    else:
        flash('Something went wrong.')

    return redirect(url_for('index'))



@app.route('/change_collection', methods=['POST'])
def change_collection():
    """Change MongoDB collection being read"""

    # Update collection in session object
    session['collection_name'] = request.form['collection_name']

    # Feedback
    flash('MongoDB collection changed to {}'.format(session['collection_name']))

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)



