DeepSpeech REST API
===================

|Open| |versions|


.. |Open| image:: https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-speech.svg

This REST API is built on top of Mozilla's `DeepSpeech`_. It is written based on `examples`_  provided by Mozilla. It accepts HTTP methods such as GET and POST as well as WebSocket. To perform transcription using HTTP methods is
appropriate for relatively short audio files while the WebSocket can be used even for longer audio recordings.

.. _DeepSpeech: https://github.com/mozilla/DeepSpeech
.. _examples: https://github.com/mozilla/DeepSpeech-examples


Project setup
~~~~~~~~~~~~~

1. Clone the repository to your local machine and change directory to ``deepspeech-rest-api``

.. code-block:: console

    git clone https://github.com/fabricekwizera/deepspeech-rest-api.git
    cd deepspeech-rest-api


2. Create a virtual environment and activate it (assuming that it is installed your machine)
and install the project in editable mode (locally).

.. code-block:: console

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -U pip
    pip install --editable .


3. Download the model and the scorer. For English model and scorer, follow below links

.. code-block:: console

    wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm \
        -O deepspeech_model.pbmm
    wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer \
        -O deepspeech_model.scorer


For other languages, you can place the two files in the current working directory under the names ``deepspeech_model.pbmm`` for the
model and ``deepspeech_model.scorer`` for the scorer.

4. Migrations are done using `Alembic`_

.. _Alembic: https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment

5. Running the server

.. code-block:: console

    python3 run.py

Usage of the API
~~~~~~~~~~~~~~~~

Register a new user and request a new `JWT`_ token to access the API

.. _JWT: https://jwt.io/
.. code-block:: console

    curl -X POST \
    http://0.0.0.0:8000/users \
    -H 'Content-Type: application/json' \
    -d '{
    "username": "forrestgump",
    "email": "fgump@yourdomain.com",
    "password": "yourpassword"
    }'

API response

.. code-block:: json

    {
      "message": "User forrestgump is successfully created."
    }


To generate a JWT token to access the API

.. code-block:: console

    curl -X POST \
    http://0.0.0.0:8000/token \
    -H 'Content-Type: application/json' \
    -d '{
    "username": "forrestgump",
    "password": "yourpassword"
    }'


If both steps are done correctly, you should get a token in below format

.. code-block:: json

    {
        "access_token": "JWT_token",
        "refresh_token": "Refresh_token"
    }


With this ``JWT_token``, you have access to different endpoints of the API, and the ``Refresh_token`` is used to refresh the access token
when it expires.

To refresh a JWT token

.. code-block:: console

    curl -X POST \
    http://0.0.0.0:8000/token/refresh \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer JWT_token" \
    -d '{
        "refresh_token": "Refresh_token"
    }'



Performing STT (Speech-To-Text)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Change directory to ``audio`` and use the WAV files provided for testing.

- STT the HTTP way


.. code-block:: console

    cURL

    curl -X POST \
    http://0.0.0.0:8000/api/stt/http \
    -H 'Authorization: Bearer JWT_token' \
    -F 'audio=@8455-210777-0068.wav' \
    -F 'paris=-1000' \
    -F 'power=1000' \
    -F 'parents=-1000'


.. code-block:: python

    python

    import requests

    jwt_token = 'JWT_token'
    headers = {'Authorization': 'Bearer ' + jwt_token}
    hot_words = {'paris': -1000, 'power': 1000, 'parents': -1000}
    audio_filename = 'audio/8455-210777-0068.wav'
    audio = [('audio', open(audio_filename, 'rb'))]
    url = 'http://0.0.0.0:8000/api/stt/http'
    response = requests.post(url, data=hot_words, files=audio, headers=headers)
    print(response.json())


``Note the usage of hot-words and their boosts in the request.``

- STT the WebSocket way (simple test)

WebSockets don't support ``curl``. To take advantage of this feature, you will have to write a web app to send request to ``ws://0.0.0.0:8000/api/stt/ws``.

 
Below command can be used to check if the WebSocket is running.

.. code-block:: console

    python3 test_websocket.py

In the both cases (HTTP and WebSocket), you should get a result in below format.

.. code-block:: json

    {
      "message": "experience proves this",
      "time": 1.4718825020026998
    }
