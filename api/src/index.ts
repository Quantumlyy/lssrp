import 'reflect-metadata';
import { port } from './config';
import gqlServer from './server';

const server = gqlServer();

server.listen({ port: Number(port) }, () => {
	console.log(`server started on http://localhost:${port}`);
});
