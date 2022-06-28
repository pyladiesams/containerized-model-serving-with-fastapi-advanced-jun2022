
# A Deep Dive into Containerized Model Serving with FastAPI
### Level: Advanced
### Presentation: [A Deep Dive into Containerized Model Serving with FastAPI](workshop/Presentation_template.pptx)

## Workshop description

The goal of this hands-on workshop is to create an end-to-end Machine Learning solution that recommends Spotify songs based on your personal music taste. To make your solution available for others, you build and containerize an API that acts as an entry point, using Docker and FastAPI. This way, you can make an impact with your Machine Learning algorithm on any machine in the world! 

FastAPI lets you build robust and high-performance APIs that scale in production environments. Simplicity, speed, the possibility of asynchronous requests, and automatic doc generation are some advantages of FastAPI over Flask, another API web framework.

A container is an isolated, portable computing environment. It contains everything an application needs to run, from binaries to dependencies to configuration files. The advantages of containerization are portability, efficiency, easy to use, scalability, lightweight. 

## Requirements

+ git
+ bash shell (git bash on Windows, bash on Linux, zsh/bash on Mac)
+ IDE (Visual Studio Code, PyCharm, ...)
+ Docker desktop
+ [Optional] Spotify developer app [link](https://developer.spotify.com/dashboard/login) (if you want to receive personalised recommendations)

Don't have Docker? 
macOS:
- Install Docker via your terminal: `brew install docker --cask`
- Don't have package manager brew? (https://www.docker.com/products/docker-desktop/)
Windows:
- https://www.docker.com/products/docker-desktop/


## Usage
* Clone the repository
* Create an spotify app in the developer portal [link](https://developer.spotify.com/dashboard/login) Follow these instructions:
  + 1. Click on the Spotify developer app link above. Log in with your (free/premium) Spotify account or sign up for a free Spotify account
  + 2. Create an app
  + 3. Edit the settings by filling in the redirect uri (http://localhost:9000) and hit the save button. The rest of the settings are optional.
* Create an .env file in the workshop directory with a client_id, client_secret and redirect_uri as environment variables. The values for these variables can be found in your Spotify developer app. If you don't have a Spotify developer app, then you can leave your .env file blank.


## Video record
Re-watch YouTube stream [here](https://youtu.be/CBeliQek-Pw)

## Credits
This workshop was set up by @pyladiesams and @nvanommeren and @KarlijnSchipper
