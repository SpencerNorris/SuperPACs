# SuperPAC Project

superpac.biz is a project examining the interactions of SuperPACs and political initiatives.

## Executive Summary

In the age of SuperPACs massively funding politicians, it is important to know exactly who is influencing those who vote directly on our legislation. Our website seeks to combine publicly available SuperPAC contribution data with Congressional voting data to create information-rich but intuitive visualizations, so that any concerned citizen can simply search for either a SuperPAC or a politician and “follow the money” from SuperPACs to members of Congress to legislation.

## Project Description

The focus of our website is to visualize how SuperPAC contributions to members of congress affect their voting on different pieces of legislation. A particular visualization or set of visualizations is presented when the user searches either for a specific member of Congress or for a specific SuperPAC. If the user searches for a SuperPAC, visualizations will focus on how that SuperPAC's contributions to congresspeople affect legislation. Conversely, if the user searches for a particular representative, the visuals will focus on which SuperPACs are contributing and how that is reflected in the representative’s voting patterns on legislation. More information about a particular SuperPAC or politician will be either given directly or linked to where possible.

# Setup Guide

### Docker
This project uses Docker 1.13+ and Docker Compose 1.11+. 
Installation instructions [here](https://docs.docker.com/engine/installation/).

### Database (MySQL)
This project uses MySQL 5.6+. 
Installation instructions [here](https://dev.mysql.com/doc/refman/5.6/en/installing.html).

### Client (Angular)
This project uses Angular 1.6+. 
Download Angular [here](https://angularjs.org/).

### Server (Django)
This project uses Django 1.10.6 with Python 3.6. 
Download Python 3.6 [here](https://www.python.org/downloads/) or use a virtual environment (details below).
Installation instructions for Django [here](https://docs.djangoproject.com/en/1.10/topics/install/).

For more help with Django, check out this [useful video tutorial](https://www.youtube.com/playlist?list=PLQVvvaa0QuDeA05ZouE4OzDYLHY-XH-Nd).

Note:  There is an encryption key in `restapi/rest/rest/settings.py` that must be securely stored, out of production. Stick it in an environment variable, and leave it out of the code.

## Virtual Environment for Python 3.

Included in the gitignore is the file `/superpac`. It is meant to be the virtual environment file, there so you can work with the python 3 code even with python 2.7 installed.

Run `SuperPACs/ $ virtualenv -p python3 superpac`. A new folder will be created: `/superpac`. Now run `$ python3` and Python 3 will start.

# Deployment Guide

Use the following instructions to deploy this website on to a server that supports Docker Compose.

## Prerequisites
You will need to set the following environment variables:
* `MYSQL_DATABASE`
* `MYSQL_USER`
* `MYSQL_PASSWORD`
* `MYSQL_ROOT_PASSWORD`
* `DJANGO_SECRET_KEY`

## Build Instructions
* Clone this project onto the server
* Enter the project directory
* Run `docker-compose build`

Docker Compose will automatically build all the Docker containers. You may need to run as root for the build to work properly.

## Deployment Instructions
* Run `docker-compose up -d`

Docker Compose will start the Docker containers and the website should be running on localhost. You may need to run as root. If you do, remember to have the environment variables in the root environment.

# Software Design And Development Documentation.

## Style

We have chosen style guides for [Github](https://sethrobertson.github.io/GitBestPractices/), [Javascript](https://google.github.io/styleguide/jsguide.html), [Python](https://google.github.io/styleguide/pyguide.html), and [Angular](https://google.github.io/styleguide/angularjs-google-style.html).

## Deployment Diagram

![Deployment Diagram](https://lh4.googleusercontent.com/Rc-BI434lkhq59SBmjxQgtHMp8-AdFfe_UH_84F6yACxUgEL4pquDi17hqTc89HMwN5XppKRaZA14zI=w1600-h770-rw)

## Domain Model

![Domain Model](https://lh5.googleusercontent.com/GG82Cm7vj0BM6_TSgyuD1P9OZqFGY2LCw17x5tky4mCqa1alWWcAZpBka1DO43id-_qTVjmCAC5Ds6g=w1600-h770-rw)

## Inception document

https://docs.google.com/document/d/1J4wr-IQZrq70X1NWiGK2sZdRkyR7uL44O6pK88FKAZk/edit?usp=sharing

## Elaboration document

https://docs.google.com/document/d/1N2Na6WvKSEU1u6L_2dpugFqMjkHSLFVl76K2zl2guqk/edit?usp=sharing
