-- TEST DATA
-- CUSTOMER ACCOUNT USERNAME, PASSWORD: test@gmail.com , test2
-- STAFF ACCOUNT USERNAME, PASSWORD: test_staff , test2

-- Delete from all tables
delete from ticket;
delete from customer_phone_number;
delete from customer;
delete from flight;
delete from maintenance_procedures;
delete from airplane;
delete from staff_phone_number;
delete from staff_email;
delete from staff;
delete from airport;
delete from airline;

-- Insert Airline
insert into airline (airline_name) values ('Jet Blue');

-- Insert Airports
insert into airport (code, airport_name, city, country, number_of_terminals, airport_type)
values 
    ('JFK', 'John F. Kennedy International Airport', 'New York City', 'USA', 20, 'international'),
    ('LAX', 'Los Angeles International Airport', 'Los Angeles', 'USA', 18, 'international');

-- Insert Customers
insert into customer (customer_email, customer_password, first_name, last_name, addr_building_number, addr_street, addr_apartment_number, addr_city, addr_state, zip, passport_number, passport_expiration, passport_country, date_of_birth)
values 
    ('test@gmail.com', 'ad0234829205b9033196ba818f7a872b', 'John', 'Doe', 123, 'Main St', 7, 'New York City', 'NY', 10001, 123456789, '2030-12-31', 'USA', '1989-08-26');

-- Insert Airplanes
insert into airplane (id, airline_name, seats, manufacturer, model, manufacture_date)
values 
    (0, 'Jet Blue', 126, 'Boeing', 737, '1994-05-05'),
    (1, 'Jet Blue', 375, 'Boeing', 767, '2018-06-20'),
    (2, 'Jet Blue', 550, 'Boeing', 777, '2021-03-10'),
    (3, 'Jet Blue', 330, 'Boeing', 787, '2016-03-10'),
    (4, 'Jet Blue', 0, 'Boeing', 737, '1994-05-05'),
    (5, 'Jet Blue', 1, 'Boeing', 737, '1994-05-05'),
    (6, 'Jet Blue', 5, 'Boeing', 737, '1994-05-05');

-- Insert Airline Staff
insert into staff (username, staff_password, first_name, last_name, date_of_birth, airline_name)
values 
    ('test_staff', 'ad0234829205b9033196ba818f7a872b', 'Staff', 'Person', '1995-08-24', 'Jet Blue');

-- Insert Flights
insert into flight (airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, base_price, flight_status, id, departure_code, arrival_code)
values 
    ('Jet Blue', 10001, '2024-12-30', '10:00:00', '2024-12-31', '11:00:00', 1250, 'on time', 1, 'JFK', 'LAX'),
    ('Jet Blue', 10002, '2025-01-22', '11:00:00', '2025-01-23', '14:00:00', 700, 'delayed', 2, 'LAX', 'JFK'),
    ('Jet Blue', 10003, '2025-01-23', '12:00:00', '2025-01-24', '13:30:00', 900, 'on time', 3, 'JFK', 'LAX'),
    ('Jet Blue', 9999,  '2025-01-01', '10:00:00', '2025-01-02', '11:00:00', 789, 'on time', 4, 'JFK', 'LAX'),
    ('Jet Blue', 9999,  '2025-01-01', '11:00:00', '2025-01-02', '12:00:00', 123, 'on time', 5, 'JFK', 'LAX'),
    ('Jet Blue', 9999,  '2023-01-01', '11:00:00', '2023-01-02', '12:00:00', 123, 'on time', 5, 'JFK', 'LAX'),
    ('Jet Blue', 9998,  '2025-01-01', '11:00:00', '2025-01-02', '12:00:00', 1000, 'on time', 6, 'JFK', 'LAX');

-- Insert Tickets
insert into ticket (first_name, last_name, date_of_birth, airline_name, flight_number, departure_date, departure_time, card_type, purchase_date_time, name_on_card, expiration_date, customer_email, sold_price)
values 
    ('John', 'Doe', '1989-08-26', 'Jet Blue', 9999, '2023-01-01', '11:00:00', 'debit', '2024-11-03 08:30:00', 'James Harden', '2026-11-01', 'test@gmail.com', 100),
    ('John', 'Doe', '1989-08-26', 'Jet Blue', 9999, '2025-01-01', '11:00:00', 'debit', '2024-11-03 08:30:00', 'James Harden', '2026-11-01', 'test@gmail.com', 100),
    ('John', 'Doe', '1989-08-26', 'Jet Blue', 9999, '2025-01-01', '11:00:00', 'debit', '2024-11-03 08:30:00', 'James Harden', '2026-11-01', 'test@gmail.com', 100),
    ('John', 'Doe', '1989-08-26', 'Jet Blue', 9998, '2025-01-01', '11:00:00', 'debit', '2024-11-03 08:30:00', 'James Harden', '2026-11-01', 'test@gmail.com', 1000),
    ('John', 'Doe', '1989-08-26', 'Jet Blue', 9998, '2025-01-01', '11:00:00', 'debit', '2024-11-03 08:30:00', 'James Harden', '2026-11-01', 'test@gmail.com', 1000),
    ('John', 'Doe', '1989-08-26', 'Jet Blue', 9998, '2025-01-01', '11:00:00', 'debit', '2024-11-03 08:30:00', 'James Harden', '2026-11-01', 'test@gmail.com', 1000),
    ('John', 'Doe', '1989-08-26', 'Jet Blue', 9998, '2025-01-01', '11:00:00', 'debit', '2024-11-03 08:30:00', 'James Harden', '2026-11-01', 'test@gmail.com', 1000);