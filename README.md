# REST API
Basic catalog system to manage _products_:
- Non registered users can read data about the products.
- Admin users can create, read, update and delete products and users.

About the framework:
_FastAPI framework, high performance, easy to learn, fast to code, ready for production_
**Documentation**:  [](https://fastapi.tiangolo.com/)[https://fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
**Source Code**:  [](https://github.com/tiangolo/fastapi)[https://github.com/tiangolo/fastapi](https://github.com/tiangolo/fastapi)

## Special requirements
* Every time a **show product** is executed by whoever user the *times_requested* is incremented by one.
* When a user admin **update a product** all admins are notified by email.

## Database Diagram
![image](https://user-images.githubusercontent.com/21109597/123803978-67ab7400-d8b2-11eb-913e-c2eafa4d131b.png)

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
## Backend Requirements

*  [Docker](https://www.docker.com/).

## Backend local development

* Build the Docker image

`docker build -t catalog-api backend`

*  Run the Docker container

`docker run -d --name catalog-container -p 8000:8000 catalog-api`

* Now you can open your browser and interact with these URLs:

Backend, JSON based web API based on OpenAPI: http://localhost:8000/api/


## API docs

#### Automatic Interactive Docs (Swagger UI): **http://localhost:8000/docs**
![Screenshot_20210629_080127](https://user-images.githubusercontent.com/21109597/123801907-53ff0e00-d8b0-11eb-9bab-76b7939c5475.png)

#### Automatic Alternative Docs (ReDoc): http://localhost:8000/redoc

![image](https://user-images.githubusercontent.com/21109597/123802114-87da3380-d8b0-11eb-8e67-0d585b8e6d3a.png)

### Login as admin
* Execute  http://localhost:8000/docs#/Others/reset_reset_post to reset the app with default values.
![image](https://user-images.githubusercontent.com/21109597/123802514-02a34e80-d8b1-11eb-8ff0-ad1e0ff8f843.png)
* Login with default admin user
username:	username@example.com
password:	string
![image](https://user-images.githubusercontent.com/21109597/123802371-dab3eb00-d8b0-11eb-8d1b-f62483b78ced.png)
* Now you can create, update or delete users or products
![image](https://user-images.githubusercontent.com/21109597/123803734-287d2300-d8b2-11eb-90e6-453ad992266c.png)


