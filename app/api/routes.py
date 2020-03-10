from time import strftime

from flask import jsonify, request, current_app

from app.api import bp
from app.api.errors import error_response
from app.gios_api import GiosService


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


@current_app.after_request
def after_request(response):
    current_app.logger.info('%s %s %s %s %s', request.remote_addr, request.method, request.scheme, request.full_path,
                            response.status)
    return response
