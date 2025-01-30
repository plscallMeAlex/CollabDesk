# Steps

Make the venv and go inside venv first.

```bash
python -m venv venv
activate
```

After that install modules.

```bash
pip install -r requirements.txt
```

You need to initialize the Django configuration and setting first with the command as follows

```bash
cd server
python manage.py startapp server
```

Then config your database inside the setting to the postgreSQL enter your database name, user, password.
