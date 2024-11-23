from flask import Blueprint, request, jsonify
from models import Listing, db

listings_bp = Blueprint('listings', __name__)

#get all listings or filter by criteria
@listings_bp.route('/', methods=['GET'])
def get_listings():
    filters = request.args
    query = Listing.query

    #apply filters
    if 'location' in filters:
        query = query.filter(Listing.location.ilike(f"%{filters['location']}%"))
    if 'price_min' in filters and 'price_max' in filters:
        query = query.filter(Listing.price.between(filters['price_min'], filters['price_max']))
    if 'distance_from_campus' in filters:
        query = query.filter(Listing.distance_from_campus <= filters['distance_from_campus'])

    listings = query.all()
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
    } for l in listings])

#add a new listing
@listings_bp.route('/', methods=['POST'])
def add_listing():
    data = request.get_json()
    listing = Listing(
        title=data['title'],
        location=data['location'],
        price=data['price'],
        duration=data['duration'],
        roommates=data.get('roommates'),
        amenities=data.get('amenities'),
        distance_from_campus=data.get('distance_from_campus'),
        contact_info=data['contact_info'],
    )
    db.session.add(listing)
    db.session.commit()
    return jsonify({'message': 'Listing created successfully!'}), 201

#delete a listing
@listings_bp.route('/<int:id>', methods=['DELETE'])
def delete_listing(id):
    listing = Listing.query.get_or_404(id)
    db.session.delete(listing)
    db.session.commit()
    return jsonify({'message': 'Listing deleted successfully!'})

#update a listing's status
@listings_bp.route('/<int:id>', methods=['PUT'])
def update_listing(id):
    data = request.get_json()
    listing = Listing.query.get_or_404(id)
    listing.status = data.get('status', listing.status)
    db.session.commit()
    return jsonify({'message': 'Listing updated successfully!'})