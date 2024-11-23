from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sublease.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    roommates = db.Column(db.Integer)
    amenities = db.Column(db.String(200))
    distance_from_campus = db.Column(db.Float)
    contact_info = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

@app.route('/listings', methods=['GET'])
def get_listings():
    listings = Listing.query.all()
    return jsonify([{
        'id': l.id,
        'title': l.title,
        'location': l.location,
        'price': l.price,
        'duration': l.duration,
        'roommates': l.roommates,
        'amenities': l.amenities,
        'distance_from_campus': l.distance_from_campus,
        'contact_info': l.contact_info,
        'status': l.status,
        'created_at': l.created_at,
    } for l in listings])

@app.route('/listings', methods=['POST'])
def add_listing():
    data = request.get_json()
    listing = Listing(
        id=data.get('id'),
        title=data['title'],
        location=data['location'],
        price=data['price'],
        duration=data['duration'],
        roommates=data.get('roommates'),
        amenities=data.get('amenities'),
        distance_from_campus=data.get('distance_from_campus'),
        contact_info=data['contact_info'],
        status=data.get('status', 'active'),
        created_at=data.get('created_at'),
    )
    db.session.add(listing)
    db.session.commit()
    return jsonify({'message': 'Listing created successfully!'}), 201

@app.route('/listings/<int:id>', methods=['DELETE'])
def delete_listing(id):
    listing = Listing.query.get_or_404(id)
    db.session.delete(listing)
    db.session.commit()
    return jsonify({'message': 'Listing deleted successfully!'})

@app.route('/listings/<int:id>', methods=['PUT'])
def update_listing(id):
    data = request.get_json()
    listing = Listing.query.get_or_404(id)
    listing.id = data.get('id', listing.id)
    listing.title = data.get('title', listing.title)
    listing.location = data.get('location', listing.location)
    listing.price = data.get('price', listing.price)
    listing.duration = data.get('duration', listing.duration)
    listing.roommates = data.get('roommates', listing.roommates)
    listing.amenities = data.get('amenities', listing.amenities)
    listing.distance_from_campus = data.get('distance_from_campus', listing.distance_from_campus)
    listing.contact_info = data.get('contact_info', listing.contact_info)
    listing.status = data.get('status', listing.status)
    listing.created_at = data.get('created_at', listing.created_at)
    db.session.commit()
    return jsonify({'message': 'Listing updated successfully!'})

if __name__ == '__main__':
    app.run(debug=True)