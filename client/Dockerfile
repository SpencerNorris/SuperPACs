FROM nginx:latest

ADD https://deb.nodesource.com/setup_7.x /opt/node_ppa.sh
RUN chmod u+x /opt/node_ppa.sh
RUN /opt/node_ppa.sh
RUN apt-get install -y nodejs

RUN mkdir /opt/client
COPY . /opt/client
WORKDIR /opt/client
RUN npm install
RUN npm run build
RUN cp -r /opt/client/dist/* /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
