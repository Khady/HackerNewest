drop table if exists archive;
create table archive (
  id INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
  title VARCHAR not null,
  link VARCHAR not null,
  date VARCHAR not null,
  summary VARCHAR not null,
  postid VARCHAR not null
);
