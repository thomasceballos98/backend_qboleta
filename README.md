Update prisma:
1) `prisma db pull`
2) `prisma generate`

Steps for running the backend:
0) On EC2 instance, delete the api using `rm -r qboleta_backend`
0.1) Upload the .zip (NOT SURE: not include "env" and "node_modules" directories in this .zip)
0.2) Unzip the .zip with `unzip <zip_name>.zip`
0.3) Kill the process on port 5050/tcp with `fuser -k 5050/tcp`
1) Go to the folder qboleta-backend
2) Create a virtual environment (recommend `virtualenv env`)
2.1) For EC2 instance: `python3 -m venv venv`
3) Activate the virtual environment with `source venv/Scripts/activate`
3.1) For EC2 instance: `source venv/bin/activate`
4) Install the requirements with `pip install -r requirements.txt`
5) Install gunicorn with `pip install gunicorn`
6) Run `mkdir .log`
7) Run `prisma db pull`
8) Run `prisma generate`
9) Run the code using: `gunicorn -b 0.0.0.0:5050 app:app --access-logfile .log/access.log --error-logfile .log/general.log`

Note: For EC2 instance, edit config.py, app.py and .env as 
    *For app.py: app.run(host='0.0.0.0')
    *For config.py: SERVER_NAME = None
    *For .env: DATABASE_URL="mysql://<user>:<password>@localhost:3306/qboleta_dev"


Documentación Prisma Python: https://prisma-client-py.readthedocs.io/en/stable/reference/operations/