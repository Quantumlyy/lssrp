import 'reflect-metadata';
import argon2 from 'argon2';
import { sign } from 'jsonwebtoken';
import { Arg, Ctx, Directive, Field, InputType, Mutation, ObjectType, Resolver } from 'type-graphql';
import { Context } from '../context';
import { User } from '../objects/User';
import { JWTSecret } from '../../config';

@ObjectType()
export class AuthReturn {
	@Field(() => User)
	public user!: User;

	@Field()
	public token!: string;
}

@InputType()
export class UserAuthInput {
	@Field()
	public username!: string;

	@Field()
	public password!: string;
}

@Resolver(User)
export class UserResolver {
	@Directive('@rateLimit(limit: 3, duration: 60)')
	@Mutation(() => AuthReturn)
	public async signupUser(@Arg('data') data: UserAuthInput, @Ctx() ctx: Context) {
		const user = await ctx.prisma.user.create({
			data: {
				username: data.username,
				password: await argon2.hash(data.password)
			}
		});

		// TODO: User proper signing key
		const token = sign({ user: user.id }, JWTSecret);

		return {
			user,
			token
		};
	}

	@Directive('@rateLimit(limit: 10, duration: 60)')
	@Mutation(() => AuthReturn)
	public async loginUser(@Arg('data') data: UserAuthInput, @Ctx() ctx: Context) {
		const user = await ctx.prisma.user.findUnique({ where: { username: data.username } });
		if (!user) throw new Error('No user found');

		const validPass = await argon2.verify(user.password, data.password);
		if (!validPass) throw new Error('Invalid password');

		// TODO: User proper signing key
		const token = sign({ user: user.id }, JWTSecret);

		return {
			user,
			token
		};
	}
}
