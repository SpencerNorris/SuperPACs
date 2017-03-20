FROM nginx:latest
ADD ./code /code
ADD ./nginx.conf /etc/nginx/nginx.conf
RUN cd /code
RUN npm build
ENTRYPOINT ["npm", "start"]
