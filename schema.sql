
# To create the database:
# create database twitdb;
# grant all privileges on twitdb.* to 'twit'@'localhost' identified by 'twit';
#
# To create the tables:
# mysql -utwit -ptwit -Dtwitdb < schema.sql

set session storage_engine = "InnoDB";
alter database character set "utf8";

drop table if exists users;
create table users (
    id int not null auto_increment primary key,
    username varchar(64) not null unique,
    #password varchar(64) not null default '',
    #email varchar(64) not null default '',
    #fullname varchar(64) not null default '',
    created timestamp not null,
    key (created)
);

drop table if exists msgs;
create table msgs (
    id int not null auto_increment primary key,
    user_id int not null references users(id),
    username varchar(64) not null,
    text varchar(255) not null,
    created timestamp not null,
    key (user_id),
    key (created)
);

drop table if exists follows;
create table follows (
    id int not null auto_increment primary key,
    user_id int not null references users(id),
    followed_id int not null references users(id),
    followed_username varchar(64) not null,
    created timestamp not null,
    key (user_id),
    key (followed_id)
);

