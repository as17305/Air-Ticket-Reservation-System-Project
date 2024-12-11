-- Arnik Shah and Kenny Lau

-- Airline Table
create table airline (
    airline_name varchar(20), 
    primary key (airline_name)
);

-- Staff Table
create table staff (
    username varchar(20), 
    staff_password char(32) not null,
    first_name varchar(20) not null,
    last_name varchar(20) not null,
    date_of_birth date not null,
    airline_name varchar(20),
    primary key (username),
    foreign key (airline_name) references airline(airline_name) on delete cascade
);

-- Staff Email Table
create table staff_Email (
    username varchar(20),
    email_address varchar(30),
    primary key (username, email_address),
    foreign key (username) references staff(username) on delete cascade
);

-- Staff Phone Number Table
create table staff_Phone_Number (
    username varchar(20),
    phone_number numeric(12, 0),
    primary key (username, phone_number),
    foreign key (username) references staff(username) on delete cascade
);

-- Airplane Table
create table airplane (
    ID numeric(5, 0),
    airline_name varchar(20),
    seats numeric(4, 0) check (seats >= 0),
    manufacturer varchar(20) not null,
    model varchar(10) not null,
    manufacture_date date not null,
    primary key (ID, airline_name),
    foreign key (airline_name) references airline(airline_name) on delete cascade
);

-- Maintenance Table
create table maintenance_procedures (
    airline_name varchar(20), 
    ID numeric(5, 0),
    maintenance_start_date date,
    maintenance_start_time time,
    maintenance_end_date date,
    maintenance_end_time time,
    primary key (airline_name, ID, maintenance_start_date,maintenance_start_time, maintenance_end_date, maintenance_end_time),
    foreign key (ID, airline_name) references airplane(ID, airline_name) on delete cascade
); 

-- Airport Table
create table airport (
    code varchar(10),
    airport_name varchar(60) not null,
    city varchar(30) not null,
    country varchar(40) not null,
    number_of_terminals numeric(5, 0) check (number_of_terminals > 0),
    airport_type varchar(13) check (airport_type in ('domestic', 'international', 'both')),
    primary key (code)
);

-- Flight Table
create table flight (
    airline_name varchar(20),
    flight_number numeric(10, 0),
    departure_date date,
    departure_time time,
    arrival_date date,
    arrival_time time,
    base_price numeric(5, 0) check (base_price >= 0),
    flight_status varchar(8) check (flight_status in ('delayed', 'on time', 'canceled')),
    ID numeric(5, 0),
    departure_code varchar(10),
    arrival_code varchar(10),
    primary key (airline_name, flight_number, departure_date, departure_time),
    foreign key (ID, airline_name) references airplane(ID, airline_name) on delete cascade,
    foreign key (departure_code) references airport(code) on delete cascade,
    foreign key (arrival_code) references airport(code) on delete cascade
);

-- Customer Table
create table customer (
    customer_email varchar(30),
    customer_password char(32) not null,
    first_name varchar(20) not null,
    last_name varchar(20) not null,
    addr_building_number numeric(5, 0) not null,
    addr_street varchar(20) not null,
    addr_apartment_number numeric(5, 0) not null,
    addr_city varchar(20) not null,
    addr_state varchar(20) not null,
    zip numeric(5, 0) not null,
    passport_number numeric(9, 0) not null,
    passport_expiration date not null,
    passport_country varchar(30) not null,
    date_of_birth date not null,
    primary key (customer_email)
);

-- Ticket Table
create table ticket (
    code int NOT NULL AUTO_INCREMENT,
    first_name varchar(20) not null,
    last_name varchar(20) not null,
    date_of_birth date not null,
    airline_name varchar(20),
    flight_number numeric(10, 0),
    departure_date date,
    departure_time time,
    card_type varchar(6) check (card_type in ('credit', 'debit')),
    purchase_date_time timestamp not null,
    card_number numeric(16, 0),
    name_on_card varchar(40) not null,
    expiration_date date not null,
    customer_email varchar(30),
    sold_price numeric(10, 2),
    primary key (code),
    foreign key (airline_name, flight_number, departure_date, departure_time) references flight(airline_name, flight_number, departure_date, departure_time) on delete cascade,
    foreign key (customer_email) references customer(customer_email) on delete cascade
);

-- Takes Flight Table
create table takes (
    customer_email varchar(30),
    airline_name varchar(20),
    flight_number numeric(10, 0),
    departure_date date,
    departure_time time,
    comment varchar(200),
    rating numeric(10, 0),
    primary key (customer_email, airline_name, flight_number, departure_date, departure_time),
    foreign key (customer_email) references customer(customer_email) on delete cascade,
    foreign key (airline_name, flight_number, departure_date, departure_time) references flight(airline_name, flight_number, departure_date, departure_time) on delete cascade
);

-- Customer Phone Number Table
create table customer_phone_number (
    customer_email varchar(30),
    customer_number numeric(12, 0),
    primary key (customer_email, customer_number),
    foreign key (customer_email) references customer(customer_email) on delete cascade
);
