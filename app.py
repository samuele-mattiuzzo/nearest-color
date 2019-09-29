import requests
from io import BytesIO
from flask import Flask, Response, abort, request, json, jsonify

from cruncher import cruncher


api = Flask(__name__)


def _get_from_url(img_url):
    response = requests.get(img_url)
    im_bytes = BytesIO(response.content)
    return im_bytes


@api.route('/nearest', methods=['POST'])
def nearest():
    """API endpoint to find the nearest color matched by the images

    :return: status code 405 - invalid JSON or invalid request type
    :return: status code 400 - unsupported Content-Type
    :return: status code 201 - success
    """
    # Ensure post's Content-Type is supported
    if request.json:
        # Ensure data is a valid JSON
        try:
            data = request.get_json()
        except ValueError:
            return Response(status=405)

        # TODO: optimise
        img = data.get('image')
        if 'http' in img:
            img = _get_from_url(img)

        nearest_color = cruncher(img)

        if nearest_color:
            res = nearest_color
        else:
            res = 'No color found'
        return jsonify(color=res), 200
    # User submitted an unsupported Content-Type
    else:
        return Response(status=400)


if __name__ == '__main__':
    api.run(debug=True)