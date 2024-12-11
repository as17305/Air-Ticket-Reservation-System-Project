from flask import render_template, request, session, redirect, url_for
from app.staff import staff_blueprint
from app.db_conn import conn
from datetime import datetime, timedelta, time
from functools import wraps

"""
get staff username and airline name
"""
def getStaffInfo():
    cursor = conn.cursor()
    cursor.execute('select airline_name from staff where username = %s', (session['username'],))
    result = cursor.fetchone()
    cursor.close()
    return session['username'], result['airline_name']

""" 
get people on flights
"""
def getFlightInfo(flights):
    cursor = conn.cursor()
    flight_details = []
    for flight in flights:
        flight_number = flight['flight_number']
        cursor.execute("""
            select customer.customer_email, customer.first_name, customer.last_name, customer.date_of_birth
            from customer join ticket on ticket.customer_email = customer.customer_email
            where ticket.flight_number = %s
        """, (flight_number,))
        customers = cursor.fetchall()
        flight_details.append({
            'flight': flight,
            'customers': customers
        })
    cursor.close()
    return flight_details

"""
determine whether user is logged in as customer
"""
def is_logged_in():
    return 'username' in session and 'role' in session and session['role'] == 'staff'

"""
wrapper for authentication
"""
def customer_protected_wrapper(route):
    @wraps(route)
    def protected(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for("default.login_page"))
        return route(*args, **kwargs)
    return protected

"""
route for the staff home page
"""
@staff_blueprint.route('/')
@customer_protected_wrapper
def customer_home():
    return render_template('staff/index.html')

"""
Display Flight Information
"""
@staff_blueprint.route('/viewflights', methods=['GET', 'POST'])
@customer_protected_wrapper
def staff_view_flights():
    # Default shows flights for next 30 days
    username, airline_name = getStaffInfo()
    today = datetime.today()
    thirtyDays = today + timedelta(days=30)
    query = "select * from flight where airline_name = %s and departure_date >= %s and departure_date <= %s"
    flights = None
    flight_details = None
    source_airport = None
    destination_airport = None
    start_date = None
    end_date = None

    cursor = conn.cursor()
    # Show flights for the next thirty days a default
    cursor.execute(query, [airline_name, today, thirtyDays])
    defaultFlights = cursor.fetchall()
    default_flight_details = getFlightInfo(defaultFlights)

    # Get valid airport codes for form dropdown
    cursor.execute("select code from airport")
    airport_codes = [row["code"] for row in cursor.fetchall()]
    cursor.close()

    # Optional Flights Filter
    if request.method == 'POST':
        cursor = conn.cursor()
        try:
            source_airport = request.form.get('departure_code')
            destination_airport = request.form.get('arrival_code')
            start_date = request.form.get('departure_date')
            end_date = request.form.get('max_departure_date')
            data = [airline_name, start_date, end_date]
            if source_airport:
                query += " and departure_code = %s"
                data.append(source_airport)

            if destination_airport:
                query += " and arrival_code = %s"
                data.append(destination_airport)

            cursor.execute(query, data)
            flights = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            cursor.close()

    # Get customer details for each flight
    if flights is not None:
        flight_details = getFlightInfo(flights)
    return render_template('staff/viewflights.html', flight_details=flight_details, default_flight_details = default_flight_details, source_airport=source_airport, destination_airport=destination_airport, start_date=start_date, end_date=end_date, airport_codes=airport_codes)

