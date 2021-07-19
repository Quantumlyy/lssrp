FROM --platform=linux/amd64 node:16-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache dumb-init

COPY --chown=node:node package.json ./
COPY --chown=node:node yarn.lock ./
COPY --chown=node:node prisma/ prisma/
COPY --chown=node:node generated/api generated/api/

RUN yarn install --frozen-lockfile

RUN yarn global add prisma
RUN yarn generate:prisma

USER node

CMD ["dumb-init", "yarn", "start"]
