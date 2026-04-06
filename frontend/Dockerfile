FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build 


FROM httpd:2.4-alpine

RUN rm -rf /usr/local/apache2/htdocs/*

COPY --from=build /app/build /usr/local/apache2/htdocs/

COPY my-httpd.conf /usr/local/apache2/conf/httpd.conf

EXPOSE 80
