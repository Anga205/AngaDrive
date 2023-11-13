### drive.anga.pro
a web application for file hosting over the internet

## Getting Started with self-hosting
To get started with hosting your own version of drive.anga.pro, you will need to install its pypi dependencies and Python in a virtual environment. Once you have installed the dependencies, you can clone the drive.anga.pro repository from GitHub.

here are the exact commands to run to host a clone of drive.anga.pro:

# For windows command prompt

first download the repository
`git clone https://github.com/Anga205/drive.anga.pro`

enter the cloned repository
`cd anga.pro`

**NOTE: YOU MUST HAVE virtualenv installed thru pypi to make a virtual environment, if you dont, please run `pip install virtualenv`**

create a virtual environment in the directory
`python -m venv venv`

activate the virtual environment
`venv\Scripts\activate`

install the required dependencies, reflex and requests
`pip install -r requirements.txt`

initialize reflex
`reflex init`

startup the website
`reflex run`

*once you have run all these commands, the website should be avalible on http://localhost:3000*



# For debian-based linux systems

first install dependencies:
`sudo apt install python3-venv curl nodejs`

create a virtual environment:
`python3 -m venv venv`

run virtual environment:
`source venv/bin/activate`

download repo:
`git clone https://github.com/Anga205/drive.anga.pro`

install dependencies:
`pip install -r requirements.txt`

initialize reflex:
`reflex init`

run webapp:
`reflex run`

*once you have run all these commands, the website should be avalible on http://localhost:3000*

# Contributing
anga.pro is an open source project, and I welcome contributions from everyone. If you would like to contribute, please fork the repository and submit a pull request.