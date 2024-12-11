from flask import render_template, session, request, redirect, url_for
from app.customer import customer_blueprint
from app.db_conn import conn
import datetime
from collections import defaultdict
from functools import wraps

####################
# HELPER FUNCTIONS #
####################

"""
return number of tickets solds already for a flight
"""
def get_purchased_tickets(airline_name, flight_number, departure_date, departure_time):
    cursor = conn.cursor()
    count_purchased_tickets = """
        SELECT count(code) as count FROM ticket NATURAL JOIN flight
        WHERE airline_name = %s AND
                flight_number = %s AND
                departure_date = %s AND
                departure_time = %s
    """
    cursor.execute(count_purchased_tickets, (airline_name, flight_number, departure_date, departure_time))
    num_tickets = cursor.fetchone()
    cursor.close()

    return num_tickets['count']

"""
get seats a plane can have
"""
def get_plane_capacity(airline_name, flight_number, departure_date, departure_time):
    cursor = conn.cursor()
    check_capacity = """
        SELECT seats FROM flight NATURAL JOIN airplane
        WHERE airline_name = %s AND 
                flight_number = %s AND
                departure_date = %s AND
                departure_time = %s
        
    """
    cursor.execute(check_capacity, (airline_name, flight_number, departure_date, departure_time))
    total_seats = cursor.fetchone()
    cursor.close()

    return total_seats['seats']

"""
helper function to get number of available seats on a flight
"""
def get_available_seats(airline_name, flight_number, departure_date, departure_time):
    return get_plane_capacity(airline_name, flight_number, departure_date, departure_time) - get_purchased_tickets(airline_name, flight_number, departure_date, departure_time)

"""
calculate the price of ticket based on seats and capacity
"""
def get_price(airline_name, flight_number, departure_date, departure_time):
    plane_capacity = get_plane_capacity(airline_name, flight_number, departure_date, departure_time)
    capacity_left_percent = get_available_seats(airline_name, flight_number, departure_date, departure_time) / plane_capacity if plane_capacity != 0 else 0

    base_price_query = """
        SELECT base_price FROM flight
        WHERE airline_name = %s AND
                flight_number = %s AND
                departure_date = %s AND
                departure_time = %s
    """
    cursor = conn.cursor()
    cursor.execute(base_price_query, (airline_name, flight_number, departure_date, departure_time))
    base_price = float(cursor.fetchone()['base_price'])
    cursor.close()

    if capacity_left_percent <= 0.3:
        base_price += 0.25 * base_price

    return base_price

"""
determine whether user is logged in as customer
"""
def is_logged_in():
    return 'username' in session and 'role' in session and session['role'] == 'customer'

"""
get a user's ticket info from code
returns the data obj returned from cursor.fetchone()
"""
def get_ticket_from_code(code):
    query = """
        SELECT * FROM ticket NATURAL JOIN flight
        WHERE code = %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (code))
    data = cursor.fetchone()
    cursor.close()

    return data

##################################
# ROUTING/PAGE/HANDLER FUNCTIONS #
##################################

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
route for the customer home page
"""
@customer_blueprint.route('/')
@customer_protected_wrapper
def customer_home():
    # the user is not logged in
    # redirect them
    #if not is_logged_in():
    #    return redirect(url_for("default.login_page"))
    
    return render_template('customer/index.html')

"""
Display a customer's purchased flights for future.
"""
@customer_blueprint.route('/viewflights')
@customer_protected_wrapper
def customer_view_flights():
    # the user is not logged in
    # redirect them
    # if not is_logged_in():
    #     return redirect(url_for("default.login_page"))

    query = 'SELECT * FROM flight NATURAL JOIN ticket WHERE customer_email = %s AND TIMESTAMP(departure_date, departure_time) > NOW()'
    cursor = conn.cursor()
    cursor.execute(query, (session['username']))
    data = cursor.fetchall()
    cursor.close()
    return render_template('customer/viewflights.html', data = data, all=False)

