drop table if exists gifs;
create table gifs (
    gif_id integer primary key autoincrement,
    gif_name varchar(255) not null,
    gif_file varchar(255) not null
);
drop table if exists tags;
create table tags (
    tag_id integer primary key autoincrement,
    tag_name varchar (255) UNIQUE not null
);
drop table if exists gifs_to_tags;
create table gifs_to_tags (
    gtt_id integer primary key autoincrement,
    gtt_gif integer,
    gtt_tag integer,
    FOREIGN KEY (gtt_gif) REFERENCES gifs(gif_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (gtt_tag) REFERENCES tags(tag_id) ON DELETE CASCADE ON UPDATE CASCADE
);
drop table if exists params;
create table params (
    param_key varchar(255) primary key,
    param_val integer 
);
drop table if exists memes;
create table memes (
    meme_id integer primary key autoincrement,
    meme_file varchar(255) not null,
    meme_name varchar(255) not null,
    meme_txt1 varchar(150),
    meme_txt2 varchar(150)
);
insert into params values("gifcount", 0);
insert into params values("memecount", 0);
insert into params values("memegencount", 0);
