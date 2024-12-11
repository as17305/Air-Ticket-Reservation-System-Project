-- Delete from all tables
delete from takes;
delete from customer_phone_number;
delete from ticket;
delete from customer;
delete from flight;
delete from airport;
delete from maintenance_procedures;
delete from airplane;
delete from staff_phone_number;
delete from staff_email;
delete from staff;
delete from airline;

-- Airline
insert into airline (airline_name) values ('JetBlue');


-- Airline Staff
insert into staff (username, staff_password, first_name, last_name, date_of_birth, airline_name) values 
    ('admin', MD5('abcd'), 'Roe', 'Jones', '1978-05-25', 'JetBlue');
insert into staff_Email (username, email_address) values 
    ('admin', 'staff1@nyu.edu');
insert into staff_Email (username, email_address) values 
    ('admin', 'staff2@nyu.edu');
insert into staff_Phone_Number (username, phone_number) values 
    ('admin', '11122223333');
insert into staff_Phone_Number (username, phone_number) values 
    ('admin', '44455556666');
    
-- Airplanes
insert into airplane (id, airline_name, seats, manufacturer, model, manufacture_date)
values 
    (1, 'JetBlue', 4, 'Boeing', 'B-101', '2013-05-02'),
    (2, 'JetBlue', 4, 'Boeing', 'A-101', '2011-05-02'),
    (3, 'JetBlue', 50, 'Boeing','B-101', '2015-05-02');

-- Maintenance
insert into maintenance_procedures (ID, airline_name, maintenance_start_date, maintenance_start_time, maintenance_end_date, maintenance_end_time)
values 
    (1, 'JetBlue', '2025-01-27', '13:25:00', '2025-01-29', '07:25:00'),
    (2, 'JetBlue', '2025-01-27', '13:25:00', '2025-01-29', '07:25:00');

-- Airports
insert into airport (code, airport_name, city, country, number_of_terminals, airport_type)
values 
    ('JFK', 'JFK', 'NYC', 'USA', 4, 'both'),
    ('BOS', 'BOS', 'Boston', 'USA', 2, 'both'),
    ('PVG', 'PVG', 'Shanghai', 'China', 2, 'both'),
    ('BEI', 'BEI', 'Beijing', 'China', 2, 'both'),
    ('SFO', 'SFO', 'San Francisco', 'USA', 2, 'both'),
    ('LAX', 'LAX', 'Los Angeles', 'USA', 2, 'both'),
    ('HKA', 'HKA', 'Hong Kong', 'China', 2, 'both'),
    ('SHEN', 'SHEN', 'Shenzhen', 'China', 2, 'both');

-- Customers
insert into customer (customer_email, customer_password, first_name, last_name, addr_building_number, addr_street, addr_apartment_number, addr_city, addr_state, zip, passport_number, passport_expiration, passport_country, date_of_birth)
values 
    ('testcustomer@nyu.edu', MD5(1234), 'Jon', 'Snow', 1555, 'Jay St', 0, 'Brooklyn', 'New York', 00000, 54321, '2025-12-24', 'USA', '1999-12-19'),
    ('user1@nyu.edu', MD5(1234), 'Alice', 'Bob', 5405, 'Jay Street', 0, 'Brooklyn', 'New York', 00000, 54322, '2025-12-25', 'USA', '1999-11-19'),
    ('user2@nyu.edu', MD5(1234), 'Cathy', 'Wood', 1702, 'Jay Street', 0, 'Brooklyn', 'New York', 00000, 54323, '2025-10-24', 'USA', '1999-10-19'),
    ('user3@nyu.edu', MD5(1234), 'Trudy', 'Jones', 1890, 'Jay Street', 0, 'Brooklyn', 'New York', 00000, 54324, '2025-09-24', 'USA', '1999-09-19');
insert into customer_phone_number (customer_email, customer_number) 
values
    ('testcustomer@nyu.edu', 12343214321),
    ('user1@nyu.edu', 12343224322),
    ('user2@nyu.edu', 12343234323),
    ('user3@nyu.edu', 12343244324);