"""
Display a customer's purchased flights for all purchased
"""
@customer_blueprint.route('/viewallflights')
@customer_protected_wrapper
def customer_view_flights_all():
    # the user is not logged in
    # redirect them
    # if not is_logged_in():
    #     return redirect(url_for("default.login_page"))

    query = 'SELECT * FROM flight NATURAL JOIN ticket WHERE customer_email = %s'
    cursor = conn.cursor()
    cursor.execute(query, (session['username']))
    data = cursor.fetchall()
    cursor.close()
    return render_template('customer/viewflights.html', data = data, all=True)

"""
Display search page
"""
@customer_blueprint.route('/search')
def customer_search():
    error = request.args.get('error')
    return render_template('customer/search.html', error=error)

"""
Display search results
"""
@customer_blueprint.route('/searchflights', methods=['GET', 'POST'])
def customer_search_results():
    values = (
        request.form['src-airport'],
        request.form['dst-airport'],
        request.form['departure-date'],
        request.form.get('return-date')
    )

    # true if the return date field has input in the form
    is_round_trip = values[-1] != ''

    query_dest_flights = 'SELECT * FROM flight NATURAL JOIN airplane WHERE departure_code = %s AND arrival_code = %s AND departure_date = %s'
    query_return_flights = 'SELECT * FROM flight NATURAL JOIN airplane WHERE arrival_code = %s AND departure_code = %s AND departure_date = %s'
    
    cursor = conn.cursor()
    cursor.execute(query_dest_flights, (values[0], values[1], values[2]))
    dest_data = cursor.fetchall()

    # get return flights if needed
    return_data = []
    if is_round_trip:
        cursor.execute(query_return_flights, (values[0], values[1], values[3]))
        return_data = cursor.fetchall()
    
    cursor.close()

    for flight in dest_data:
        seats = get_available_seats(flight['airline_name'], flight['flight_number'], flight['departure_date'], flight['departure_time'])
        flight['capacity'] = seats
        
        """
        if seats <= 0:
            return render_template('customer/searchresults.html', dest_data=dest_data, return_data=return_data, round_trip=is_round_trip, error="One or more selected flights are full")
        """
    
    for flight in return_data:
        seats = get_available_seats(flight['airline_name'], flight['flight_number'], flight['departure_date'], flight['departure_time'])
        flight['capacity'] = seats
        
        """"
        if seats <= 0:
            return render_template('customer/searchresults.html', dest_data=dest_data, return_data=return_data, round_trip=is_round_trip, error="One or more selected flights are full")
        """

    return render_template('customer/searchresults.html', dest_data=dest_data, return_data=return_data, round_trip=is_round_trip)

"""
Display the search page to search for flights
"""
@customer_blueprint.route('/purchase')
@customer_protected_wrapper
def customer_purchase():
    # the user is not logged in
    # redirect them
    # if not is_logged_in():
    #     return redirect(url_for("default.login_page"))
    
    return render_template('customer/search.html')

"""
Page to allow users to enter info (credit card, name, etc)
"""
@customer_blueprint.route('/purchasing-ticket-info', methods=['GET', 'POST'])
@customer_protected_wrapper
def customer_purchasing_ticket_info():
    # the user is not logged in
    # redirect them
    # if not is_logged_in():
    #     return redirect(url_for("default.login_page"))
    
    selected_flights = request.form.getlist('flights')
    flights = []

    # the customer did not select a flight to purchase
    if len(selected_flights) == 0:
        return redirect(url_for('customer.customer_search', error="No flights were selected"))

    cursor = conn.cursor()
    future_flight_check_query = """
        SELECT * FROM flight
        WHERE airline_name = %s AND
                flight_number = %s AND
                departure_date = %s AND
                departure_time = %s AND
                TIMESTAMP(departure_date, departure_time) > NOW();
    """
    # construct the flight list of dicts
    for f in selected_flights:
        airline_name, flight_number, departure_date, departure_time = f.split(',')
        
        # no seats available, cannot purchase this flight, redirect to search
        seats_available = get_available_seats(airline_name, flight_number, departure_date, departure_time)
        if seats_available <= 0:
            return redirect(url_for('customer.customer_search', error="One or more flights selected have no seats available"))
        
        # the flight is in the past
        # user cannot purchase past flights
        cursor.execute(future_flight_check_query, (airline_name, flight_number, departure_date, departure_time))
        data = cursor.fetchone()
        if not data:
            return redirect(url_for('customer.customer_search', error="One or more flights selected is in the past"))

        value = {}
        value['airline_name'] = airline_name
        value['flight_number'] = flight_number
        value['departure_date'] = departure_date
        value['departure_time'] = departure_time
        value['price'] = get_price(airline_name, flight_number, departure_date, departure_time)
        flights.append(value)
        
    return render_template('customer/purchasingticketinfo.html', flights=flights)

