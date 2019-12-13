# Fangler

Fangler is a Flask-based Python application that exposes an API for users to defang and refang URLs.
The schema for this is custom and may be modified freely. 

WARNING: As this is proof-of-concept/testing code I do not recommended deploying this as-is.

### Prerequisites

This application is designed to run with Python 3.7+

To install all prerequisite Python packages in your virtual environment please run the following:
```
pip install -r requirements.txt
```

## Getting Started

After installing prerequisites and making sure all tests pass you can execute the following to get a test server running:
```
$ export FLASK_APP=fangler.py
$ flask run
 * Running on http://127.0.0.1:5000/
```

### Endpoints
There are two API endpoints: ```/defang``` and ```/refang```. 

Both of these expect a POST request with a JSON blob 
in the format 
```{"data": "URL"}``` 

or 

```{"data": ["URL", "URL", "URL", ...]}```

### Endpoint curl Examples

```
$ curl -d '{"data": "https://www.example.com"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/defang
{"response": "hxxps:$$www[dot]example[dot]com"}

$ curl -d '{"data": "hxxps:$$www[dot]example[dot]com"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/refang
{"response": "https://www.example.com"}
```

There's also a stress test file that contains 500 complex HTTP/HTTPS URLs (WARNING: These are phishing urls!!!).
```
$ curl -d '@sample_requests/stresstest_defang.json' -H "Content-Type: application/json" -X POST http://localhost:5000/api/defang
{"response": ...[wall of text :)

$ curl -d '@sample_requests/stresstest_refang.json' -H "Content-Type: application/json" -X POST http://localhost:5000/api/refang
{"response": ...[wall of text :)

```

## Tests

To run the test suite execute the following:
```
python test_fangler.py -v
```

There are some Postman and HAR formatted example requests in the sample_requests folder. These cover the core 
functionality of the app and should import into Postman and most browser-based request editors.
[Learn more about HAR here](http://www.softwareishard.com/blog/har-adopters/).


## Design Documentation

The project design document can be found [here](https://docs.google.com/document/d/1k_0lx9Aak_pojCCY_KWCQA9KEH5Mgtd1YWyumwVKW1g/edit?usp=sharing)

## Authors

* **Ryan Weaver**
