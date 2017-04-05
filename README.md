# SuperPAC Project

superpac.biz, is a project examining the interactions of SuperPACs and political initiatives.

## Executive Summary

In today’s age of SuperPACs massive funding of politicians it is important for people to know who is influencing those that vote directly on our legislation. While the data for SuperPAC contributions is already available, our website seeks to combine this data with data about how the politicians they contribute to vote on legislation and present it using information-rich but intuitive visualizations, such that any concerned citizen can simply search for either a SuperPAC or a politician and be presented with visuals that easily allow them to “follow the money” from SuperPACs to members of Congress to voting on legislation.

## Project Description

The focus of our website is to create visualizations of how SuperPAC contributions to members of congress affect their voting on different pieces of legislation. A particular visualization, or set of visualizations, is presented when the user searches either for a specific member of Congress or for a specific SuperPAC. If the user searches for a SuperPAC, visualizations will focus on how that SuperPACs contributions to congressmen affect legislation. Conversely, if the user searches for a particular representative, the visuals will focus on what SuperPACs are contributing and how that is reflected in the representative’s voting on legislation. As the goal of the site is to inform, other relevant information, such as more information about a particular SuperPAC or politician, will be either given directly, or linked to, whenever possible.

# Deployment Guide

Use the following instructions to deploy this website on to a server that supports Docker Compose.

## Prerequisites
This project uses Docker compose for its deployment so you'll need
* Docker 1.13+
* Docker Compose 1.11+

Instructions for installing Docker and Docker Compose can be found here:
https://docs.docker.com/compose/install/

You will also need to set the following environment variables
* MYSQL_DATABASE
* MYSQL_USER
* MYSQL_PASSWORD
* MYSQL_ROOT_PASSWORD
* DJANGO_SECRET_KEY
* PP_API_KEY
* FEC_API_KEY

> PP_API_KEY refers to the ProPublic API Key which can be procured from https://www.propublica.org/datastore/api/campaign-finance-api,
> FEC_API_KEY refers to the Federal Election Commission API Key which can be procured from https://api.data.gov/signup/

## Build Instructions
* Clone this project on to the server
* Enter the project directory
* Run `docker-compose build`

Docker Compose will now automatically build all the Docker containers, you may need to run as root for the build to work properly.

## Deployment Instructions
* Run `docker-compose up -d`

Docker Compose will now start the Docker containers and the website should be running on localhost. You may need to run as root, if you do remember to have the environment variables in the root environment. Note that on Windows, the website may instead be running on virtualbox, but you can still access the site through Kinematic which is available as part of the Docker Toolbox download.

> Note, if you are running mysql locally you may need to stop it before deploying Docker

# Development Instructions

## Backend Development

To develop for Django, simply deploy Docker and edit files within the `server/` folder. Changes will be reflected automatically in the Docker contianer.

## Frontend Development

Instructions for frontend development are within the `client/` folder.

# Software Design And Development Documentation.

## Style Guide

We have chosen style guides for Github, Javascript, Python, Object-Oriented Code, d3, and Angular.

https://docs.google.com/document/d/1Abvn7wZxvmLC8nWsMPAthzQ2oexTH3sDtC91zH7zmeI/edit?usp=sharing


## Deployment Diagram

https://drive.google.com/file/d/0B4fJ04kc6tHRQmFMUGpDQ1BFN0E/view?usp=sharing

## Domain Model

https://drive.google.com/file/d/0ByU5I4EWAyp5cjdSdFpBZ2xEa3c/view?usp=sharing

## Inception document

https://docs.google.com/document/d/1J4wr-IQZrq70X1NWiGK2sZdRkyR7uL44O6pK88FKAZk/edit?usp=sharing

## Elaboration document

https://docs.google.com/document/d/1N2Na6WvKSEU1u6L_2dpugFqMjkHSLFVl76K2zl2guqk/edit?usp=sharing
