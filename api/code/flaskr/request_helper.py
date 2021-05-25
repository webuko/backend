from flask import abort


# this constant defines the default keys that are retrieved from the db
DEFAULT_RETURN_KEYS = [
    'id', 'name', 'description', 'price',
    'host_name', 'host_picture_url', 'picture_url',
    'bedrooms', 'bathrooms','bedrooms', 'accommodates',
    'property_type', 'room_type', 'neighbourhood',
    'longitude', 'latitude', 'city'
    ]


def filter_listings(request, force_GET=False):
    """ loads an encoder and then encodes the given value

    :param request: the request object sent by the user
    :type: flask.request
    :param force_GET: allows to retrieve default filter and projection keys in case of a POST request
    :type: boolean, optional

    :returns: a tuple containing the filter and projection keys used to retrieve data
    :rtype: tuple
    """

    if request.method == 'POST' and not force_GET:
        if not request.json.get('fields'):
            abort(400, 'fields parameter missing')

        if not isinstance(request.json['fields'], list):
            abort(400, 'Request data must be provided as array of keys')
        force_fields = False
        if request.json.get('force_fields'):
            if not isinstance(request.json['force_fields'], bool):
                abort(400, 'force_field parameter must be provided as bool')
            force_fields = request.json['force_fields']

        keys_projection = {str(key): 1 for key in request.json['fields']}
        keys_projection['_id'] = 0
        keys_filter = {}
        if force_fields:
            keys_filter = {str(key): {"$exists": 1} for key in request.json['fields']}
    else:
        keys_projection = {k: 1 for k in DEFAULT_RETURN_KEYS}
        keys_projection['_id'] = 0
        keys_filter = {}

    return keys_filter, keys_projection