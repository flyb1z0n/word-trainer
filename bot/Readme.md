# Development :

## Setup virtual env

### For Windows
```
sdasd
```
`python -m venv venv`


# For macOS/Linux
`python3 -m venv venv`

## Setup activate venv

# For Windows
`.\venv\Scripts\activate`

# Might requre additional scopes
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`

# For macOS/Linux
`source venv/bin/activate`


## Add dependencies:

### Install dependecies
`pip install package_name`

### Save dependecy list to `requirement.txt`
`pip freeze > requirements.txt`

`pip install -r requirements.txt`

## Docker:

### Building docker image
`docker build -t telegram-bot .`

### Run docker
`docker run -e TELEGRAM_BOT_TOKEN=<your_token_here> telegram-bot`