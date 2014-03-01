drop table if exists gifs;
create table gifs (
    gif_id integer primary key autoincrement,
    gif_name varchar(255) not null,
    gif_file varchar(255) not null
);
drop table if exists tags;
create table tags (
    tag_id integer primary key autoincrement,
    tag_name varchar (255) not null
);
drop table if exists gifs_to_tags;
create table gifs_to_tags (
    gtt_id integer primary key autoincrement,
    gtt_gif integer,
    gtt_tag integer,
    FOREIGN KEY (gtt_gif) REFERENCES gifs(gif_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (gtt_tag) REFERENCES tags(tag_id) ON DELETE CASCADE ON UPDATE CASCADE
);
