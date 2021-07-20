import { z } from 'zod';
import { randomBytes } from 'crypto';

const portSchema = z.number().int().positive().default(8284);
const portParser = z
	.string()
	.optional()
	.transform((port) => (port === undefined ? undefined : Number(port)));
export const port = portSchema.parse(portParser.parse(process.env.PORT));

const JWTSecretSchema = z.string().default(randomBytes(128).toString('utf8'));
export const JWTSecret = JWTSecretSchema.parse(process.env.JWT_SECRET);

const redisHostSchema = z.string().default('cache');
export const redisHost = redisHostSchema.parse(process.env.SPORTAJ_REDIS_HOST);

const redisPortSchema = z.number().int().positive().default(6379);
const redisPortParser = z
	.string()
	.optional()
	.transform((port) => (port === undefined ? undefined : Number(port)));
export const redisPort = redisPortSchema.parse(redisPortParser.parse(process.env.SPORTAJ_REDIS_PORT));
