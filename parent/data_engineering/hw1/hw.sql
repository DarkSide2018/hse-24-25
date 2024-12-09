create table driver
(
    id           serial
        primary key,
    name         varchar(255) not null,
    bank_account numeric(10)  not null
);

alter table driver
    owner to postgres;

create table vehicle
(
    id        serial
        primary key,
    name      varchar(255) not null,
    driver_id bigint       not null
        constraint vehicle_driver_id_fk
            references driver
);

alter table vehicle
    owner to postgres;

create table delivery_point
(
    id   serial
        primary key,
    name varchar(255) not null,
    size bigint       not null
);

alter table delivery_point
    owner to postgres;

create table "order"
(
    id            serial
        primary key,
    name          varchar(255) not null,
    price         numeric(10)  not null,
    delivery_fee  numeric(10)  not null,
    driver_salary numeric(10)  not null,
    start_point   bigint       not null
        constraint order_delivery_point_start_id_fk
            references delivery_point,
    finish_point  bigint       not null
        constraint order_delivery_point_finish__fk
            references delivery_point,
    driver_id     bigint       not null
        constraint order_driver_id_fk
            references driver
);

alter table "order"
    owner to postgres;

create table route
(
    id   serial
        primary key,
    name varchar(255) not null
);

alter table route
    owner to postgres;

create table route_delivery_point
(
    route_id          bigint not null
        constraint route_delivery_point_route_id_fk
            references route,
    delivery_point_id bigint not null
        constraint route_delivery_point_delivery_point_id_fk
            references delivery_point,
    "order"           bigint not null
);

comment on column route_delivery_point."order" is 'порядок посещения пунктов в маршруте';

alter table route_delivery_point
    owner to postgres;