-- Flights
insert into flight (airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, base_price, flight_status, id, departure_code, arrival_code)
values 
    ('JetBlue', 102, '2024-09-20', '13:25:00', '2024-09-20', '16:50:00', 300, 'on time', 3, 'SFO', 'LAX'),
    ('JetBlue', 104, '2024-10-04', '13:25:00', '2024-10-04', '16:50:00', 300, 'on time', 3, 'PVG', 'BEI'),
    ('JetBlue', 106, '2024-08-04', '13:25:00', '2024-08-04', '16:50:00', 350, 'delayed', 3, 'SFO', 'LAX'),
    ('JetBlue', 206, '2025-02-04', '13:25:00', ' 2025-02-04', '16:50:00', 400, 'on time', 2, 'SFO', 'LAX'),
    ('JetBlue', 207, '2025-03-04', '13:25:00', '2025-03-04', '16:50:00', 300, 'on time', 2, 'LAX', 'SFO'),
    ('JetBlue', 134, '2023-12-15', '13:25:00', '2023-12-15', '16:50:00', 300, 'delayed', 3, 'JFK', 'BOS'),
    ('JetBlue', 296, '2024-12-30', '13:25:00', '2024-12-30', '16:50:00', 3000, 'on time', 1, 'PVG', 'SFO'),
    ('JetBlue', 715, '2024-09-28', '10:25:00', '2024-09-28', '13:50:00', 500, 'delayed', 1, 'PVG', 'BEI'),
    ('JetBlue', 839, '2023-12-26', '13:25:00', '2023-12-26', '16:50:00', 300, 'on time', 3, 'SHEN', 'BEI');

