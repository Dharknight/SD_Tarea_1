FROM node:17.8.0-alpine3.15



WORKDIR /app

COPY . .

EXPOSE 8030


RUN npm i
RUN npm i csv

CMD ["npm","run","server"]


