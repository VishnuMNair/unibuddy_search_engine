import http
import json

from flask import Flask, request, jsonify
import requests

from SearchUtility.search_engine import SearchEngine

server = Flask(__name__)
book_url = 'https://ie4djxzt8j.execute-api.eu-west-1.amazonaws.com/coding'

engine: SearchEngine


def fetch_author(id):
    """
    fetch author name from microservice
    :param id: book id
    :return: author name if found
    """
    data = {'book_id': int(id)}
    response = requests.post(url=book_url, json=data)
    if response.status_code == 200:
        return response.json()['author']
    else:
        return 'No Author'


@server.route('/SearchBook', methods=['GET', 'POST'])
def search_for_book():
    """
    search for book endpoint
    :return: list of books
    """
    req = request.get_json()
    try:
        ret = []
        queries = req['queries']
        max_items = req['K']
        for val in queries:
            result = engine.search_for(val, max_items)
            output = json.loads(result)
            book_list = []
            for key, value in output.items():
                author = fetch_author(value)
                obj = {'summary': key, 'id': value, 'query': val, 'author': author}
                book_list.append(obj)
            ret.append(book_list)

        return jsonify(ret)

    except Exception as e:
        return jsonify({'status_code': http.HTTPStatus.INTERNAL_SERVER_ERROR, 'message': str(e)})


if __name__ == '__main__':
    engine = SearchEngine()
    server.run(host='0.0.0.0', port=5000, debug=True)
