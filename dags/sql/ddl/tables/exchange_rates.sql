create table if not exists exchange_rates (
    id serial primary key,
    base varchar(50) not null,
    target varchar(50) not null,
    ts timestamp not null,
    rate double precision not null
);