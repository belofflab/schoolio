FROM node:latest

WORKDIR /panel
COPY . .

RUN npm i 
ENV NODE_ENV production
EXPOSE 3000

CMD [ "npx", "serve", "build" ]