"""
logic to handle customer purchase submitted
"""
@customer_blueprint.route('/submitpurchase', methods=['GET', 'POST'])
@customer_protected_wrapper
def customer_submit_purchase():
    # the user is not logged in
    # redirect them
    # if not is_logged_in():
    #     return redirect(url_for("default.login_page"))

    form_info = request.form.items()
    flights = defaultdict(dict)

    # create dictionary of flights and their respective passenger info
    for k, v in form_info:
        if k in ["email", "type", "card-number", "card-name", "card-expiration"]:
            continue
        flight_data, info_type = k.split('/')
        airline_name, flight_number, departure_date, departure_time = flight_data.split(',')
        
        # check to ensure there are seats available
        # in theory we should never get to this point if the user does not act maliciously
        capacity = get_available_seats(airline_name, flight_number, departure_date, departure_time)
        if capacity <= 0:
            return redirect(url_for("customer.customer_home"))
        
        f = flights[(airline_name, flight_number, departure_date, departure_time)]
        f[info_type] = v

    # get payment info
    email = session['username']
    type = request.form['type']
    card_number = request.form['card-number']
    card_name = request.form['card-name']
    card_expiration = request.form['card-expiration']

    cursor = conn.cursor()
    # insert data into the database
    for k, v in flights.items():
        first_name = v['first_name']
        last_name = v['last_name']
        date_of_birth = v['date_of_birth']
        airline_name = k[0]
        flight_number = k[1]
        departure_date = k[2]
        departure_time = k[3]
        card_type = type
        purchase_date_time = datetime.datetime.now()
        name_on_card = card_name
        expiration_date = card_expiration
        customer_email = email
        sold_price = get_price(airline_name, flight_number, departure_date, departure_time)
        query = f'INSERT INTO ticket (first_name, last_name, date_of_birth, airline_name, flight_number, departure_date, departure_time, card_type, purchase_date_time, card_number, name_on_card, expiration_date, customer_email, sold_price) values ("{first_name}", "{last_name}", "{date_of_birth}", "{airline_name}", {flight_number}, "{departure_date}", "{departure_time}", "{card_type}", "{purchase_date_time}", {card_number}, "{name_on_card}", "{expiration_date}", "{customer_email}", {sold_price})'
        cursor.execute(query)
        conn.commit()
    cursor.close()
    
    return redirect(url_for("customer.customer_home"))

"""
page for customers to cancel their flights
"""
@customer_blueprint.route('/cancel')
@customer_protected_wrapper
def customer_cancel():
    # user is not logged in
    # if not is_logged_in():
    #     return redirect(url_for("default.login_page"))

    query = 'SELECT * FROM flight NATURAL JOIN ticket WHERE customer_email = %s AND TIMESTAMP(departure_date, departure_time) > (NOW() + INTERVAL 1 DAY);'
    cursor = conn.cursor()
    cursor.execute(query, (session['username']))
    data = cursor.fetchall()
    cursor.close()

    return render_template('customer/cancel.html', data=data)

