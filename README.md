### Anga.pro
anga.pro is an open source Python web app made in Reflex. It is a simple app that allows users to create and manage their to-do lists.

### Features
* File hosting

## Getting Started
To get started with hosting your own version of anga.pro, you will need to install reflex==0.2.4 and Python in a virtual environment. Once you have installed the dependencies, you can clone the anga.pro repository from GitHub.

here are the exact commands to run to use anga.pro:

# For windows command prompt

first download the repository
`git clone hhtps://github.com/Anga205/anga.pro`

enter the cloned repository
`cd anga.pro`

**NOTE: YOU MUST HAVE virtualenv installed thru pypi to make a virtual environment, if you dont, please run `pip install virtualenv`**

create a virtual environment in the directory
`python -m venv venv`

activate the virtual environment
`venv\Scripts\activate`

install the required dependencies, reflex and requests
`pip install git+https://github.com/reflex-dev/reflex@masenf/on_mount`
`pip install requests`

initialize reflex
`reflex init`

startup the website
`reflex run`

*once you have run all these commands, the website should be avalible on http://localhost:3000*

# Contributing
anga.pro is an open source project, and I welcome contributions from everyone. If you would like to contribute, please fork the repository and submit a pull request.