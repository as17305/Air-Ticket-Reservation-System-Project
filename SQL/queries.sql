-- Arnik Shah and Kenny Lau

-- Show all the future flights in the system
select *
from flight
where (departure_date > current_date) or (departure_date = current_date and departure_time >= current_time);
-- Results:
-- airline_name	 flight_number	departure_date	departure_time	base_price flight_status ID departure_code	arrival_code
-- Jet Blue	     10001	        2024-12-30	    10:00:00	    1250	   on time	     1	LBJ1969	        XJP2020
-- Jet Blue	     10002	        2025-01-22	    11:00:00	    700	       delayed	     2	XJP2020	        LBJ1969
-- Jet Blue	     10003	        2025-01-23	    12:00:00	    900	       on time	     3	LBJ1969	        XJP2020

-- Show all of the delayed flights in the system 
select *
from flight
where flight_status = 'delayed';
-- Results:
-- airline_name	 flight_number	departure_date	departure_time	base_price flight_status ID departure_code	arrival_code
-- Jet Blue	     10002	        2025-01-22	    11:00:00	    700	       delayed	      2	 XJP2020	    LBJ1969

-- Show the customer names who bought the tickets
select distinct first_name, last_name
from ticket natural join customer;
-- Results:
-- first_name	last_name
-- Devin	    Booker
-- James	    Harden
-- Kevin	    Durant
-- Russell	    Westbrook

-- Show all the airplanes owned by the airline Jet Blue
select *
from airplane
where airline_name = 'Jet Blue';
-- Results
-- airline_name	seats manufacturer model manufacture_date
-- Jet Blue	    126	  Boeing	   737	 1994-05-05
-- Jet Blue	    375	  Boeing	   767	 2018-06-20
-- Jet Blue	    550	  Boeing	   777	 2021-03-10
-- Jet Blue	    330	  Boeing	   787	 2016-03-10