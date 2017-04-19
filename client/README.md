# SuperPAC Client Code

This client uses the base code structure provided by https://github.com/preboot/angularjs-webpack

We use the webpack v2 build system to compile our frontend assets into a bundle which we then serve through our static assets server (Nginx).

# Development Instructions
Use the following instructions to develop code for client side use

## Dependencies
What you'll need the begin development:
* `node`and `npm`
* Ensure you're running Node (v7.7.3+) and NPM (4.1.2+)

## Installing
* On your local copy of this project, enter this directory (`client/`)
* Run `npm install`

This will install all the dependencies needed.

## Running
* Run `npm start`

The webpack dev server is now serving content at `http://localhost:8080`.

The webpack dev server proxies requests that are sent to `api/`.
To set the server that it points to set the environment variable `API_SERVER`, the default value used is `http://localhost:8000`.
We recommend running the Docker container for this, with the `API_SERVER` enviroment variable pointing to the Django server in Docker.


This is the point at which you can begin developing.
Any changed made will update in real time and automatically refresh the browser window.

## Testing
Run client test with the following commands.
* Run tests `npm test`
* Run tests live `npm run test-watch` (best when developing tests or fixing code that broke tests)

# Deployment Instructions
Run the following command to build all the assets.
* `npm run build`

The `dist` folder now contains all the compiled client assets, this can be served our static assets server.