-- Insert Tickets
insert into ticket (code, first_name, last_name, date_of_birth, airline_name, flight_number, departure_date, departure_time, card_type, purchase_date_time, card_number, name_on_card, expiration_date, customer_email, sold_price)
values
    (1, 'Jon', 'Snow', '1999-12-19', 'JetBlue', '102', '2024-09-20', '13:25:00', 'credit', '2024-08-17 11:55:55', 1111222233334444, 'Jon Snow', '2025-03-01', 'testcustomer@nyu.edu', 300),
    (2, 'Alice', 'Bob', '1999-11-19', 'JetBlue', '102', '2024-09-20', '13:25:00', 'credit', '2024-08-16 11:55:55', 1111222233335555, 'Alice Bob', '2025-03-01', 'user1@nyu.edu', 300),
    (3, 'Cathy', 'Wood', '1999-10-19', 'JetBlue', '102', '2024-09-20', '13:25:00', 'credit', '2024-09-14 11:55:55', 1111222233335555, 'Cathy Wood', '2025-03-01', 'user2@nyu.edu', 300),
    (4, 'Alice', 'Bob', '1999-11-19', 'JetBlue', '104', '2024-10-04', '13:25:00', 'credit', '2024-08-21 11:55:55', 1111222233335555, 'Alice Bob', '2024-03-01', 'user1@nyu.edu', 300),
    (5, 'Jon', 'Snow', '1999-12-19', 'JetBlue', '104', '2024-10-04', '13:25:00', 'credit', '2024-09-28 11:55:55', 1111222233334444, 'Jon Snow', '2024-03-01', 'testcustomer@nyu.edu', 300),
    (6, 'Jon', 'Snow', '1999-12-19', 'JetBlue', '106', '2024-08-04', '13:25:00', 'credit', '2024-08-02 11:55:55', 1111222233334444, 'Jon Snow', '2024-03-01', 'testcustomer@nyu.edu', 350),
    (7, 'Trudy', 'Jones', '1999-09-19', 'JetBlue', '106', '2024-08-04', '13:25:00', 'credit', '2024-07-23 11:55:55', 1111222233335555, 'Trudy Jones', '2024-03-01', 'user3@nyu.edu', 350),
    (8, 'Trudy', 'Jones', '1999-09-19', 'JetBlue', '839', '2023-12-26', '13:25:00', 'credit', '2023-12-23 11:55:55', 1111222233335555, 'Trudy Jones', '2024-03-01', 'user3@nyu.edu', 300),
    (9, 'Trudy', 'Jones', '1999-09-19', 'JetBlue', '102', '2024-09-20', '13:25:00', 'credit', '2024-07-14 11:55:55', 1111222233335555, 'Trudy Jones', '2024-03-01', 'user3@nyu.edu', 300),
    (11, 'Trudy', 'Jones', '1999-09-19', 'JetBlue', '134', '2023-12-15', '13:25:00', 'credit', '2023-10-23 11:55:55', 1111222233335555, 'Trudy Jones', '2024-03-01', 'user3@nyu.edu', 300),
    (12, 'Jon', 'Snow', '1999-12-19', 'JetBlue', '715', '2024-09-28', '10:25:00', 'credit', '2024-05-02 11:55:55', 1111222233334444, 'Jon Snow', '2024-03-01', 'testcustomer@nyu.edu', 500),
    (14, 'Trudy', 'Jones', '1999-09-19', 'JetBlue', '206', '2025-02-04', '13:25:00', 'credit', '2024-11-20 11:55:55', 1111222233335555, 'Trudy Jones', '2024-03-01', 'user3@nyu.edu', 400),
    (15, 'Alice', 'Bob', '1999-11-19', 'JetBlue', '206', '2025-02-04', '13:25:00', 'credit', '2024-11-21 11:55:55', 1111222233335555, 'Alice Bob', '2024-03-01', 'user1@nyu.edu', 400),
    (16, 'Cathy', 'Wood', '1999-10-19', 'JetBlue', '206', '2025-02-04', '13:25:00', 'credit', '2024-09-19 11:55:55', 1111222233335555, 'Cathy Wood', '2024-03-01', 'user2@nyu.edu', 400),
    (17, 'Alice', 'Bob', '1999-11-19', 'JetBlue', '207', '2025-03-04', '13:25:00', 'credit', '2024-08-15 11:55:55', 1111222233335555, 'Alice Bob', '2024-03-01', 'user1@nyu.edu', 300),
    (18, 'Jon', 'Snow', '1999-12-19', 'JetBlue', '207', '2025-03-04', '13:25:00', 'credit', '2024-09-25 11:55:55', 1111222233334444, 'Jon Snow', '2024-03-01', 'testcustomer@nyu.edu', 300),
    (19, 'Alice', 'Bob', '1999-11-19', 'JetBlue', '296', '2024-12-30', '13:25:00', 'credit', '2024-11-22 11:55:55', 1111222233334444, 'Alice Bob', '2024-03-01', 'user1@nyu.edu', 3000),
    (20, 'Jon', 'Snow', '1999-12-19', 'JetBlue', '296', '2024-12-30', '13:25:00', 'credit', '2023-12-17 11:55:55', 1111222233334444, 'Jon Snow', '2024-03-01', 'testcustomer@nyu.edu', 3000);

-- Insert into Takes
insert into takes (customer_email, airline_name, flight_number, departure_date, departure_time, rating, comment)
values
    ('testcustomer@nyu.edu', 'JetBlue', 102, '2024-09-20', '13:25:00', 4, "Very Comfortable"),
    ('user1@nyu.edu', 'JetBlue', 102, '2024-09-20', '13:25:00', 5, "Relaxing, check-in and onboarding very professional"),
    ('user2@nyu.edu', 'JetBlue', 102, '2024-09-20', '13:25:00', 3, "Satisfied and will use the same flight again"),
    ('testcustomer@nyu.edu', 'JetBlue', 104, '2024-10-04', '13:25:00', 1, "Customer Care services are not good"),
    ('user1@nyu.edu', 'JetBlue', 104, '2024-10-04', '13:25:00', 5, "Comfortable journey and Professional");