import { JwtPayload, verify } from 'jsonwebtoken';
import 'reflect-metadata';
import { Arg, Ctx, Field, InputType, Query, Resolver } from 'type-graphql';
import { JWTSecret } from '../../config';
import { Context } from '../context';
import { EmailService } from '../objects/EmailService';

@InputType()
export class UserEmailFetch {
	@Field()
	public username!: string;

	@Field()
	public token!: string;
}

@Resolver(EmailService)
export class EmailServiceResolver {
	@Query(() => EmailService)
	public async signupUser(@Arg('data') data: UserEmailFetch, @Ctx() ctx: Context) {
		// TODO: User proper signing key
		const token = verify(data.token, JWTSecret) as JwtPayload;
		if (data.username !== token.username) throw new Error('Invalid username');

		const emailAccount = await ctx.prisma.emailService.findFirst({
			where: {
				userUsername: {
					equals: token.username
				}
			}
		});

		if (!emailAccount) throw new Error('No email account found');

		return emailAccount;
	}
}
