
## 6.th Berlin TAC Tournament Website

29.th August in Berlin

### Installation

create a virtual python env

~~~bash
$ pip install virtualenv
$ cd some/directory
$ virtualenv venv/tac
~~~

get the code and install it into the venv

~~~bash
$ cd some/directory
$ git clone https://github.com/quiqua/tac-tournament-website.git
$ source venv/tac/bin/activate
$ pip install -e tacsite/.
~~~

### Starting the server locally

With an activated virtualenv:

~~~bash
$ cd some/directory/tacsite
$ python app.py
~~~

You may edit the config.py file and add a Mail Account for sending mails with
this application.

The server is now available at [localhost](http://127.0.0.1:5000).
