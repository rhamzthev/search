FROM node:latest AS build

WORKDIR /usr/src/app

COPY package*.json .
RUN npm i

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=build /usr/src/app/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /usr/src/app/dist /usr/share/nginx/html

EXPOSE 80