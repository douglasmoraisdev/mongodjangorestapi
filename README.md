# mongodjangorestapi: A Mongo+Django REST API
A rest api to manage a users/group/meetings system, powered by Django and MongoDB, using OAuth2  for autentication and autorization.

# 1. Installing dependencies

```sh
$ pip install -r docs/requirements.txt
```

# 3. Configuration

```sh
$ vim apps/mysite/settings.py
```
add:
```
ALLOWED_HOSTS = ['your-domain-name-or-localhost.com:port']
```

# 2. Running a local server

```sh
$ cd apps/
$ python3 manage.py runserver
```

# 3. Done!