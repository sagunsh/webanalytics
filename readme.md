## Py Analytics

A minimal web analytics project written using Python and FastAPI.

### .env setup

    $ cp .env.example .env

Make necessary changes to .env file

### Install Requirements

    $ pip install -r requirements

### Create Database

**Note: Running this will remove existing sqlite file along with all data and create new file**

    $ python init_db.py

### Run locally

Start the analytics server

    $ fastapi dev app.py --port=5000

Register your client

    $ curl --header "Content-Type: application/json" -X POST -d '{"client_id": "AA100", "domain": "127.0.0.1:3000"}' http://127.0.0.1:5000/add

You will see a output like this:

    {"success":true,"msg":"Added client AA100 - 127.0.0.1:3000"}

Start the test server

    $ cd test
    $ python server.py

Then, visit http://127.0.0.1:3000/ to send events to analytics server

Now, goto http://127.0.0.1:5000/client/AA100 to see results.