import { IsEmail } from 'class-validator';
import 'reflect-metadata';
import { Field, ID, ObjectType } from 'type-graphql';
import { User } from './User';

@ObjectType()
export class EmailService {
	@Field(() => ID)
	public id!: number;

	@Field()
	public username!: string;

	@Field()
	@IsEmail()
	public address!: string;

	@Field(() => User)
	public user!: User;

	@Field(() => [Email])
	public sent!: [Email];

	@Field(() => [Email])
	public received!: [Email];

	@Field(() => Date)
	public createdAt!: Date;

	@Field(() => Date)
	public updatedAt!: Date;
}

@ObjectType()
export class Email {
	@Field(() => ID)
	public id!: number;

	@Field({ nullable: true })
	public subject?: string | null;

	@Field({ nullable: true })
	public content?: string | null;

	@Field(() => EmailService)
	public sender!: EmailService;

	@Field(() => EmailService)
	public receiver!: EmailService;

	@Field(() => Date)
	public createdAt!: Date;
}