"""
logic to handle customer cancel a flight
"""
@customer_blueprint.route('/submitcancel', methods=['GET', 'POST'])
@customer_protected_wrapper
def customer_submit_cancel():
    # the user is not logged in
    # redirect them
    # if not is_logged_in():
    #     return redirect(url_for("default.login_page"))

    form_info = request.form.getlist('cancel')
    tickets_to_cancel = []
    query = 'SELECT * FROM flight NATURAL JOIN ticket WHERE code = %s AND customer_email = %s AND TIMESTAMP(departure_date + departure_time) > (NOW() + INTERVAL 1 DAY);'

    # parse the form submission and
    # ensure selected tickets can be canceled by this user
    cursor = conn.cursor()
    for ticket_code in form_info:
        cursor.execute(query, (ticket_code, session['username']))
        data = cursor.fetchone()
        if data:
            tickets_to_cancel.append(data)

    # delete data from the database
    cancel_query = 'DELETE FROM ticket WHERE code = %s'
    for ticket in tickets_to_cancel:
        cursor.execute(cancel_query, (ticket['code']))
        conn.commit()
    cursor.close()
    
    return redirect(url_for("customer.customer_home"))

"""
render the rate and comment page
"""
@customer_blueprint.route('/ratecomment')
@customer_protected_wrapper
def customer_ratecomment():
    # user is not logged in
    # if not is_logged_in():
    #     return redirect(url_for("default.login_page"))

    # get all flights
    query = 'SELECT * FROM flight NATURAL JOIN ticket WHERE customer_email = %s AND TIMESTAMP(arrival_date, arrival_time) < (NOW());'
    cursor = conn.cursor()
    cursor.execute(query, (session['username']))
    data = cursor.fetchall()

    # get all comments
    comment_query = f'''SELECT * FROM takes WHERE customer_email = "{session['username']}"'''
    cursor.execute(comment_query)
    existing_comments = cursor.fetchall()
    flights_with_comments = set()
    for element in existing_comments:
        flights_with_comments.add((element['airline_name'], element['flight_number'], element['departure_date'], element['departure_time']))
    cursor.close()

    return render_template('customer/ratecomment.html', data=data, flights_with_comments=flights_with_comments)

"""
render the rate page for a single flight/ticket
"""
@customer_blueprint.route('/ratecomment/<int:ticket_id>')
@customer_protected_wrapper
def customer_rate_flight(ticket_id):
    # user is not logged in
    # if not is_logged_in():
    #     return redirect(url_for("default.login_page"))
    
    query = f'SELECT * FROM ticket NATURAL JOIN flight WHERE code = {ticket_id}'
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchone()
    cursor.close()

    return render_template('customer/ratecommentpage.html', flight=data)

"""
render the rate page for viewing a single flight/ticket comment
"""
@customer_blueprint.route('/viewratecomment/<int:ticket_id>')
@customer_protected_wrapper
def customer_view_rate_flight(ticket_id):
    # user is not logged in
    # if not is_logged_in():
    #     return redirect(url_for("default.login_page"))
    
    query = f'SELECT * FROM ticket NATURAL JOIN takes WHERE code = {ticket_id}'
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchone()
    cursor.close()

    return render_template('customer/viewratecommentpage.html', comment=data)

"""
submit a rating
"""
@customer_blueprint.route('/submitrating/<int:ticket_id>', methods=['GET', 'POST'])
@customer_protected_wrapper
def customer_rate_submit_handler(ticket_id):
    # user is not logged in
    # if not is_logged_in():
    #     return redirect(url_for("default.login_page"))
    
    # get flight info associated with ticket
    query = f'SELECT * FROM ticket NATURAL JOIN flight WHERE code = {ticket_id}'
    cursor = conn.cursor()
    cursor.execute(query)
    flight_data = cursor.fetchone()

    # data needed to insert
    customer_email = session['username']
    airline_name = flight_data['airline_name']
    flight_number = flight_data['flight_number']
    departure_date = flight_data['departure_date']
    departure_time = flight_data['departure_time']
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    
    # insert the data
    insert_query = f'INSERT INTO takes VALUES ("{customer_email}", "{airline_name}", {flight_number}, "{departure_date}", "{departure_time}", "{comment}", {rating})'
    cursor.execute(insert_query)
    conn.commit()

    cursor.close()

    return redirect(url_for('customer.customer_home'))

