from flask import render_template, request, session, url_for, redirect
from app.default import default_blueprint
from hashlib import md5
from app.db_conn import conn

"""
session['username'] contains the user's username
session['role'] is either 'customer' or 'staff', used to distinguish user type
"""

"""
Landing page
"""
@default_blueprint.route('/')
def landing_page():
    return render_template('default/index.html')

"""
Login Page
"""
@default_blueprint.route('/login')
def login_page():
    return render_template('default/login.html')

"""
Catch All LoginAuth
"""
@default_blueprint.route('/loginAuth', methods=['GET', 'POST'])
def login_auth():
    # get username password from form
    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    login_type = request.form['type']

    cursor = conn.cursor()
    
    customer_or_staff = 0 # 0 for customer, staff otherwise
    data = None
    if login_type == 'customer':
        # check against username, md5(password) database
        query = 'SELECT * FROM customer WHERE customer_email = %s AND customer_password = %s'
        cursor.execute(query, (username, md5(password).hexdigest()))
        data = cursor.fetchone()
    else:
        query = 'SELECT * FROM staff WHERE username = %s AND staff_password = %s'
        cursor.execute(query, (username, md5(password).hexdigest()))
        data = cursor.fetchone()
        if data:
            customer_or_staff = 1
    
    cursor.close()
    error = None

    if data:
        session['username'] = username
        session['role'] = 'customer' if not customer_or_staff else 'staff' # store role of user
        return redirect('customer/') if not customer_or_staff else redirect('staff/')
    else:
        error = 'Invalid login'
        return render_template('default/login.html', error=error)

"""
Customer Registration Page
"""
@default_blueprint.route('/register')
def register_page_customer():
    return render_template('default/register.html')

"""
Staff Registration Page
"""
@default_blueprint.route('/registerstaff')
def register_page_staff():
    return render_template('default/registerstaff.html')

"""
Registration logic for customers
"""
@default_blueprint.route('/registerAuthCustomer', methods=['GET', 'POST'])
def register_auth():
    values = (
        request.form['email'],
        md5(request.form['password'].encode('utf-8')).hexdigest(),
        request.form['first_name'],
        request.form['last_name'],
        request.form['addr_building_number'],
        request.form['addr_street'],
        request.form['addr_apartment_number'],
        request.form['addr_city'],
        request.form['addr_state'],
        request.form['zip'],
        request.form['passport_number'],
        request.form['passport_expiration'],
        request.form['passport_country'],
        request.form['date_of_birth'],
    )
    phone_numbers_input = request.form['phone_numbers'].split(',')
    numbers = [p.strip() for p in phone_numbers_input]

    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM customer WHERE customer_email = %s'
    cursor.execute(query, values[0])
    data = cursor.fetchone()
    error = None

    if data:
        error = "This user already exists"
        cursor.close()
        return render_template('default/register.html', error = error)
    else:
        ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, values)
        ins_phone_numbers = 'INSERT INTO customer_phone_number VALUES (%s, %s)'
        for p in numbers:
            cursor.execute(ins_phone_numbers, (values[0], p))
        conn.commit()
        cursor.close()
        return render_template('/default/index.html')

"""
Registration logic for staff
"""
@default_blueprint.route('/registerAuthStaff', methods=['GET', 'POST'])
def register_auth_staff():
    values = (
        request.form['email'],
        md5(request.form['password'].encode('utf-8')).hexdigest(),
        request.form['first_name'],
        request.form['last_name'],
        request.form['date_of_birth'],
        request.form['airline_name']
    )
    phone_numbers_input = request.form['phone_numbers'].split(',')
    numbers = [p.strip() for p in phone_numbers_input]
    emails_input = request.form['email_addresses'].split(',')
    emails = [e.strip() for e in emails_input]

    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM staff WHERE username = %s'
    cursor.execute(query, values[0])
    data = cursor.fetchone()
    error = None

    if data:
        error = "This user already exists"
        return render_template('default/register.html', error = error)
    else:
        # we need to validate the airline foreign key dependency
        validate_airline_query = "SELECT * FROM airline WHERE airline_name = %s"
        cursor.execute(validate_airline_query, values[-1])
        data = cursor.fetchone()
        if not data:
            error = "Airline does not exist"
            cursor.close()
            return render_template('default/registerstaff.html', error = error)
        else:
            ins = 'INSERT INTO staff VALUES(%s, %s, %s, %s, %s, %s)'
            ins_emails = 'INSERT INTO staff_Email VALUES(%s, %s)'
            ins_phone_numbers = 'INSERT INTO staff_Phone_Number VALUES (%s, %s)'
            cursor.execute(ins, values)
            for p in numbers:
                cursor.execute(ins_phone_numbers, (values[0], p))
            for e in emails:
                cursor.execute(ins_emails, (values[0], e))
            conn.commit()
            cursor.close()
            return render_template('/default/index.html')

"""
Logout Logic
"""
@default_blueprint.route('/logout', methods=['GET', 'POST'])
def logout_auth():
    session['role'] = None
    session['username'] = None
    return render_template('/default/login.html')

"""
View Pubic Info Search Page
"""
@default_blueprint.route('/viewpublicinfo')
def view_public_info_page():
    return render_template('default/viewpublicinfo.html')

"""
Search Results for A Flight
"""
@default_blueprint.route('/searchflights', methods=['GET', 'POST'])
def search_results_page():
    values = (
        request.form['src-airport'],
        request.form['dst-airport'],
        request.form['departure-date'],
        request.form.get('return-date')
    )

    # true if the return date field has input in the form
    is_round_trip = values[-1] != ''

    query_dest_flights = 'SELECT * FROM flight WHERE departure_code = %s AND arrival_code = %s AND departure_date = %s'
    query_return_flights = 'SELECT * FROM flight WHERE arrival_code = %s AND departure_code = %s AND departure_date = %s'
    
    cursor = conn.cursor()
    cursor.execute(query_dest_flights, (values[0], values[1], values[2]))
    dest_data = cursor.fetchall()

    # get return flights if needed
    return_data = None
    if is_round_trip:
        cursor.execute(query_return_flights, (values[0], values[1], values[3]))
        return_data = cursor.fetchall()
    
    cursor.close()

    return render_template('default/searchresults.html', dest_data=dest_data, return_data=return_data, round_trip=is_round_trip)
