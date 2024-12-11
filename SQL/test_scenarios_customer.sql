-- Delete tables
-- delete from customer;
-- delete from customer_phone_number;
delete from ticket;
delete from takes;

-- -- Insert Customers
-- INSERT INTO customer (customer_email, customer_password, first_name, last_name, addr_building_number, addr_street, addr_apartment_number, addr_city, addr_state, zip, passport_number, passport_expiration, passport_country, date_of_birth)
-- values 
--     ('testcustomer@nyu.edu', MD5('1234'), 'Jon', 'Snow', 1555, 'Jay St', 0, 'Brooklyn', 'New York', 00000, 54321, '2025-12-24', 'USA', '1999-12-19'),
--     ('user1@nyu.edu', MD5('1234'), 'Alice', 'Bob', 5405, 'Jay Street', 0, 'Brooklyn', 'New York', 00000, 54322, '2025-12-25', 'USA', '1999-11-19'),
--     ('user2@nyu.edu', MD5('1234'), 'Cathy', 'Wood', 1702, 'Jay Street', 0, 'Brooklyn', 'New York', 00000, 54323, '2025-10-24', 'USA', '1999-10-19'),
--     ('user3@nyu.edu', MD5('1234'), 'Trudy', 'Jones', 1890, 'Jay Street', 0, 'Brooklyn', 'New York', 00000, 54324, '2025-09-24', 'USA', '1999-09-19');

-- -- Insert Customer Phone Number
-- INSERT INTO customer_phone_number
-- VALUES
--     ('testcustomer@nyu.edu', 12343214321),
--     ('user1@nyu.edu', 12343224322),
--     ('user2@nyu.edu', 12343234323),
--     ('user3@nyu.edu', 12343244324);

-- Insert Tickets
INSERT INTO ticket (code, first_name, last_name, date_of_birth, airline_name, flight_number, departure_date, departure_time, card_type, purchase_date_time, name_on_card, expiration_date, customer_email, sold_price)
VALUES
    (1, 'Jon', 'Snow', '1999-12-19', 'JetBlue', '102', '2024-09-20', '13:25:25', 'credit', '2024-08-17 11:55:55', 'JonSnow', '', 'testcustomer@nyu.edu', 300),
    (2, 'Alice', 'Bob', '1999-11-19', 'JetBlue', '102', '2024-09-20', '13:25:25', 'credit', '2024-08-16 11:55:55', 'AliceBob', '', 'user1@nyu.edu', 300),
    (3, 'Cathy', 'Wood', '1999-10-19', 'JetBlue', '102', '2024-09-20', '13:25:25', 'credit', '2024-09-14 11:55:55', 'CathyWood', '', 'user2@nyu.edu', 300),
    (4, 'Alice', 'Bob', '1999-11-19', 'JetBlue', '104', '2024-10-04', '13:25:25', 'credit', '2024-08-21 11:55:55', 'AliceBob', '', 'user1@nyu.edu', 300),
    (5, 'Jon', 'Snow', '1999-12-19', 'JetBlue', '104', '2024-10-04', '13:25:25', 'credit', '2024-09-28 11:55:55', 'JonSnow', '', 'testcustomer@nyu.edu', 300),
    (6, 'Jon', 'Snow', '1999-12-19', 'JetBlue', '106', '2024-08-04', '13:25:25', 'credit', '2024-08-02 11:55:55', 'JonSnow', '', 'testcustomer@nyu.edu', 350),
    (7, 'Trudy', 'Jones', '1999-09-19', 'JetBlue', '106', '2024-08-04', '13:25:25', 'credit', '2024-07-23 11:55:55', 'TrudyJones', '', 'user3@nyu.edu', 350),
    (8, 'Trudy', 'Jones', '1999-09-19', 'JetBlue', '839', '2023-12-26', '13:25:25', 'credit', '2023-12-23 11:55:55', 'TrudyJones', '', 'user3@nyu.edu', 300),
    (9, 'Trudy', 'Jones', '1999-09-19', 'JetBlue', '102', '2024-09-20', '13:25:25', 'credit', '2024-07-14 11:55:55', 'TrudyJones', '', 'user3@nyu.edu', 300),
    (11, 'Trudy', 'Jones', '1999-09-19', 'JetBlue', '134', '2023-12-15', '13:25:25', 'credit', '2023-10-23 11:55:55', 'TrudyJones', '', 'user3@nyu.edu', 300),
    (12, 'Jon', 'Snow', '1999-12-19', 'JetBlue', '715', '2024-09-28', '10:25:25', 'credit', '2024-05-02 11:55:55', 'JonSnow', '', 'testcustomer@nyu.edu', 500),
    (14, 'Trudy', 'Jones', '1999-09-19', 'JetBlue', '206', '2025-02-04', '13:25:25', 'credit', '2024-11-20 11:55:55', 'TrudyJones', '', 'user3@nyu.edu', 400),
    (15, 'Alice', 'Bob', '1999-11-19', 'JetBlue', '206', '2025-02-04', '13:25:25', 'credit', '2024-11-21 11:55:55', 'AliceBob', '', 'user1@nyu.edu', 400),
    (16, 'Cathy', 'Wood', '1999-10-19', 'JetBlue', '206', '2025-02-04', '13:25:25', 'credit', '2024-09-19 11:55:55', 'CathyWood', '', 'user2@nyu.edu', 400),
    (17, 'Alice', 'Bob', '1999-11-19', 'JetBlue', '207', '2025-03-04', '13:25:25', 'credit', '2024-08-15 11:55:55', 'AliceBob', '', 'user1@nyu.edu', 300),
    (18, 'Jon', 'Snow', '1999-12-19', 'JetBlue', '207', '2025-03-04', '13:25:25', 'credit', '2024-09-25 11:55:55', 'JonSnow', '', 'testcustomer@nyu.edu', 300),
    (19, 'Alice', 'Bob', '1999-11-19', 'JetBlue', '296', '2024-12-30', '13:25:25', 'credit', '2024-11-22 11:55:55', 'AliceBob', '', 'user1@nyu.edu', 3000),
    (20, 'Jon', 'Snow', '1999-12-19', 'JetBlue', '296', '2024-12-30', '13:25:25', 'credit', '2023-12-17 11:55:55', 'JonSnow', '', 'testcustomer@nyu.edu', 3000)

-- Insert into Takes
INSERT INTO takes (customer_email, airline_name, flight_number, depature_date, departure_time, rating, comment)
VALUES
    ('testcustomer@nyu.edu', 'JetBlue', 102, '2024-09-20', '13:25:25', 4, "Very Comfortable"),
    ('user1@nyu.edu', 'JetBlue', 102, '2024-09-20', '13:25:25', 5, "Relaxing, check-in and onboarding very professional"),
    ('user2@nyu.edu', 'JetBlue', 102, '2024-09-20', '13:25:25', 3, "Satisfied and will use the same flight again"),
    ('testcustomer@nyu.edu', 'JetBlue', 104, '2024-10-04', '13:25:25', 1, "“Customer Care services are not good"),
    ('user1@nyu.edu', 'JetBlue', 104, '2024-09-20', '13:25:25', 5, "Comfortable journey and Professional");