create table chats
(
    id        numeric not null
        constraint chats_pk
            primary key,
    name      text,
    language  text,
    is_active boolean
);

create unique index chats_id_uindex
    on chats (id);

create table admins
(
    user_id  integer,
    chat_id  numeric,
    username text,
    rights   integer
);