"""
Create New Flight
"""
@staff_blueprint.route('/createflight', methods=['GET', 'POST'])
@customer_protected_wrapper
def staff_create_flight():
    message = ""
    airline_name = getStaffInfo()[1]
    if request.method == 'POST':
        cursor = conn.cursor()
        try:
            # Get values
            flight_number = request.form['flight_number']
            departure_date = request.form['departure_date']
            departure_time = request.form['departure_time']
            arrival_date = request.form['arrival_date']
            arrival_time = request.form['arrival_time']
            base_price = request.form['base_price']
            flight_status = request.form['flight_status']
            flight_id = request.form['ID']
            departure_code = request.form['departure_code']
            arrival_code = request.form['arrival_code']

            # Combine date and time
            flight_departure_datetime = datetime.strptime(departure_date + " " + departure_time, '%Y-%m-%d %H:%M')
            flight_arrival_datetime = datetime.strptime(arrival_date + " " + arrival_time, '%Y-%m-%d %H:%M')

            # Check if the arrival is before departure
            if flight_arrival_datetime < flight_departure_datetime:
                raise Exception("Arrival can't be before departure")
            
            # Plane can't be under maintenance
            cursor.execute("select maintenance_start_date,maintenance_start_time, maintenance_end_date, maintenance_end_time from maintenance_procedures where airline_name = %s and ID = %s", (airline_name, flight_id))
            maintenance_info = cursor.fetchone()

            if maintenance_info:
                maintenance_start = datetime.combine(maintenance_info['maintenance_start_date'], 
                                                    time(maintenance_info['maintenance_start_time'].seconds // 3600, 
                                                        (maintenance_info['maintenance_start_time'].seconds % 3600) // 60))

                maintenance_end = datetime.combine(maintenance_info['maintenance_end_date'], 
                                                time(maintenance_info['maintenance_end_time'].seconds // 3600, 
                                                        (maintenance_info['maintenance_end_time'].seconds % 3600) // 60))
                if maintenance_start <= flight_departure_datetime <= maintenance_end or maintenance_start <= flight_arrival_datetime <= maintenance_end:
                    raise Exception("Airplane is under maintenance during the requested flight time.")
            
            # Insert into the database
            cursor.execute("insert into flight values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                airline_name, flight_number, departure_date, departure_time,
                arrival_date, arrival_time, base_price, flight_status, flight_id,
                departure_code, arrival_code))

            # Commit the transaction
            conn.commit()
            cursor.close()

            # Show success message
            message = "Flight created successfully!"
        except Exception as e:
            print(e)
            conn.rollback()
            cursor.close()
            message = "An error occurred"

   # Retrieve valid values for form dropdown
    cursor = conn.cursor()

    # Default flights for next 30 days
    today = datetime.today()
    thirtyDays = today + timedelta(days=30)
    cursor.execute("select * from flight where airline_name = %s and departure_date >= %s and departure_date <= %s", (airline_name, today, thirtyDays))
    default = cursor.fetchall()

    # Get valid airport codes
    cursor.execute("select code from airport")
    airport_codes = [row["code"] for row in cursor.fetchall()]

    # Get valid airplane IDs
    cursor.execute("select ID from airplane")
    airplane_ids = [row["ID"] for row in cursor.fetchall()]

    flight_statuses = ['delayed', 'on time', 'canceled']  # Possible flight statuses
    
    cursor.close()

    # Render the template with the message, data, and dropdowns
    return render_template('staff/createflight.html', message=message, airport_codes=airport_codes, flight_statuses=flight_statuses, airplane_ids=airplane_ids, default=default)

"""
Update Flight Status
"""
@staff_blueprint.route('updateflightstatus', methods=['GET', 'POST'])
@customer_protected_wrapper
def staff_update_flight_status():
    message = ""
    airline_name = getStaffInfo()[1]
    if request.method == 'POST':
        cursor = conn.cursor()
        try:
            # Get values
            flight_number = request.form['flight_number']
            departure_date = request.form['departure_date']
            departure_time = request.form['departure_time']
            new_status = request.form['new_status']
            # Update database
            cursor.execute("update flight set flight_status = %s where airline_name = %s and flight_number = %s and departure_date = %s and departure_time = %s", (new_status, airline_name, flight_number, departure_date, departure_time))

            # Check if any rows were updated
            if cursor.rowcount == 0:
                message = "No matching flight found to update or flight status was not changed!"
            else:
                conn.commit()
                message = "Flight Status Updated"

            cursor.close()
        except Exception as e:
            print(e)
            conn.rollback()
            cursor.close()
            message = "An error occurred!"    
    return render_template('staff/updateflightstatus.html', message=message)

"""
Add airplane
"""
@staff_blueprint.route('addairplane', methods=['GET', 'POST'])
@customer_protected_wrapper
def staff_add_airplane():
    message = ""
    airplanes = []
    
    airline_name = getStaffInfo()[1]
    if request.method == 'POST':
        cursor = conn.cursor()
        try:
            # Get values
            flight_id = request.form['ID']
            seats = request.form['seats']
            manufacturer = request.form['manufacturer']
            model = request.form['model']
            manufacture_date = request.form['manufacture_date']
            
            # Insert the new airplane into the database
            cursor.execute("insert into airplane values (%s, %s, %s, %s, %s, %s)", (flight_id, airline_name, seats, manufacturer, model, manufacture_date))
            conn.commit()
            cursor.close()
            message = "Airplane added successfully!"
        except Exception as e:
            print(e)
            conn.rollback()
            cursor.close()
            message = "An error occurred"
    # Fetch all airplanes for the airline
    cursor = conn.cursor()
    cursor.execute("select ID, manufacturer, model, seats, manufacture_date from airplane where airline_name = %s", (airline_name,))
    airplanes = cursor.fetchall()
    cursor.close()
    return render_template('staff/addairplane.html', message=message, airplanes=airplanes, airline_name=airline_name)


"""
Add airport
"""
@staff_blueprint.route('addairport', methods=['GET', 'POST'])
@customer_protected_wrapper
def staff_add_airport():
    message = ""
    if request.method == 'POST':
        cursor = conn.cursor()
        try:
            # Get values
            code = request.form['code']
            airport_name = request.form['airport_name']
            city = request.form['city']
            country = request.form['country']
            number_of_terminals = request.form['number_of_terminals']
            airport_type = request.form['airport_type']
            
            # Insert the new airport into the database
            cursor.execute("insert into airport values (%s, %s, %s, %s, %s, %s)", (code, airport_name, city, country, number_of_terminals, airport_type))
            conn.commit()
            cursor.close()
            message = "Airport added successfully!"
        except Exception as e:
            print(e)
            conn.rollback()
            cursor.close()
            message = "An error occurred"
    return render_template('staff/addairport.html', message=message)


"""
View Flight Rating
"""
@staff_blueprint.route('viewflightrating', methods=['GET', 'POST'])
@customer_protected_wrapper
def staff_view_flight_rating():
    # Get values for flight
    airline_name = getStaffInfo()[1]
    flight_number = request.form.get('flight_number')
    departure_date = request.form.get('departure_date')
    departure_time = request.form.get('departure_time')
    cursor = conn.cursor()
    # Get ratings and comments for a flight
    cursor.execute("select rating, comment from takes where airline_name = %s and flight_number = %s and departure_date = %s and departure_time = %s", (airline_name, flight_number, departure_date, departure_time))
    data = cursor.fetchall()
    cursor.execute("select avg(rating) as value from takes where airline_name = %s and flight_number = %s and departure_date = %s and departure_time = %s", (airline_name, flight_number, departure_date, departure_time))
    avgRating = cursor.fetchone()
    cursor.close()
    return render_template('staff/viewflightrating.html', data=data, avgRating=avgRating)

"""
Schedule Maintenance
"""
@staff_blueprint.route('schedulemaintenance', methods=['GET', 'POST'])
@customer_protected_wrapper
def staff_schedule_maintenance():
    message = ""
    if request.method == 'POST':
        cursor = conn.cursor()
        try:
            # Get values
            airline_name = getStaffInfo()[1]
            airplane_ID = request.form['ID']
            maintenance_start_date = request.form['maintenance_start_date']
            maintenance_start_time = request.form['maintenance_start_time']
            maintenance_end_date = request.form['maintenance_end_date']
            maintenance_end_time = request.form['maintenance_end_time']
            
            # Insert the new maintenance_procedures into the database
            cursor.execute("insert into maintenance_procedures values (%s, %s, %s, %s, %s, %s)", (airline_name, airplane_ID, maintenance_start_date, maintenance_start_time, maintenance_end_date, maintenance_end_time))
            conn.commit()
            cursor.close()
            message = "Maintenance Schedule was successfully added!"
        except Exception as e:
            print(e)
            conn.rollback()
            cursor.close()
            message = "An error occurred"
    return render_template('staff/schedulemaintenance.html', message=message)

"""
View Frequent Customer
"""
@staff_blueprint.route('viewfrequentcustomer', methods=['GET', 'POST'])
@customer_protected_wrapper
def staff_view_frequent_customer():
    airline_name = getStaffInfo()[1]
    one_year = datetime.today() - timedelta(days=365)
    cursor = conn.cursor()
    # Get most frequent customers
    cursor.execute("""
            select customer_email, count(*) as num_of_flights
            from ticket
            where airline_name = %s and purchase_date_time >= %s
            group by customer_email
            order by num_of_flights desc 
            limit 5""", (airline_name, one_year))
    frequent = cursor.fetchall()
    # Query for flights particular customer has taken
    customer_email = request.form.get('customer_email')
    cursor.execute("""select flight_number, departure_date, departure_time
                    from ticket
                    where airline_name = %s and customer_email = %s """, (airline_name, customer_email))
    flights = cursor.fetchall()
    cursor.close()
    return render_template('staff/viewfrequentcustomer.html', frequent=frequent, flights = flights, customer_email=customer_email)

"""
Earned Revenue
"""
@staff_blueprint.route('earnedrevenue', methods=['GET', 'POST'])
@customer_protected_wrapper
def staff_earned_revenue():
    airline_name = getStaffInfo()[1]
    today = datetime.today()
    last_month = today - timedelta(days=30)
    last_year = today - timedelta(days=365)

    cursor = conn.cursor()

    # Query for last month's revenue
    cursor.execute("""
        select sum(sold_price) as total_revenue_last_month
        from ticket
        where airline_name = %s and purchase_date_time >= %s""", (airline_name, last_month))
    revenue_last_month = cursor.fetchone()['total_revenue_last_month'] or 0

    # Query for last years's revenue
    cursor.execute("""
        select sum(sold_price) as total_revenue_last_year
        from ticket
        where airline_name = %s and purchase_date_time >= %s""", (airline_name, last_year))
    revenue_last_year = cursor.fetchone()['total_revenue_last_year'] or 0

    revenue_last_month = round(revenue_last_month, 2)
    revenue_last_year = round(revenue_last_year, 2)
    cursor.close()
    return render_template('staff/earnedrevenue.html', revenue_last_month=revenue_last_month, revenue_last_year=revenue_last_year)