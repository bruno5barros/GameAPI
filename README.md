# Mini Game Server

Game Rest API backend

### Introduction

This is a simpler Game Rest API backend to serve the final users. I used Python, Django, Django Rest Framework, MySQL, and Docker to solve this exercise. Developed the code using principles like inheritance, DRY, single responsibility, and others.
This solution is suitable for the goal of this stage and for the size of the Application. Other improvements could be done to improve performance if needed and some designs could be applied to improve the code for a more extensive application.

### Architecture

I split the solution into three parts:

- Common
- User
- Game

Common is where I saved classes, functions, and methods to perform tasks that are needed across the application.

User is the app that contains all the code, and models related to users.

Game is the app where you will find all the code, and models related to games, and others are very related to it (like Genre and PlaySession).

### Run the project

You need to have docker to build the code. To run the project use the following command:

- docker-compose up

To run the tests you need to run:

- docker-compose run app sh -c "python manage.py test && flake8"

### Final

These endpoints are available.

- POST /users (create a user) [open to everyone]
- GET /users (list of users) [restricted to staff]
- GET /users/lastplayed (list of users and their last played game) [restricted to staff]
- GET /games (get a listing of games) [open to everyone]
- GET /games/{id} (get a specific game by its id) [open to everyone]
- POST /playsessions (create a playsession) [restricted to authenticated registered users only]
- POST /token (login) [open to everyone]

Thank you!
