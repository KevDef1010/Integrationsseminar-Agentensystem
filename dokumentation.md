---

# Task Management System Technical Documentation

## Project Overview

The Task Management System is a web application that allows users to efficiently organize, prioritize, and manage their tasks. The system provides a user-friendly interface for creating, retrieving, updating, and deleting tasks using an API.

### Key Features

* Create new tasks through a graphical user interface with the click of a button or by entering text into a field
* Retrieve all tasks, a single task by ID, and tasks with specific priorities, deadlines, or categories using API methods
* Mark tasks as completed
* Update or delete users
* Sort tasks by priority or deadline through the API

## Functionality

The following sections describe the functionalities of the Task Management System.

### Tasks

The system allows users to create new tasks and retrieve all tasks, a single task by ID, and tasks with specific priorities, deadlines, or categories using the API. The API also provides functionality for marking tasks as completed.

#### Task API Endpoints

* `/tasks`: List all tasks
* `/tasks/<int:task_id>`: Get a single task by ID
* `/tasks/<int:task_id>/complete`: Mark a task as completed

### Users

The system allows users to create, update, and delete their own user accounts using the API. The API also provides functionality for retrieving all users and a single user by email address.

#### User API Endpoints

* `/users`: List all users
* `/users/<string:email>`: Get a single user by email address
* `/users/<string:email>/update`: Update the password for a user
* `/users/<string:email>/delete`: Delete a user by email address

### Error Handling

The system checks if the provided data is valid before processing it, which helps prevent errors such as an empty task title, an invalid date format for the deadline, or a non-existent user ID for a task.

### Code Quality

The code follows basic best practices, such as using descriptive variable names, commenting the code, and organizing it logically. Type hints are used to make the code easier to understand.

### Documentation

Detailed documentation is provided for the Task Management System, including descriptions of each function, parameters, return values, and examples of usage. The documentation can be found in the [Documentation](#documentation) section below.

### Bugs

The system has been thoroughly tested to ensure that there are no hidden issues or errors.

## Installation

To install the Task Management System, follow these steps:

1. Clone this repository: `git clone https://github.com/YOUR_USERNAME/task-management-system.git`
2. Navigate to the project directory: `cd task-management-system`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Run the application: `python app.py`

## Usage

Once the system is running, you can access the API at `http://localhost:5000`. To use the API, send HTTP requests to the specified endpoints using a tool such as Postman or curl.

### Examples

#### List All Tasks

To list all tasks, send an HTTP GET request to `/tasks`:
```
GET http://localhost:5000/tasks
```
The response will be a JSON array containing the details of all tasks in the system.

#### Get a Single Task by ID

To get a single task by ID, send an HTTP GET request to `/tasks/<int:task_id>`, where `<int:task_id>` is the ID of the task you want to retrieve:
```
GET http://localhost:5000/tasks/1234567890
```
The response will be a JSON object containing the details of the specified task.

#### Mark a Task as Completed

To mark a task as completed, send an HTTP PATCH request to `/tasks/<int:task_id>/complete`, where `<int:task_id>` is the ID of the task you want to update:
```
PATCH http://localhost:5000/tasks/1234567890/complete
```
The response will indicate whether the task was successfully marked as completed.

## Documentation

Detailed documentation for the Task Management System can be found in the [Documentation](docs/documentation.md) file in this repository.

---

I hope you find this technical documentation helpful. If you have any questions or concerns, please don't hesitate to reach out. Enjoy using the Task Management System!