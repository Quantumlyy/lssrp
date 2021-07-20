import 'reflect-metadata';
import { Field, ID, ObjectType } from 'type-graphql';
import { EmailService } from './EmailService';

@ObjectType()
export class User {
	@Field(() => ID)
	public id!: number;

	@Field()
	public username!: string;

	@Field()
	public password!: string;

	@Field(() => EmailService, { nullable: true })
	public email?: EmailService | null;

	@Field(() => Date)
	public createdAt!: Date;

	@Field(() => Date)
	public updatedAt!: Date;
}
