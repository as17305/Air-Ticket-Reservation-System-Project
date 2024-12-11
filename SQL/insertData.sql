-- Arnik Shah and Kenny Lau

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
    ('LBJ1969', 'JFK', 'New York City', 'USA', 20, 'international'),
    ('XJP2020', 'PVG', 'Shanghai', 'china', 18, 'international');

-- Insert Customers
insert into customer (customer_email, customer_password, first_name, last_name, addr_building_number, addr_street, addr_apartment_number, addr_city, addr_state, zip, passport_number, passport_expiration, passport_country, date_of_birth)
values 
    ('james.harden@gmail.com', 'Rockets89', 'James', 'Harden', 123, 'Main St', 7, 'New York City', 'NY', 10001, 123456789, '2030-12-31', 'USA', '1989-08-26'),
    ('kevin.durant@gmail.com', 'Thunder88', 'Kevin', 'Durant', 456, 'Broadway', 45, 'New York City', 'NY', 10001, 987654321, '2032-06-22', 'USA', '1968-08-19'),
    ('devin.booker@gmail.com', 'SunsPhx96', 'Devin', 'Booker', 789, 'Pine St', 3, 'Phoenix', 'AZ', 85001, 567891012, '2025-06-17', 'USA', '2005-11-03'),
    ('russell.westbrook@gmail.com', 'DLOla88', 'Russell', 'Westbrook', 321, 'Elm St', 11, 'Los Angeles', 'CA', 90001, 210198765, '2026-1-6', 'USA', '1988-12-12');

-- Insert Airplanes
insert into airplane (id, airline_name, seats, manufacturer, model, manufacture_date)
values 
    (0, 'Jet Blue', 126, 'Boeing', 737, '1994-05-05'),
    (1, 'Jet Blue', 375, 'Boeing', 767, '2018-06-20'),
    (2, 'Jet Blue', 550, 'Boeing', 777, '2021-03-10'),
    (3, 'Jet Blue', 330, 'Boeing', 787, '2016-03-10');

-- Insert Airline Staff
insert into staff (username, staff_password, first_name, last_name, date_of_birth, airline_name)
values 
    ('j.reddick', 'ReddickFakers88', 'Jon', 'Reddick', '1995-08-24', 'Jet Blue');

-- Insert Flights
insert into flight (airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, base_price, flight_status, id, departure_code, arrival_code)
values 
    ('Jet Blue', 10001, '2024-12-30', '10:00:00', '2024-12-31', '11:00:00', 1250, 'on time', 1, 'LBJ1969', 'XJP2020'),
    ('Jet Blue', 10002, '2025-01-22', '11:00:00', '2025-01-23', '14:00:00', 700, 'delayed', 2, 'XJP2020', 'LBJ1969'),
    ('Jet Blue', 10003, '2025-01-23', '12:00:00', '2025-01-24', '13:30:00', 900, 'on time', 3, 'LBJ1969', 'XJP2020');

-- Insert Tickets
insert into ticket (first_name, last_name, date_of_birth, airline_name, flight_number, departure_date, departure_time, card_type, purchase_date_time, name_on_card, expiration_date, customer_email)
values 
    ('James', 'Harden', '1989-08-26', 'Jet Blue', 10001, '2024-12-30', '10:00:00', 'debit', '2024-11-03 08:30:00', 'James Harden', '2026-11-01', 'james.harden@gmail.com'),
    ('Kevin', 'Durant', '1968-08-19', 'Jet Blue', 10002, '2025-01-22', '11:00:00', 'credit', '2024-11-03 09:00:00', 'Kevin Durant', '2026-10-01', 'kevin.durant@gmail.com'),
    ('Devin', 'Booker', '2005-11-03', 'Jet Blue', 10003, '2025-01-23', '12:00:00', 'credit', '2024-11-03 09:30:00', 'Devin Booker', '2026-11-15', 'devin.booker@gmail.com'),
    ('Russell', 'Westbrook', '1988-12-12', 'Jet Blue', 10001, '2024-12-30', '10:00:00', 'credit', '2024-11-03 10:00:00', 'Russell Westbrook', '2025-10-01', 'russell.westbrook@gmail.com');
