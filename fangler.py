from flask import Flask, jsonify, request, abort
from flask_restful import Api, Resource, reqparse
import urllib.parse


app = Flask(__name__)
api = Api(app, prefix='/api')

# TODO: Maybe move the maps to config files.
# TODO: Custom error messages (See http://flask.pocoo.org/docs/1.0/patterns/errorpages/ )
# TODO: Look into making defang and refang a single flip/flop style operation? Currently not very DRY.
# TODO: Break out replacement strings into a data structure for more resilient processing.

""" 
The protocol map is designed to be an extensible list of valid protocols used by multiple functions.
Check https://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml before adding more
"""
protocol_map = {
    'http': 'hxxp',
    'https': 'hxxps',
    'ftp': 'fxp',
    'sftp': 'sfxp',
    'smtp': 'smxp',
    'bitcoin': 'bitcxxn',
    'magnet': 'magnxt',
}
valid_defang_protocols = list(protocol_map)
valid_refang_protocols = list(protocol_map.values())

replacement_map = {
    ".": "[dot]",
    "/": "$"
}
defang_replacements = list(replacement_map)
refang_replacements = list(replacement_map.values())


def validate(url, refang=False):
    """
    The validate function currently just checks if the URL matches the known protocol list. Additional validations
    should be added here as discovered. There are more validations to do on the refang side of things, for sure.

    Parameters:
        url (string): A URL.
        refang (boolean): Triggers a logic change for validating URLs in need of a refang.

    Returns:
        boolean
    """
    # TODO: Examine url = w3lib.url.canonicalize_url(url) as an option.

    if refang:
        url = url.replace('.', '[dot]')
        url = url.replace('/', r'$')
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.scheme in valid_refang_protocols:
            return True
        else:
            return False
    else:
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.scheme in valid_defang_protocols:
            return True
        else:
            return False


def defang(url):
    """
    The defang function first parses the URL provided, then defangs the protocol segment before re-assembling.
    The next and final operation is a series of string.replace() calls to further defang the URL.

    Parameters:
        url (string): A URL.

    Returns:
        string:url - A defanged URL
    """
    # Parsing the URL to examine and change the protocol segment
    url = urllib.parse.urlparse(url)
    if url.scheme in valid_defang_protocols:
        url = url._replace(scheme=protocol_map[url.scheme])
    url = urllib.parse.urlunparse(url)

    # Making regular text replacements
    for entry in defang_replacements:
        url = url.replace(entry, replacement_map[entry])

    return url


def refang(url):
    """
    The refang function operates mirror to defang, and as such first runs replacement operations. It then parses the
    URL provided and refangs the protocol segment before re-assembling.

    Parameters:
        url (string): A URL.

    Returns:
        string:url - A refanged URL
    """

    # Making regular text replacements
    for entry in refang_replacements:
        # This is a little convoluted but it's just grabbing the dict entry based on value instead of key.
        url = url.replace(entry, list(replacement_map.keys())[list(replacement_map.values()).index(entry)])

    # Parsing the URL to examine and change the protocol segment
    url = urllib.parse.urlparse(url)
    if url.scheme in valid_refang_protocols:
        url = url._replace(scheme=list(protocol_map.keys())[list(protocol_map.values()).index(url.scheme)])
    url = urllib.parse.urlunparse(url)

    return url



class DefangResource(Resource):
    def post(self):
        """
        This is the /defang endpoint logic. Here it's simply checking to see if it's a single request or a list.
        It then runs validate() against each URL and, if there are no errors, returns the defanged URLs.

        Returns:
            Either a JSON object containing defanged URLs or an HTTP error.
        """
        json_data = request.get_json(force=True)
        data = json_data['data']

        if type(data) is list:
            urls = []
            for url in data:
                if validate(url):
                    urls.append(defang(url))
                else:
                    abort(400)
            return {'response': urls}
        else:
            if validate(data):
                return {'response': defang(data)}
            else:
                abort(400)


class RefangResource(Resource):
    def post(self):
        """
        This is the /refang endpoint logic. Here it's simply checking to see if it's a single request or a list.
        It then runs validate() against each URL and, if there are no errors, returns the refanged URLs.

        Returns:
            Either a JSON object containing refanged URLs or an HTTP error.
        """
        json_data = request.get_json()
        # TODO: Fail on list with invalid JSON (improper quotes).
        data = json_data['data']  # Maybe ast.literal? Seems dangerous
        if type(data) is list:
            urls = []
            for url in data:
                if validate(url, refang=True):
                    urls.append(refang(url))
                else:
                    abort(400)
            return {'response': urls}
        else:
            if validate(data, refang=True):
                return {'response': refang(data)}
            else:
                abort(400)


api.add_resource(DefangResource, '/defang')
api.add_resource(RefangResource, '/refang')

app.run()
