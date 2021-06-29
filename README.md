# REST API
_FastAPI framework, high performance, easy to learn, fast to code, ready for production_
**Documentation**:  [](https://fastapi.tiangolo.com/)[https://fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
**Source Code**:  [](https://github.com/tiangolo/fastapi)[https://github.com/tiangolo/fastapi](https://github.com/tiangolo/fastapi)

# Project Structure

```
.
├── app              	 	# root of the API project
│   ├── catalog.db       	# project database
│   ├── main.py          	# "main" module, e.g. import app.main
│   ├── requirements.py  	# necessary packages
│   └── app  	         	# "app" is a "Python subpackage"
│   	├── __init__.py  	# makes "routers" a "Python subpackage"
│   	├── database.py     # Connection and config to database related
│		├──	hashing.py		# Encrypt and validate passwords
│		├──	models.py		# Models with their relations
│		├──	oauth2			# Authorization by token
│		├── token			# JWT tokens implementation
│		├── controllers		# To separate logic from endpoint
│		│	├── __init__.py # makes "controllers" a "Python subpackage"
│		│	├── ..
│		│	├── ..
│		│	└── auth.py		# Login function
│		├── routers			# points of entry organized by prefix
│		│	├── __init__.py # makes "routers" a "Python subpackage"
│		│	├── users.py
│		│	├── products.py
│   	│	└── analytics.py
│   	└── schemas         # Pydantic schemas
│       	├── __init__.py # makes "schemas" a "Python subpackage"
│			├── users.py
│			├── products.py
│       	└── analytics.py

```




## Start the app

### Build the Docker image
`docker build -t catalog-api backend`
### Build the Docker image
`docker run -d --name catalog-container -p 8000:8000 catalog-api`


## API docs
Documentation  (read only)
http://127.0.0.1:8000/redoc

You will see the interactive API documentation (API client included)
http://127.0.0.1:8000/docs