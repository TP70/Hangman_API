# Hangman API
This is a simple Hangman API built with Flask and MongoDB. The API allows users to play the classic game of Hangman by starting a new game, making guesses, and ending games.

## Installation
To set up the Hangman API, follow these steps:

## Clone the repository:

```bash
git clone https://github.com/your-username/hangman-api.git
cd hangman-api
```

## Install the required dependencies:

```bash
make install
```

## Usage
Running the Application Locally
To run the application locally, use the following command:

```bash
make up
```

This will start the API using Docker Compose. You can access the API at http://localhost:5000.

## Running Tests
To run the tests, use the following command:

```bash
make test
````

Building and Running with Docker
To build and run the application using Docker, use the following command:

```bash
make build_run
```

Stopping the Docker Containers
To stop the Docker containers, use the following command:

```bash
make down
````

Cleaning Up Docker Resources
If you need to clean up Docker resources, including volumes and orphaned containers, use the following command:

```bash
make clean_docker
```

This will stop the containers, remove volumes, and prune the Docker system.

# API Endpoints
## Start a new game:

### Endpoint: POST /games
Description: Start a new Hangman game.

### Endpoint: GET /games
Description: Get the status of all Hangman games

### Endpoint: GET /games/<game_id>
Description: Get the status of a Hangman game by ID

### Endpoint: POST /games/<game_id>
Description: Make a guess for the specified game.

### Endpoint: DELETE /games/<game_id>
Description: End the specified game.