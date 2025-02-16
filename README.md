# Virtual Environment

```bash
python -m venv venv
activate
```

After that install modules.

```bash
pip install -r requirements.txt
```

# Setting

You need to set your .env by this following keys.

```env
SECRET_KEY
DATABASE_URL
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT
PGADMIN_DEFAULT_EMAIL
PGADMIN_DEFAULT_PASSWORD
API_URL
```

# Usage

This project is separate to two directories app/ standfor the frontend (customtkinter) and the server is for api endpoint connected to the database.

To use this you need to run the docker both services by this command.

```bash
# For the start the project the first time
docker compose up --build -d

# For stop the docker containers.
docker compose down -v
```

Then config your database inside the setting to the postgreSQL enter your database name, user, password.
