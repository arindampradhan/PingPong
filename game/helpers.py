import json
import pandas
import csv
import json
from functools import wraps


def CustomParser(data):
    j1 = json.loads(data)
    return j1

def csv_to_json(csv_filename):
    try:
        reader = csv.DictReader(open(csv_filename, 'r'))
        dict_list = []
        for line in reader:
            dict_list.append(line)
        print(dict_list)
        return dict_list
    except Exception as e:
        return {'error': str(e)}

#
# def validate_api(f):
#     """Validate apis for different cases."""
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if str(request.headers.get('api_key')) != str(session.get('api_key')):
#             # print(request.headers.get('api_key'))
#             # print(session.get('api_key'))
#             return make_response(jsonify({'error': 'Invalid api_key', 'status': 400}), 400)
#         request_count = session.get('request_count')
#         if request_count is None:
#             session['request_count'] = 0
#         else:
#             session['request_count'] += 1
#         if session.get('username') is None:
#             return make_response(jsonify({'error': 'Invalid User', 'status': 503}), 503)
#         return f(*args, **kwargs)
#     return decorated_function