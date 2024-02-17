create table user_roles
(
    id smallint generated always as identity,
    role varchar(16) unique,

    constraint PK__user_roles__key primary key(id)
);

INSERT INTO user_roles (role) VALUES ('STUDENT'), ('TEACHER');

create table users
(
	id int generated always as identity,
	chat_id bigint unique not null,
	user_role_id smallint not null,

	constraint PK__users__key primary key(id),
	constraint FK__users__user_role foreign key(user_role_id) references user_roles(id)
);

create table departments
(
	id int generated always as identity,
	name varchar(64) unique not null,
	
	constraint PK__departments__key primary key(id)
);

create table teachers
(
	user_id int,
	first_name varchar(48) not null,
	last_name varchar(48) not null,
	department_id int not null,
	
	constraint PK__teachers__key primary key(user_id),
	constraint FK__teachers__user foreign key(user_id) references users(id) ON DELETE CASCADE,
	constraint FK__teachers__department foreign key(department_id) references departments(id)
);

create table students
(
	user_id int,
	group_name varchar(7) not null,
	department_id int not null,
	
	constraint PK__students__key primary key(user_id),
	constraint FK__students__user foreign key(user_id) references users(id) ON DELETE CASCADE,
	constraint FK__students__department foreign key(department_id) references departments(id)
);

create table schedules
(
	id int generated always as identity,
	json jsonb not null,
	department_id int not null,
	date date not null,
	
	constraint PK__schedules__key primary key(id),
	constraint FK__schedules__user foreign key(department_id) references departments(id)
);