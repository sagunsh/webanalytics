## Py Analytics

A minimal web analytics project written using Python and FastAPI.

### .env setup

    $ cp .env.example .env

Make necessary changes to .env file

### Virtual Environment [Option but recommended]

    $ sudo pip3 install virtualenv
    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $

`(venv)` verifies that virtual environment has been activated

### Install Requirements

    (venv) $ pip install -r requirements.txt

### Create Database

**Note: Running this will remove existing sqlite file along with all data and create new file**

    (venv) $ python db_init.py

### Run locally

Start the analytics server

    (venv) $ fastapi dev app.py --port=5000

In another terminal window, register your client

    (venv) $ curl --header "Content-Type: application/json" -X POST -d '{"client_id": "AA100", "domain": "127.0.0.1:3000"}' http://127.0.0.1:5000/add

You will see a output like this:

    {"success":true,"msg":"Added client AA100 - 127.0.0.1:3000"}

Start the test server

    (venv) $ cd test
    (venv) $ python server.py

Then, visit http://127.0.0.1:3000/ to send events to analytics server

Now, goto http://127.0.0.1:5000/client/AA100 to see results.

### Deployment

For deployment, follow this
document https://docs.vultr.com/how-to-deploy-fastapi-applications-with-gunicorn-and-nginx-on-ubuntu-20-04

### Add Tracking Script

Once deployed, you can add the following snippet in the head section of all the pages in that domain name you wish to
track.

    <script defer src="https://<analytics.test>/static/script.js" data-code="<code>"></script>

Replace `<analytics.test>` with your domain name where you hosted this analytics app and `<code>` with the respective code for the domain where this script tag is being added.