"""
render the default tracking page
"""
@customer_blueprint.route('/track')
@customer_protected_wrapper
def customer_track():
    money_spent_past_year_query = f'''SELECT SUM(sold_price) as total FROM ticket WHERE customer_email = "{session['username']}" AND purchase_date_time >= (NOW() - INTERVAL 1 YEAR)'''
    monthly_spending_query = f'''SELECT MONTH(purchase_date_time) as month, YEAR(purchase_date_time) as year, SUM(sold_price) as total FROM ticket WHERE customer_email = "{session['username']}" AND purchase_date_time >= (MONTH(NOW() - INTERVAL 6 MONTH)) GROUP BY MONTH(purchase_date_time), YEAR(purchase_date_time)'''

    # get data
    cursor = conn.cursor()
    cursor.execute(money_spent_past_year_query)
    yearly = cursor.fetchone()
    cursor.execute(monthly_spending_query)
    monthly = cursor.fetchall()
    cursor.close()

    # prepare dictionary of month:spending
    monthly_spending = {}
    today = datetime.datetime.now()
    for _ in range(6, 0, -1):
        monthly_spending[(today.strftime("%B"), today.strftime("%Y"))] = 0
        # this works since we are setting the day to the first
        # of each month and then subtracting by 1 day, 
        # which gives us the previous month
        today = today.replace(day=1) - datetime.timedelta(days=1)
    for item in monthly:
        print(item)
        m, spending, year = item['month'], item['total'], item['year']
        str_month = datetime.date(2024, int(m), 1).strftime("%B")
        if (str_month, str(year)) not in monthly_spending:
            continue
        monthly_spending[(str_month, str(year))] = spending if spending else 0
    prepared_monthly = []
    for k, v in monthly_spending.items():
        prepared_monthly.append([k, v])

    return render_template('customer/track.html', yearly=yearly['total'] if yearly['total'] else 0, monthly=prepared_monthly)

"""
render page for a tracking range
"""
@customer_blueprint.route('/trackrange', methods=['GET', 'POST'])
@customer_protected_wrapper
def customer_track_range():
    start_date = request.form['start']
    end_date = request.form['end']

    monthly_spending_query = f'''SELECT MONTH(purchase_date_time) as month, YEAR(purchase_date_time) as year, SUM(sold_price) as total FROM ticket WHERE customer_email = "{session['username']}" AND purchase_date_time >= TIMESTAMP("{start_date}") AND purchase_date_time <= TIMESTAMP("{end_date}") GROUP BY MONTH(purchase_date_time), YEAR(purchase_date_time)'''
    cursor = conn.cursor()
    cursor.execute(monthly_spending_query)
    data = cursor.fetchall()
    cursor.close()

    # prepare dictionary of month:spending
    monthly_spending = {}
    # we will propagate the dict with zeros first so they show up
    # we loop through time
    # the while condition ensures we stay in the range
    today = datetime.datetime.now().replace(day=1)
    while today.date() >= datetime.datetime.strptime(start_date, '%Y-%m-%d').date() or (today.date() < datetime.datetime.strptime(start_date, '%Y-%m-%d').date() and today.month == datetime.datetime.strptime(start_date, '%Y-%m-%d').month):
        monthly_spending[(today.strftime("%B"), today.year)] = 0
        # this works since we are setting the day to the first
        # of each month and then subtracting by 1 day, 
        # which gives us the previous month
        today = today.replace(day=1) - datetime.timedelta(days=1)
    # go through the data from database and assign actual values to the dict
    for item in sorted(data, key=lambda x: (-int(x['year']), -(x['month']))):
        month_numeric = item['month']
        year_numeric = item['year']
        total = item['total']
        month_string = datetime.date(2024, int(month_numeric), 1).strftime("%B")
        monthly_spending[(month_string, year_numeric)] = total
    prepared_monthly = []
    for k, v in monthly_spending.items():
        prepared_monthly.append([k[0], k[1], v])

    return render_template('customer/trackrange.html', monthly=prepared_monthly, range_start=start_date, range_end=end_date)