import { BaseRedisCache } from 'apollo-server-cache-redis';
import { ApolloServer } from 'apollo-server-koa';
import { GraphQLScalarType, GraphQLSchema } from 'graphql';
import { DateTimeResolver } from 'graphql-scalars';
import Redis from 'ioredis';
import Koa from 'koa';
import 'reflect-metadata';
import { buildSchemaSync } from 'type-graphql';
import { redisHost, redisPort } from './config';
import { context } from './lib/context';

export const buildGqlSchema = (): GraphQLSchema => {
	return buildSchemaSync({
		// @ts-expect-error Will be fixed shortly
		resolvers: [],
		scalarsMap: [{ type: GraphQLScalarType, scalar: DateTimeResolver }]
	});
};

const gqlServer = (): Koa<Koa.DefaultState, Koa.DefaultContext> => {
	const schema = buildGqlSchema();
	const app = new Koa();
	const apolloServer = new ApolloServer({
		context,
		schema,
		introspection: true,
		playground: {
			endpoint: '/',
			settings: {
				'editor.theme': 'dark',
				'editor.fontFamily': '"Fira Code", "MesloLGS NF", "Menlo", Consolas, Courier New, monospace',
				'editor.reuseHeaders': true
			}
		},
		cache: new BaseRedisCache({
			client: new Redis({ host: redisHost, port: redisPort })
		})
	});

	apolloServer.applyMiddleware({ app, path: '/', cors: true });

	return app;
};

export default gqlServer;
