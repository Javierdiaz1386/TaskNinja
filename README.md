# **Task Ninja API**
Task Ninja API is a very simple web service with which you can create a user and save your tasks there, you can create, delete, modify and view your tasks.

# How To Use
It is deployed in a free host so the response speed is affected, to use it you must make the different requests to the following url.

___
## **Python**
To make HTTP requests in Python, we will use the "requests" library this time. As an example, we will use the endpoint with which we can create our user in the Task Ninja API.

First, we must install the aforementioned library "[requests](https://pypi.org/project/requests/)". To do this, we will use the Python package manager called "PIP".

```shell
pip install requests
```

As we already have the necessary library installed, we will begin with the code.

In this case, we will make a request to the API at its endpoint "/user/create/", which only accepts the POST method since it is for creating our user in the Task Ninja API.

```py
import requests

url = 'https://taskninja.onrender.com/user/create'

data = {"username": str,
        "password": str.
        "full_name": str,
        "email": str,
        "disable": bool
}

res = requests.post(url, data=data)
```
___

## **JavaScript**

In the following example, we will make a request to the endpoint "/user/create" from the Javascript programming language. We will use one of its packages called "axios", which allows us to make HTTP requests to URLs.

To install, we must run the following command in our terminal:

```shell
npm install axios
```
Once installed, we will proceed to make a request to the Task Ninja API to create our user:

```js
const axios = require('axios');

let data = {
  username: 'JDoe',
  full_name: "John Doe"
  email: 'johndoe@example.com',
  password: 'mypassword',
  disable: true
};

axios.post('https://taskninja.onrender.com/user/create', data)
  .then((response) => {
    console.log(response.data);
  })
  .catch((error) => {
    console.log(error.response.data);
  });

```

# **EndPoints**

This API has several endpoints, each of which will help us create a fast and easy task application.

### **Endpoints for user management:**

Since it's a simple task API, it does not have an extensive user management system. However, it provides the basic endpoints needed for creating, retrieving, updating, and deleting user accounts.

* [POST /user/create: Creates a new user.](#createuser)

* POST /user/login: Login the users.

* GET /user/me: Returns information about the authenticated user.

____
## **Create User<a name="createuser"></a>**
`EndPoint /user/create`

Regarding the Task Ninja API, the endpoint to create a user is indeed "/user/create", and it receives the following data in the request body:

#### **Fields:**

* `full_name`: represents the full name of the user.

* `username`: A string representing the username.

* `email`: A string representing the email address of the user.

* `password`: A string representing the password of the user.

* `disabled`: A boolean value indicating whether the user is disabled or not. If disabled is true, the user won't be able to access the other API endpoints.

### **Possible responses**

#### **User already exists:**

`Status code 400` 

If the user already exists in the database, this request will return an exception indicating that the user already exists.

#### **User created successfully:**

`Status code 200`

If the user is created successfully, this request will return the data with which the user was created. The user's ID and password will not be displayed.

#### **Field Requerid:**

If any of the mentioned fields are missing, the system will return a message stating that fields are missing to create the user.


Here you can see how to make a post to this endpoint using the Python programming language. We use the json library to convert the Python object to a json.
```py
import requests
import json

#To generate the POST request to create a user, we can use the requests library in Python. Here's an example of how to do it:

user_created = requests.post("https://taskninja.onrender.com/user/create", data=json.dumps({
            "username": "JDoe",
            "full_name": "Jhon Doe",
            "password": "Jd3506",
            "email": "jhondoe@doe.com",
            "disable": "false"
        }))
```
____
## **Login Users<a name="loginuser"></a>**

`EndPoint /user/login`

The request to this endpoint should be made using the POST method, where we will pass the username and password in a form. After verifying that the credentials are correct, an access token will be returned, which must be used to access the other services.

To make a request to this endpoint, we should use the POST method and pass the username and password in a form in the request body. After verifying that the credentials are correct, an access token will be returned, which should be used to access the other services.

#### **Fields:**

* `username`: Here, the username with which you want to log in should be passed.

* `password`: The user's password should be passed.

### **Possible responses**

#### **Not User**

`Status code 400`

If the user is not registered, an exception will be thrown with the detail "User not found".

#### **Password Incorrect**

`Status code 400`

If the password is incorrect, an exception will be thrown with the detail "Incorrect password".
#### **Session started successfully**
`Status code 200`

If there is no error, the endpoint will return the type and token of this user.
____

This is a simple login request.

```py
import requests

url = 'https://taskninja.onrender.com/user/login'
username = 'my_username'
password = 'my_password'

# Set the data to be sent in the form
data = {
    'username': username,
    'password': password
}

# Make the POST request to the login endpoint
response = requests.post(url, data=data)

# Check if the request was successful (status code 200)
if response.ok:
    # Access token is returned in the response body
    access_token = response.json().get('access_token')
    print('Access token:', access_token)
else:
    # If the request failed, raise an exception with the response body as the message
    response.raise_for_status()
```
## **Current User**
`EndPoint /user/me`

This endpoint is only available using the GET method. To access it, we need to pass the token obtained from the Login as a header.

Here's a brief example of how we could make the request with the token in the header:

```py
import requests

url = 'https://taskninja.onrender.com/user/me'
token = 'my_token'

# Set the Authorization header with the token
headers = {
    'Authorization': f'Bearer {token}'
}

# Make the GET request to the get_data endpoint with the Authorization header
response = requests.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    # If the request failed, raise an exception with the response body as the message
    response.raise_for_status()

```
_______
### **Endpoints to manage tasks**
There are 4 endpoints available to manage tasks, which allow you to create, delete, update, or list all your tasks. These operations depend on whether the user is registered and logged in correctly to the system. To do so, you must send the token obtained at login through the header.

* [POST /tasks/create: Creates a new tasks.](#createtask)

* DELETE /tasks/delete/{task_id}: Delete tasks.

* GET /tasks/all: Returns all tasks depending on the logged-in user

* UPDATE /tasks/update: You can update task information using the following endpoint


## **Create Tasks**
`EndPoint /tasks/create`

This endpoint is the one you must use to create tasks, you must pass in the request header the token that verifies that you are logged in.

#### **Fields:**
* `affair`: This is affair the task

### **Possible responses**
#### **Not Authenticated**

`Status code 401`

If the user not is authenticated correctly the endpoint will return "Not authenticated".

#### **Field Requerid**
`Status code 400`

If your request does not contain the necessary fields, this endpoint will return a "Field required" message.
#### **Task Created**
`Status code 201`

if no error occurs, the endpoint will return "A JSON with the information of the created task".

```py
import requests 
import json

affair = "This is affair "

token = "Access Token"

create = requests.post('https://taskninja.onrender.com/tasks/create', data=json.dumps(
            {"affair": affair}), headers={"Authorization": f'Bearer {token}'})
```


`Other entpoints coming soon`