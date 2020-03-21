from flask import jsonify, request, current_app
from marshmallow import ValidationError

from app import db
from app.api import bp
from app.api.errors import error_response, bad_request
from app.api.schemas import subscription_schema
from app.gios_api import GiosService
from app.models import Subscription


@bp.route('/', methods=['GET'])
def connection():
    return jsonify({'message': 'API is online!'}), 200


@bp.route('/air-data', methods=['GET'])
def get_air_data():
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)
    if not lat or not lon:
        return error_response(422, 'Lack required parameters (lat, lon).')
    else:
        return jsonify(GiosService.get_nearest_station_data(lat, lon)), 200


@bp.route('/register', methods=['POST'])
def register():
    """
    {
        "email": "sample@test.pl",
        "lat": 51.1234,
        "lon": 21.0101,
        "hours": [12, 14, 20]
    }
    """
    json_data = request.get_json()
    if not json_data:
        return bad_request('No input data provided')
    try:
        data = subscription_schema.load(json_data)
    except ValidationError as e:
        return jsonify(e.messages), 422
    else:
        current_app.logger.info('Subscription data: %s' % data)

        # sprawdzić czy email już istnieje
        old_sub = Subscription.query.filter_by(email=data.get('email')).first()
        if old_sub is not None:
            current_app.logger.info("Email taken")
            return error_response(422, "Email '%s' already registered!" % data.get('email'))

        # Usunięcie duplikatów godzin
        hours = set(data.pop('hours'))

        sub = Subscription(**data)
        for h in hours:  # TODO: lambda?
            sub.add_hour(h)
        db.session.add(sub)
        db.session.commit()
        current_app.logger.info("Subscription saved")
        return jsonify({'message': 'Subscription saved!'}), 200


@bp.route('/subscription', methods=['PUT', 'DELETE'])
def manage_subscription():
    return error_response(501)


@current_app.after_request
def after_request(response):
    current_app.logger.info('%s %s %s %s %s', request.remote_addr, request.method, request.scheme, request.full_path,
                            response.status)
    return response
