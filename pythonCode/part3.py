#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 12:11:08 2018

@author: zhangyueying
"""

#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import datetime
import random

app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='192.168.64.2',
                       user='root',
                       password='',
                       db='airline',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

today = datetime.date.today()

@app.route('/')
def hello():
	return render_template('public_info.html')


#==============================================================================
# search flight based on city, airport, date (data not required)
# if city/airport missing, select all flights:
# if date missing, select flight departing today
#==============================================================================
@app.route('/public_info_check_flight', methods=['GET', 'POST'])
def public_info_check_flight():    
    # search upcoming flight
    source_city = request.form['source city']
    source_airport = request.form['source airport']
    des_city = request.form['destination city']
    des_airport = request.form['destination airport']
    date = request.form['date']
    # if date is empty, use today, search flights.departure_time = today
    if not date:
        date = today
    data_l = [source_city, des_city, source_airport, des_airport]
    data_l_revised = [i if (i.strip() != '') else None for i in data_l]
    data_l_revised.append('upcoming')
    data_l_revised.append(date)
    data_t = tuple(data_l_revised)
    cursor = conn.cursor()
    query = '''SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price
    FROM flight JOIN airport S ON S.airport_name = departure_airport JOIN airport T ON T.airport_name = arrival_airport
    WHERE S.airport_city = IFNULL(%s, S.airport_city) AND T.airport_city = IFNULL(%s, T.airport_city)
    AND departure_airport = IFNULL(%s, departure_airport) AND arrival_airport = IFNULL(%s, arrival_airport) 
    AND status = %s AND DATE(departure_time) = %s'''  
    cursor.execute(query, data_t)
    data = cursor.fetchall()
    cursor.close()
    if not data:
        error = 'no such flight'
        return render_template('public_info.html', error=error)
    else:
        return render_template('public_info.html', posts=data)


#==============================================================================
# check selected flight status
# flight_num is required
# date not required, if empty, selecting all flight whose flight_num = input    
#==============================================================================
@app.route('/public_info_check_status', methods=['GET','POST'])
def public_info_check_status():
    cursor = conn.cursor()
    flight_num = request.form['flight number']
    departure_date = request.form['departure date']
    arrival_date = request.form['arrival date']
    if not departure_date:
        departure_date = None
    if not arrival_date:
        arrival_date = None
    if not (flight_num):
        error = 'incomplete flight information'
        cursor.close()
        return render_template('public_info.html', error=error)
    else:
        query = '''SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, status
        FROM flight 
        WHERE flight_num = %s AND DATE(departure_time) = IFNULL(%s, DATE(departure_time))
        AND DATE(arrival_time) = IFNULL(%s, DATE(arrival_time))'''
        cursor.execute(query, (flight_num, departure_date, arrival_date))
        data = cursor.fetchall()
        cursor.close()
        if not (data):
            error = 'no such flight'
            return render_template('public_info.html', error=error)
        else:
            return render_template('public_info.html', post1=data)
        


'''
customer 
login and register
'''
#customer login and register
#==============================================================================
# customer login (all data required)
#==============================================================================
@app.route('/login_cus')
def login_cus():
	return render_template('login_cus.html')

#Authenticates the login
@app.route('/loginAuth_cus', methods=['GET', 'POST'])
def loginAuth_cus():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s AND password = MD5(%s)'
	cursor.execute(query, (email, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	if (data):
		#creates a session for the the user
		#session is a built in
		session['email1'] = email  
		return redirect(url_for('home_cus'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login_cus.html', error=error)


#==============================================================================
# customer register (all data required)
#==============================================================================
@app.route('/register_cus')
def register_cus():
	return render_template('register_cus.html')


@app.route('/registerAuth_cus', methods=['GET', 'POST'])
def registerAuth_cus():
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    building_num = request.form['building number']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone_num = request.form['phone number']
    passport_num = request.form['passport number']
    passport_date = request.form['passport expiration date']
    passport_country = request.form['passport country']
    dob = request.form['date of birth']
    
    cursor = conn.cursor()
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (email))
    data = cursor.fetchone()
    if (data):
        error = "This user already exists"
        cursor.close()
        return render_template('register_cus.html', error = error)
    else:
        ins = '''INSERT INTO customer 
        VALUES(%s, %s, MD5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(ins, (email, name, password, building_num, street, city, state, phone_num, passport_num,
                             passport_date, passport_country, dob))
        conn.commit()
        cursor.close()
        return render_template('login_cus.html')


#==============================================================================
# display all the upcoming flights starting from today of the customer
#==============================================================================
@app.route('/home_cus')
def home_cus():
    try: 
        email = session['email1']
    except:
        return redirect('/login_cus')

    cursor = conn.cursor()
    query = '''SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, status 
    FROM flight NATURAL JOIN ticket NATURAL JOIN purchases
    WHERE customer_email = %s AND status = %s AND DATE(departure_time) >= %s
    ORDER BY departure_time'''
    cursor.execute(query, (email, 'upcoming', today))
    data = cursor.fetchall()
    cursor.close()
    return render_template('home_cus.html', email=email, posts=data)


#==============================================================================
# search upcoming flights based on city, airprot, date (data not required)
# if no data for city/airport, select flights for all cities/airports:
# if no data for date, use today
#==============================================================================
@app.route('/search_flight_cus', methods=['GET'])
def search_flight_cus():
    try:
        email = session['email1']
        return render_template('search_flight_cus.html', email=email)
    except:
        return redirect('/login_cus')
 
       
@app.route('/search_flight_cus', methods=['POST'])
def search_flight_cus_Auth():
    try:
        email = session['email1']
    except:
        return redirect('/login_cus')
    
    source_city = request.form['source city']
    source_airport = request.form['source airport']
    des_city = request.form['destination city']
    des_airport = request.form['destination airport']
    date = request.form['date']
    # if date is empty, use today, search flights.departure_time = today
    if not date:
        date = today
    data_l = [source_city, des_city, source_airport, des_airport]
    data_l_revised = [i if (i.strip() != '') else None for i in data_l]
    data_l_revised.append('upcoming')
    data_l_revised.append(date)
    data_t = tuple(data_l_revised)
    cursor = conn.cursor()
    query = '''SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price
    FROM flight JOIN airport S ON S.airport_name = departure_airport JOIN airport T ON T.airport_name = arrival_airport
    WHERE S.airport_city = IFNULL(%s, S.airport_city) AND T.airport_city = IFNULL(%s, T.airport_city)
    AND departure_airport = IFNULL(%s, departure_airport) AND arrival_airport = IFNULL(%s, arrival_airport) 
    AND status = %s AND DATE(departure_time) = %s'''  
    cursor.execute(query, data_t)
    data = cursor.fetchall()
    cursor.close()
    if not data:
        error = 'no such flight'
        return render_template('search_flight_cus.html', email=email, error=error)
    else:
        return render_template('search_flight_cus.html', email=email, posts=data)


#==============================================================================
# booking agent purchase ticket for customers (all data required)
# 1. check if flight exists
# 2. check if enough seat left
#==============================================================================
@app.route('/purchase_ticket_cus', methods=['GET'])
def purchase_ticket_cus():
    try:
        email = session['email1']
        return render_template('purchase_ticket_cus.html', email=email)
    except:
        return redirect('/login_cus')
    
    
@app.route('/purchase_ticket_cus', methods=['POST'])
def purchase_ticket_cus_Auth():  
    try:
        email = session['email1']
    except:
        return redirect('/login_cus')
    
    ticket_id = None
    airline_name = request.form['airline name']
    flight_num = request.form['flight number']
    cursor = conn.cursor()
    #check if we have the upcoming flight
    check1 = '''SELECT * 
    FROM flight 
    WHERE airline_name = %s AND flight_num = %s AND status = %s'''
    cursor.execute(check1, (airline_name, flight_num, 'upcoming'))
    check_data1 = cursor.fetchall()
    if not (check_data1):
        error = 'no such upcoming flight'
        cursor.close()
        return render_template('purchase_ticket_cus.html', email=email, error=error)
    
    #check if has enough seat left
    ticket_num = '''SELECT COUNT(ticket_id) as sold
    FROM ticket
    WHERE airline_name = %s AND flight_num = %s'''
    cursor.execute(ticket_num, (airline_name, flight_num))
    ticket_sold = cursor.fetchone()
    seat = '''SELECT seats 
    FROM airplane NATURAL JOIN flight 
    WHERE flight.airline_name = %s AND flight_num = %s'''
    cursor.execute(seat, (airline_name, flight_num))
    seat_available = cursor.fetchone()
    if int(ticket_sold['sold']) >= int(seat_available['seats']):  
        error = 'the flight is full, find another flight'
        cursor.close()
        return render_template('purchase_ticket_cus.html', email=email, error=error)
    
    #pass all check          
    #generate unique ticket_id
    while True:
        ticket_id = int(random.randint(10,99999999))
        check2 = '''SELECT * FROM ticket WHERE ticket_id = %s '''
        cursor.execute(check2, ticket_id)
        check_data2 = cursor.fetchone()
        if not (check_data2):
            break
    ins2 = '''INSERT INTO ticket
    VALUES(%s, %s, %s)'''
    cursor.execute(ins2, (ticket_id, airline_name, flight_num))
    conn.commit()
    ins1 = '''INSERT INTO purchases
    VALUES(%s, %s, NULL, %s)'''
    cursor.execute(ins1, (ticket_id, email, today))
    conn.commit()
    cursor.close()
    message = 'Successful purchase'
    return render_template('purchase_ticket_cus.html', email=email, posts=message)
  
      
#==============================================================================
# track total spending of the customer (data not required)
# 1. total spending in the selected date
# 2. month-wise spending in the selected date (bar chart)
# if one of date_start and date_end missing:
# 1. display default: total spending in the past year  
# 2. display default: year-month spending in the past half year
#==============================================================================
@app.route('/track_spending_cus')
def track_spending_cus():
    try:
        email = session['email1']
        return render_template('/track_spending_cus.html', email=email)
    except:
        return redirect('/login_cus')


@app.route('/track_spending_cus', methods=['POST'])   
def track_spending_cus_Auth():
    try:
        email = session['email1']
    except:
        return redirect('/login_cus')

    #user specified view
    date_start = request.form['starting date']
    date_end = request.form['ending date']

    cursor = conn.cursor()
    if (date_start) and (date_end):
        query1 = '''SELECT COALESCE(SUM(price),0) AS total_spending
        FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
        WHERE customer_email = %s AND purchase_date BETWEEN %s AND %s'''
        query2 = '''SELECT YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, COALESCE(SUM(price),0) AS total_spending
        FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
        WHERE customer_email = %s AND purchase_date BETWEEN %s AND %s 
        GROUP BY year, month'''
        cursor.execute(query1, (email, date_start, date_end))
        total = cursor.fetchall()
        cursor.execute(query2, (email, date_start, date_end))
        monthly = cursor.fetchall()
        cursor.close()
        return render_template('track_spending_cus.html', email=email, post1=total, post2=monthly)
    
    #default view
    else:
        date_end = today
        date_start_year = today + datetime.timedelta(-365)
        date_start_half = today + datetime.timedelta(-180)
        cursor = conn.cursor()
        query1 = '''SELECT COALESCE(SUM(price),0) AS total_spending
        FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
        WHERE customer_email = %s AND purchase_date BETWEEN %s AND %s'''
        query2 = '''SELECT YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, COALESCE(SUM(price),0) AS total_spending
        FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
        WHERE customer_email = %s AND purchase_date BETWEEN %s AND %s
        GROUP BY year, month'''
        cursor.execute(query1, (email, date_start_year, date_end))
        total = cursor.fetchall()
        cursor.execute(query2, (email, date_start_half, date_end))
        monthly = cursor.fetchall()  
        cursor.close()
        return render_template('track_spending_cus.html', email=email, post1=total, post2=monthly)


@app.route('/logout_cus')
def logout_cus():
	session.pop('email1')
	return render_template('logout_cus.html')


    
'''
booking agent
login and register
'''
#==============================================================================
# booking agent login (all data required)
#==============================================================================
@app.route('/login_ba')
def login_ba():
	return render_template('login_ba.html')


@app.route('/loginAuth_ba', methods=['GET', 'POST'])
def loginAuth_ba():
	email = request.form['email']
	password = request.form['password']
	cursor = conn.cursor()
	query = 'SELECT * FROM booking_agent WHERE email = %s AND password = MD5(%s)'
	cursor.execute(query, (email, password))
	data = cursor.fetchone()
	cursor.close()
	if (data):
		session['email2'] = email
		return redirect('/home_ba')
	else:
		error = 'Invalid login or username'
		return render_template('login_ba.html', error=error)
 
    
#==============================================================================
# booking agent register, all data required
# check if email or agent_id already exists
#==============================================================================
@app.route('/register_ba')
def register_ba():
	return render_template('register_ba.html')
    

@app.route('/registerAuth_ba', methods=['GET', 'POST'])
def registerAuth_ba():
    email = request.form['email']
    password = request.form['password']
    agent_id = request.form['booking agent id']

    cursor = conn.cursor()
    # check if email/agent id exist
    query = 'SELECT * FROM booking_agent WHERE email = %s OR booking_agent_id = %s'
    cursor.execute(query, (email, agent_id))
    data = cursor.fetchone()
    if (data):
	#If the previous query returns data, then user exists
        error = "This booking agent id/email already exists"
        return render_template('register_ba.html', error = error)
    else:
        ins = 'INSERT INTO booking_agent VALUES(%s, MD5(%s), %s)'
        cursor.execute(ins, (email, password, agent_id))
        conn.commit()
        cursor.close()
        return render_template('login_ba.html')


#==============================================================================
# display all the upcoming flights starting from today booked by the agent
#==============================================================================
@app.route('/home_ba')
def home_ba():
    try:
        email = session['email2']
    except:
        return redirect('/login_ba') 
       
    cursor = conn.cursor()
    query = '''SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, status, customer_email
    FROM flight NATURAL JOIN ticket NATURAL JOIN purchases NATURAL JOIN booking_agent
    WHERE booking_agent.email = %s AND status = %s AND DATE(departure_time) >= %s
    ORDER BY departure_time'''
    cursor.execute(query, (email, 'upcoming', today))
    data = cursor.fetchall()
    cursor.close()
    return render_template('home_ba.html', email=email, posts=data)


#==============================================================================
# search upcoming flight based on city, airprot, date (data not required)
# if no data for city/airport, select flights for all cities/airports:
# if no data for date, use today
#==============================================================================
@app.route('/search_ba', methods=['GET'])
def search_ba():
    try:
        email = session['email2']
        return render_template('search_ba.html', email=email)
    except:
        return redirect('/login_ba')


@app.route('/search_ba', methods=['POST'])
def search_ba_Auth():  
    try:
        email = session['email2']
    except:
        return redirect('/login_ba')
    
    source_city = request.form['source city']
    source_airport = request.form['source airport']
    des_city = request.form['destination city']
    des_airport = request.form['destination airport']
    date = request.form['date']
    # if date is empty, use today, search flights.departure_time = today
    if not date:
        date = today
    data_l = [source_city, des_city, source_airport, des_airport]
    data_l_revised = [i if (i.strip() != '') else None for i in data_l]
    data_l_revised.append('upcoming')
    data_l_revised.append(date)
    data_t = tuple(data_l_revised)
    cursor = conn.cursor()
    query = '''SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price
    FROM flight JOIN airport S ON S.airport_name = departure_airport JOIN airport T ON T.airport_name = arrival_airport
    WHERE S.airport_city = IFNULL(%s, S.airport_city) AND T.airport_city = IFNULL(%s, T.airport_city)
    AND departure_airport = IFNULL(%s, departure_airport) AND arrival_airport = IFNULL(%s, arrival_airport) 
    AND status = %s AND DATE(departure_time) = %s'''  
    cursor.execute(query, data_t)
    data = cursor.fetchall()
    cursor.close()
    if not data:
        error = 'no such flight'
        return render_template('search_ba.html', email=email, error=error)
    else:
        return render_template('search_ba.html', email=email, posts=data) 


#==============================================================================
# booking agent purchase ticket for customers (all data required)
# 1. check customer in the customer database
# 2. check if flight exists
# 3. check if enough seat left
#==============================================================================
@app.route('/purchase_ticket_ba', methods=['GET'])
def purchase_ticket_ba():
    try:
        email = session['email2']
        return render_template('purchase_ticket_ba.html', email=email)
    except:
        return redirect('/login_ba')


@app.route('/purchase_ticket_ba', methods=['POST'])
def purchase_ticket_ba_Auth():  
    try:
        email = session['email2']
    except:
        return redirect('/login_ba')
    
    airline_name = request.form['airline name']
    flight_num = request.form['flight number']
    customer_email = request.form['customer email']
    cursor = conn.cursor()
    
    #check if we have such customer
    check0 = '''SELECT * 
    FROM customer
    WHERE email = %s'''
    cursor.execute(check0, customer_email)
    check_data0 = cursor.fetchall()
    if not check_data0:
        error = 'no such customer'
        cursor.close()
        return render_template('purchase_ticket_ba.html', email=email, error=error)
    
    #check if we have the upcoming flight
    check1 = '''SELECT * 
    FROM flight 
    WHERE airline_name = %s AND flight_num = %s AND status = %s'''
    cursor.execute(check1, (airline_name, flight_num, 'upcoming'))
    check_data1 = cursor.fetchall()    
    if not check_data1:
        error = 'no such upcoming flight'
        cursor.close()
        return render_template('purchase_ticket_ba.html', email=email, error=error)
    
    #check if has enough seat left
    ticket_num = '''SELECT COUNT(ticket_id) as sold
    FROM ticket
    WHERE airline_name = %s AND flight_num = %s'''
    cursor.execute(ticket_num, (airline_name, flight_num))
    ticket_sold = cursor.fetchone()
    seat = '''SELECT seats 
    FROM airplane NATURAL JOIN flight 
    WHERE flight.airline_name = %s AND flight_num = %s'''
    cursor.execute(seat, (airline_name, flight_num))
    seat_available = cursor.fetchone()
    if int(ticket_sold['sold']) >= int(seat_available['seats']):  
        error = 'the flight is full, find another flight'
        cursor.close()
        return render_template('purchase_ticket_ba.html', email=email, error=error)
    
    #pass all check
    #generate unique ticket_id
    while True:
        ticket_id = int(random.randint(10,99999999))
        check2 = '''SELECT * FROM ticket WHERE ticket_id = %s '''
        cursor.execute(check2, ticket_id)
        check_data2 = cursor.fetchone()
        if not (check_data2):
            break
    #find booking agent id
    find = '''SELECT booking_agent_id 
    FROM booking_agent
    WHERE email = %s'''
    cursor.execute(find, email)
    agent_id = cursor.fetchone()['booking_agent_id']
    #insert purchase information
    ins2 = '''INSERT INTO ticket
    VALUES(%s, %s, %s)'''
    cursor.execute(ins2, (ticket_id, airline_name, flight_num))
    conn.commit()
    ins1 = '''INSERT INTO purchases
    VALUES(%s, %s, %s, %s)'''
    cursor.execute(ins1, (ticket_id, customer_email, agent_id, today))
    conn.commit()
    cursor.close()
    message = 'Successful purchase'
    return render_template('purchase_ticket_ba.html', email=email, posts=message)


#==============================================================================
# view commission received by the agent in the selecting date (data not required)
# if no data in date_end: use today
# if no data in date_start: use past month
#==============================================================================
@app.route('/view_commission', methods=['GET'])
def view_commission():
    try:
        email = session['email2']
        return render_template('view_commission_ba.html', email=email)
    except:
        return redirect('/login_ba')
 
    
@app.route('/view_commission', methods=['POST'])
def view_commission_Auth():
    try:
        email = session['email2']
    except:
        return redirect('/login_ba')

    date_start = request.form['starting date']
    date_end = request.form['ending date']
    if not date_start:
        date_start = today + datetime.timedelta(-30)
    if not date_end:
        date_end = today
        
    cursor = conn.cursor()       
    query = '''SELECT COALESCE(SUM(price)*0.1,0) AS total_commission, 
    COALESCE(SUM(price)*0.1/COUNT(ticket_id),0) AS average_commission, COUNT(ticket_id) AS total_ticket
    FROM purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN booking_agent
    WHERE booking_agent.email = %s AND purchase_date BETWEEN %s AND %s'''
    cursor.execute(query, (email, date_start, date_end))
    data = cursor.fetchall()
    cursor.close()
    return render_template('view_commission_ba.html', email=email, posts=data)


#==============================================================================
# view top 5 customers of the booking agent 
# 1. by number of ticket in the past half year
# 2. by total commission in the past whole year
#==============================================================================
@app.route('/view_top_cus')
def view_top_cus():
    try:
        email = session['email2']
    except:
        return redirect('/login_ba')

    date_end = today
    date_start_half = today + datetime.timedelta(-180)
    date_start_year = today + datetime.timedelta(-365)
    cursor = conn.cursor()
    # top 5 customers by number of ticket
    query1 = '''SELECT customer_email, COUNT(ticket_id ) AS number_of_tickets
    FROM purchases NATURAL JOIN ticket NATURAL JOIN booking_agent
    WHERE booking_agent.email = %s AND purchase_date BETWEEN %s AND %s
    GROUP BY customer_email
    ORDER BY number_of_tickets DESC
    LIMIT 5'''
    # top 5 customers by total commission
    query2 = '''SELECT customer_email, COALESCE(SUM(price)*0.1,0) AS total_commission 
    FROM purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN booking_agent
    WHERE booking_agent.email = %s AND purchase_date BETWEEN %s AND %s
    GROUP BY customer_email
    ORDER BY total_commission DESC
    LIMIT 5'''
    cursor.execute(query1, (email, date_start_half, date_end))
    number = cursor.fetchall()
    cursor.execute(query2, (email, date_start_year, date_end))
    amount = cursor.fetchall()
    cursor.close()
    return render_template('view_top_ba.html', email=email, post1=number, post2=amount)


@app.route('/logout_ba')
def logout_ba():
	session.pop('email2')
	return render_template('logout_ba.html')
 
    

'''
airline staff
login and register
'''    
#==============================================================================
# airline staff login (all data required)
#==============================================================================
@app.route('/login_air')
def login_air():
	return render_template('login_air.html')

#Authenticates the login
@app.route('/loginAuth_air', methods=['GET', 'POST'])
def loginAuth_air():
	email = request.form['email']
	password = request.form['password']

	cursor = conn.cursor()
	query = 'SELECT * FROM airline_staff WHERE username = %s and password = MD5(%s)'
	cursor.execute(query, (email, password))
	data = cursor.fetchone()
	cursor.close()
	if (data):
		session['email3'] = email
		return redirect(url_for('home_air'))
	else:
		error = 'Invalid login or username'
		return render_template('login_air.html', error=error)


#==============================================================================
# airline staff register (all data required)
#==============================================================================
@app.route('/register_air')
def register_air():
	return render_template('register_air.html')
    

@app.route('/registerAuth_air', methods=['GET', 'POST'])
def registerAuth_air():
    email = request.form['email']
    password = request.form['password']
    first_name = request.form['first name']
    last_name = request.form['last name']
    dob = request.form['date of birth']
    airline_name = request.form['airline name']

    cursor = conn.cursor()
    # check foreign key constraint airline_name in airline
    check = '''SELECT * FROM airline WHERE airline_name = %s'''
    cursor.execute(check, airline_name)
    check_data = cursor.fetchone()
    if not check_data:
        cursor.close()
        error = 'The airline does not exist'
        return render_template('register_air.html', error=error)
    # check if staff exists 
    query = 'SELECT * FROM airline_staff WHERE username = %s'
    cursor.execute(query, email)
    data = cursor.fetchone()
    if (data):
        error = "This airline staff already exists"
        cursor.close()
        return render_template('register_air.html', error=error)
    else:
        ins = 'INSERT INTO airline_staff VALUES(%s, MD5(%s), %s, %s, %s, %s)'
        cursor.execute(ins, (email, password, first_name, last_name, dob, airline_name))
        conn.commit()
        cursor.close()
        return render_template('login_air.html')
 

#==============================================================================
# display the default setting: upcoming flight in the next 30 days of the particular airline
#==============================================================================
@app.route('/home_air')
def home_air_default():
    try:
        email = session['email3']
    except:
        return redirect('/login_air')
    
    cursor = conn.cursor()
    date_start = today
    date_end = today + datetime.timedelta(30)
    query1 = '''SELECT airline_name FROM airline_staff WHERE username = %s '''
    cursor.execute(query1, email)
    airline = cursor.fetchone()['airline_name']
    query2 = '''SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, status
    FROM flight
    WHERE airline_name = %s AND DATE(departure_time) BETWEEN %s AND %s AND status = %s'''
    cursor.execute(query2, (airline, date_start, date_end, 'upcoming'))
    data2 = cursor.fetchall()
    cursor.close()
    return render_template('/home_air.html', email=email, posts=data2)
 

#==============================================================================
# display the flight based on date, city, airport (data not required)
# if missing date_start, use today
# if missing date_end, use today+30 (default setting)
# if missing airport/city, select all flights in the date range    
#==============================================================================
@app.route('/home_air', methods=['GET','POST'])
def home_air():
    try: 
        email = session['email3']
    except:
        return redirect('/login_air')

    cursor = conn.cursor()   
    date_start = request.form['starting date']
    date_end = request.form['ending date']
    source_city = request.form['source city']
    des_city = request.form['destination city']
    source_airport = request.form['source airport']
    des_airport = request.form['destination airport']
    # select the airline of the airline_staff
    query1 = '''SELECT airline_name FROM airline_staff WHERE username = %s'''
    cursor.execute(query1, email)
    data1 = cursor.fetchone()
    airline = data1['airline_name']    
    if not (date_start):
        date_start = today
    if not (date_end):
        date_end = today + datetime.timedelta(30)        
    data_l = [airline, source_city, des_city, source_airport, des_airport]
    data_l_revised = [i if i.strip() != '' else None for i in data_l]
    data_l_revised.append(date_start)
    data_l_revised.append(date_end)
    data_t = tuple(data_l_revised)
    # select all flights based on airport/city, date  
    query2 = '''SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, status
    FROM flight JOIN airport S ON S.airport_name = departure_airport JOIN airport T ON T.airport_name = arrival_airport
    WHERE airline_name = %s AND S.airport_city = IFNULL(%s, S.airport_city) AND T.airport_city = IFNULL(%s, T.airport_city) 
    AND departure_airport = IFNULL(%s, departure_airport) AND arrival_airport = IFNULL(%s, arrival_airport)
    AND DATE(departure_time) BETWEEN %s AND %s 
    ORDER BY departure_time'''
    cursor.execute(query2, data_t)
    data2 = cursor.fetchall()
    if not(data2):
        error = 'no such flight'
        cursor.close()
        return render_template('home_air.html', email=email, error=error)
    else:
        cursor.close()
        return render_template('home_air.html', email=email, posts=data2)


#==============================================================================
# display the customer list of selected flight (data required)
# staff can only see list of their own airline flight
#==============================================================================
@app.route('/cus_list', methods=['GET'])
def cus_list():
    try:
        email = session['email3']
        return render_template('cus_list.html', email=email)
    except:
        return redirect('/login_air')
    
    
@app.route('/cus_list', methods=['POST'])
def cus_list_Auth():
    try:
        email = session['email3']
    except:
        return redirect('/login_air')
    
    cursor = conn.cursor()
    # see customer list for a flight
    flight = request.form['flight number']
    # select the airline of the airline_staff
    query1 = '''SELECT airline_name FROM airline_staff WHERE username = %s'''
    cursor.execute(query1, email)
    data1 = cursor.fetchone()
    airline = data1['airline_name'] 
    # check if we have such flight
    check = '''SELECT * FROM flight WHERE airline_name = %s AND flight_num = %s '''
    cursor.execute(check, (airline, flight))
    check_data = cursor.fetchall()
    if not (check_data):
        error = 'no such flight in your airline'
        cursor.close()
        return render_template('home_air.html', email=email, error=error)
    else:
        query3 = '''SELECT customer_email
        FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
        WHERE airline_name = %s AND flight_num = %s'''
        cursor.execute(query3, (airline, flight))
        customer_l = cursor.fetchall()
        cursor.close()
        return render_template('home_air.html', email=email, posts=customer_l)


#==============================================================================
# create flight for the staff's own airline (all data required)
# 1. check if the flight exists
# 2. check if (airline_name, airplane_id) in airplane
# 3. check if departure_airport, arrival_airport in airport
#==============================================================================
@app.route('/create_new_flight', methods=['GET'])
def create_new_flight():
    try:
        email = session['email3']
    except:
        return redirect('/login_air')
    cursor = conn.cursor()
    date_start = today
    date_end = today + datetime.timedelta(30)
    query1 = '''SELECT airline_name FROM airline_staff WHERE username = %s '''
    cursor.execute(query1, email)
    airline = cursor.fetchone()['airline_name']
    query2 = '''SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, status
    FROM flight
    WHERE airline_name = %s AND DATE(departure_time) BETWEEN %s AND %s AND status = %s'''
    cursor.execute(query2, (airline, date_start, date_end, 'upcoming'))
    data2 = cursor.fetchall()
    cursor.close()
    return render_template('/create_new_flight.html', email=email, posts=data2) 
  
    
@app.route('/create_new_flight', methods=['POST']) 
def create_new_flight_Auth():
    try:
        email = session['email3']
    except:
        return redirect('/login_air')
    
    cursor = conn.cursor()
    query = '''SELECT airline_name FROM airline_staff WHERE username = %s '''
    cursor.execute(query, email)
    airline = cursor.fetchone()
    airline_name = airline['airline_name']
    flight_num = request.form['flight number']
    dep_airport = request.form['departure airport']
    dep_time = request.form['departure time']
    arrival_airport = request.form['arrival airport']
    arrival_time = request.form['arrival time']
    price = request.form['price']
    status = request.form['status']
    airplane_id = request.form['airplane id']
    
    date_start = today
    date_end = today + datetime.timedelta(30)
    query2 = '''SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, status
    FROM flight
    WHERE airline_name = %s AND DATE(departure_time) BETWEEN %s AND %s AND status = %s'''
    cursor.execute(query2, (airline_name, date_start, date_end, 'upcoming'))
    data2 = cursor.fetchall()
    
    # check if status in [upcoming, in progress, delayed]
    if status.strip() not in ['upcoming', 'in progress', 'delayed']:
        error = 'wrong status, status must be upcoming/in progress/delayed'
        cursor.close()
        return render_template('create_new_flight.html', email=email, posts=data2, error=error)
    
    # check whether the flight exist
    check1 = '''SELECT * FROM flight WHERE airline_name = %s AND flight_num = %s'''
    cursor.execute(check1, (airline_name, flight_num))
    check1_data = cursor.fetchone()
    if (check1_data):
        error = 'The flight already exists'
        cursor.close()
        return render_template('create_new_flight.html', email=email, posts=data2, error=error)

    #check foreign key constratin for (airline_name, airplane_id) in airplane
    check2 = '''SELECT * FROM airplane WHERE airline_name = %s AND airplane_id = %s'''
    cursor.execute(check2, (airline_name, airplane_id))
    check2_data = cursor.fetchone()
    #check foreign key for departure_airport in airport
    check3 = '''SELECT * FROM airport WHERE airport_name = %s'''
    cursor.execute(check3, dep_airport)
    check3_data = cursor.fetchone()
    #check foreign key for arrival_airport in airport
    check4 = '''SELECT * FROM airport WHERE airport_name = %s'''
    cursor.execute(check4, arrival_airport)
    check4_data = cursor.fetchone()
            
    if check2_data and check3_data and check4_data:
        ins = '''INSERT INTO flight 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) '''
        cursor.execute(ins, (airline_name, flight_num, dep_airport, dep_time, arrival_airport, arrival_time, price, status, airplane_id))
        conn.commit()                   
        msg = 'New flight created successfully'
    
    else:
        error = 'invalid flight information of airplane_id/airport'
        
    query2 = '''SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, status
    FROM flight
    WHERE airline_name = %s AND DATE(departure_time) BETWEEN %s AND %s AND status = %s'''
    cursor.execute(query2, (airline_name, date_start, date_end, 'upcoming'))
    data2 = cursor.fetchall()
    cursor.close()
    
    if check2_data and check3_data and check4_data:
        return render_template('create_new_flight.html', email=email, msg=msg, posts=data2)
    else:
        return render_template('create_new_flight.html', email=email, posts=data2, error=error)
        
    
    
#==============================================================================
# change status for the flight of the staff's own airline (all data required)
# 1. check status in [upcoming, in progress, delayed]
# 2. check if the flight exists
#==============================================================================
@app.route('/change_status', methods=['GET'])
def change_status():
    try:
        email = session['email3']
        return render_template('change_status.html', email=email)
    except:
        return redirect('/login_air')

    
@app.route('/change_status', methods=['POST']) 
def change_status_Auth():
    try:
        email = session['email3']
    except:
        return redirect('/login_air')
    
    cursor = conn.cursor()  
    query = '''SELECT airline_name FROM airline_staff WHERE username = %s '''
    cursor.execute(query, email)
    airline = cursor.fetchone()
    airline_name = airline['airline_name']
    flight_num = request.form['flight number']
    status = request.form['new status']
    
    # check if status in [upcoming, in progress, delayed]
    if status.strip() not in ['upcoming', 'in progress', 'delayed']:
        error = 'wrong status'
        cursor.close()
        return render_template('change_status.html', email=email, error=error)
    
    # check if the flight exist
    check1 = '''SELECT * FROM flight WHERE airline_name = %s AND flight_num = %s'''
    cursor.execute(check1, (airline_name, flight_num))
    check1_data = cursor.fetchone()
    if not (check1_data):
        error = 'The flight does not exist'
        cursor.close()
        return render_template('change_status.html', email=email, error=error)
  
    # pass all check and update
    upd = '''UPDATE flight
    SET status = %s
    WHERE flight_num = %s AND airline_name = %s'''
    cursor.execute(upd, (status, flight_num, airline_name))
    conn.commit()
    cursor.close()
    msg = 'Successful update'
    return render_template('change_status.html', email=email, msg=msg)


#==============================================================================
# add airplane for the airline the staff works in (all data required)
# 1. check if plane exists for the airline
#==============================================================================  
@app.route('/add_plane', methods=['GET'])
def add_plane():
    try:
        email = session['email3']
        return render_template('add_plane.html', email=email)
    except:
        return redirect('/login_air')
    
    
@app.route('/add_plane', methods=['POST'])
def add_plane_Auth():
    try:
        email = session['email3']
    except:
        return redirect('/login_air') 
       
    cursor = conn.cursor()  
    query = '''SELECT airline_name FROM airline_staff WHERE username = %s '''
    cursor.execute(query, email)
    airline = cursor.fetchone()
    airline_name = airline['airline_name']
    airplane_id = request.form['airplane id']
    seats = request.form['seats']
    
    # check if plane exist
    check1 = '''SELECT * FROM airplane WHERE airline_name = %s AND airplane_id = %s'''
    cursor.execute(check1, (airline_name, airplane_id))
    check1_data = cursor.fetchone()
    if (check1_data):
        error = 'The plane already exists'
        cursor.close()
        return render_template('add_plane.html', email=email, error=error)
    else:
        ins = '''INSERT INTO airplane
        VALUES(%s, %s, %s)'''
        cursor.execute(ins, (airline_name, airplane_id, seats))
        conn.commit()
        query = '''SELECT airplane_id, seats 
        FROM airplane 
        WHERE airline_name = %s'''
        cursor.execute(query, airline_name)
        data = cursor.fetchall()
        cursor.close()
        msg = 'Successful insert'
        return render_template('add_plane.html', email=email, msg=msg, posts=data)
 
 
#==============================================================================
# add airport (all data required)
#==============================================================================
@app.route('/add_airport', methods=['GET'])
def add_airport():
    try:
        email = session['email3']
        return render_template('add_airport.html', email=email)
    except:
        return redirect('/login_air')
    
    
@app.route('/add_airport', methods=['POST'])
def add_airport_Auth():
    try:
        email = session['email3']
    except:
        return redirect('/login_air') 
    
    airport_name = request.form['airport name']
    airport_city = request.form['airport city']
    cursor = conn.cursor()

    # check if airport exist
    check1 = '''SELECT * FROM airport WHERE airport_name = %s AND airport_city = %s'''
    cursor.execute(check1, (airport_name, airport_city))
    check1_data = cursor.fetchone()
    if (check1_data):
        error = 'The airport already exists'
        cursor.close()
        return render_template('add_airport.html', email=email, error=error)

    ins = '''INSERT INTO airport
    VALUES(%s, %s)'''
    cursor.execute(ins, (airport_name, airport_city))
    conn.commit()
    cursor.close()
    msg = 'Successful insert'
    return render_template('add_airport.html', email=email, msg=msg)

  
#==============================================================================
# view top 5 agents of the airline the staff works in
# 1. number of tickets sold in the past month
# 2. number of tickets sold in the past year
# 3. amount of commission in the past year
#==============================================================================
@app.route('/view_ba')
def view_ba():
    try:
        email = session['email3']
    except:
        return redirect('/login_air')  
    
    cursor = conn.cursor()
    # find the airline the staff works in
    query = '''SELECT airline_name FROM airline_staff WHERE username = %s '''
    cursor.execute(query, email)
    airline = cursor.fetchone()
    airline_name = airline['airline_name']
    
    # top 5 agents based on number of tickets sales for the past month
    past_month = today + datetime.timedelta(-30)
    query1 = '''SELECT booking_agent_id, COUNT(ticket_id) AS total_tickets
    FROM purchases NATURAL JOIN ticket
    WHERE purchase_date >= %s AND booking_agent_id > 0 AND airline_name = %s
    GROUP BY booking_agent_id
    ORDER BY total_tickets DESC
    LIMIT 5'''
    cursor.execute(query1, (past_month, airline_name))
    data1 = cursor.fetchall()  
    
    # top 5 agents based on number of tickets sales for the past year
    past_year = today + datetime.timedelta(-365)
    query2 = '''SELECT booking_agent_id, COUNT(ticket_id) AS total_tickets
    FROM purchases NATURAL JOIN ticket
    WHERE purchase_date >= %s AND booking_agent_id > 0 AND airline_name = %s
    GROUP BY booking_agent_id
    ORDER BY total_tickets DESC
    LIMIT 5'''
    cursor.execute(query2, (past_year, airline_name))
    data2 = cursor.fetchall()
    
    # Top 5 booking agents based on the amount of commission received for the last year    
    query3 = '''SELECT booking_agent_id, COALESCE(SUM(price)*0.1, 0) AS total_commission
    FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
    WHERE purchase_date >= %s AND booking_agent_id > 0 AND ticket.airline_name = %s
    GROUP BY booking_agent_id
    ORDER BY total_commission DESC
    LIMIT 5'''
    cursor.execute(query3, (past_year, airline_name))
    data3 = cursor.fetchall()
    cursor.close()
    return render_template('view_ba.html', email=email, post1=data1, post2=data2, post3=data3)


#==============================================================================
# view most frequent customer of the airine the staff works in in the past year
#==============================================================================  
@app.route('/frequent_customer')
def frequent_customer():
    try:
        email = session['email3']
    except:
        return redirect('/login_air') 
    
    cursor = conn.cursor()
    # the airline the staff works in
    query0 = '''SELECT airline_name FROM airline_staff WHERE username = %s '''
    cursor.execute(query0, email)
    airline = cursor.fetchone()
    airline_name = airline['airline_name']
    
    #  the most frequent customer within the last year
    past_year = today + datetime.timedelta(-365)
    view = '''CREATE VIEW customer_ticket AS
    (SELECT customer_email, COUNT(ticket_id) as times_of_flights
    FROM purchases NATURAL JOIN ticket
    WHERE purchase_date >= %s AND airline_name = %s
    GROUP BY customer_email
    ORDER BY times_of_flights)'''
    cursor.execute(view, (past_year, airline_name))
    query = '''SELECT customer_email, times_of_flights
    FROM customer_ticket 
    WHERE times_of_flights = (SELECT MAX(times_of_flights) FROM customer_ticket)
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    drop = '''DROP VIEW customer_ticket'''
    cursor.execute(drop)
    conn.commit()
    cursor.close()
    return render_template('frequent_customer.html', email=email, posts=data)
    

#==============================================================================
# view flights (operated by the airline) already taken by a selected customer (all data required)
#==============================================================================
@app.route('/customer_list', methods=['GET'])
def customer_list():
    try:
        email = session['email3']
        return render_template('customer_list.html', email=email)
    except:
        return redirect('/login_air')
    
    
@app.route('/customer_list',methods=['POST'])
def customer_list_Auth():
    try:
        email = session['email3']
    except:
        return redirect('/login_air') 

    cursor = conn.cursor()
    query = '''SELECT airline_name FROM airline_staff WHERE username = %s '''
    cursor.execute(query, email)
    airline = cursor.fetchone()
    airline_name = airline['airline_name']
    customer_email = request.form['customer email']
    date = today
    # a list of all flights a particular customer has taken only on that particular airline 
    query2 = '''SELECT flight_num
    FROM flight NATURAL JOIN ticket NATURAL JOIN purchases
    WHERE flight.airline_name = %s AND customer_email = %s AND DATE(departure_time) <= %s'''
    cursor.execute(query2, (airline_name, customer_email, date))
    data2 = cursor.fetchall()
    cursor.close()
    return render_template('customer_list.html', email=email, posts=data2)


#==============================================================================
# view ticket sold situation of the airline (data not required)
# if missing start_date, use last year:
# if missing end_date, use today:
# 1. total ticket sold in date range
# 2. month wise ticket sold in date range
#==============================================================================
@app.route('/view_report', methods=['GET'])
def view_report():
    try:
        email = session['email3']
        return render_template('view_report.html', email=email)
    except:
        return redirect('/login_air')


@app.route('/view_report',methods=['POST'])
def view_report_Auth():
    try:
        email = session['email3']
    except:
        return redirect('/login_air')  
    
    cursor = conn.cursor()
    query0 = '''SELECT airline_name FROM airline_staff WHERE username = %s '''
    cursor.execute(query0, email)
    airline = cursor.fetchone()
    airline_name = airline['airline_name']   
    start_date = request.form['starting date']
    end_date = request.form['ending date']
    if not (start_date):
        start_date = today + datetime.timedelta(-365)
    if not (end_date):
        end_date = today
    
    # total tickets sold
    query1 = '''SELECT COUNT(ticket_id) AS total_ticket_sold
    FROM purchases NATURAL JOIN ticket 
    WHERE purchase_date BETWEEN %s AND %s AND airline_name = %s'''
    cursor.execute(query1, (start_date, end_date, airline_name))
    data1 = cursor.fetchall()
    
    # month wise tickets sold
    query2 = '''SELECT YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, COUNT(ticket_id) AS ticket_sold
    FROM purchases NATURAL JOIN ticket
    WHERE purchase_date BETWEEN %s AND %s AND airline_name = %s
    GROUP BY year, month'''
    cursor.execute(query2, (start_date, end_date, airline_name))
    data2 = cursor.fetchall()
    cursor.close()
    return render_template('view_report.html', email=email, post1=data1, post2=data2)
    

#==============================================================================
# compare direct/indirect revenue of the airline  
# 1. last month compare pie chart
# 2. last year compare pie chart
#==============================================================================
@app.route('/compare_revenue')
def compare_revenue():
    try:
        email = session['email3']
    except:
        return redirect('/login_air') 
    
    cursor = conn.cursor()
    query0 = '''SELECT airline_name FROM airline_staff WHERE username = %s '''
    cursor.execute(query0, email)
    airline = cursor.fetchone()
    airline_name = airline['airline_name']
    
    # direct purchase last month
    past_month = today + datetime.timedelta(-30)
    query1 = '''SELECT COALESCE(SUM(price), 0) AS customer_purchase
    FROM flight NATURAL JOIN ticket NATURAL JOIN purchases
    WHERE booking_agent_id IS NULL AND purchase_date >= %s AND ticket.airline_name = %s'''
    cursor.execute(query1, (past_month, airline_name))
    data1 = cursor.fetchall()
       
    # direct purhcase last year
    past_year = today + datetime.timedelta(-365)
    query2 = '''SELECT COALESCE(SUM(price), 0) AS customer_purchase_year
    FROM flight NATURAL JOIN ticket NATURAL JOIN purchases
    WHERE booking_agent_id IS NULL AND purchase_date >= %s AND ticket.airline_name = %s'''
    cursor.execute(query2, (past_year, airline_name))
    data2 = cursor.fetchall()
    
    # indirect purchase last month
    query3 = '''SELECT COALESCE(SUM(price), 0) AS ba_purchase
    FROM flight NATURAL JOIN ticket NATURAL JOIN purchases
    WHERE booking_agent_id IS NOT NULL AND purchase_date >= %s AND ticket.airline_name = %s'''
    cursor.execute(query3, (past_month, airline_name))
    data3 = cursor.fetchall()
    
    # indirect purchase last year
    query4 = '''SELECT COALESCE(SUM(price), 0) AS ba_purchase_year
    FROM flight NATURAL JOIN ticket NATURAL JOIN purchases
    WHERE booking_agent_id IS NOT NULL AND purchase_date >= %s AND ticket.airline_name = %s'''
    cursor.execute(query4, (past_year, airline_name))
    data4 = cursor.fetchall()  
    cursor.close()
    return render_template('compare_revenue.html', email=email, post1=data1, post2=data2, post3=data3, post4=data4)


#==============================================================================
# view top 3 destination of the airline
# 1. past 3 month
# 2. past year
#==============================================================================
@app.route('/top_des')
def top_des():
    try:
        email = session['email3']
    except:
        return redirect('/login_air')  
    
    cursor = conn.cursor()
    query0 = '''SELECT airline_name FROM airline_staff WHERE username = %s '''
    cursor.execute(query0, email)
    airline = cursor.fetchone()
    airline_name = airline['airline_name']
    
    # the top 3 most popular destinations for last 3 months
    past_3_month = today + datetime.timedelta(-90)
    query1 = '''SELECT airport_city
    FROM flight NATURAL JOIN ticket JOIN airport ON arrival_airport = airport_name
    WHERE arrival_time BETWEEN %s AND %s AND ticket.airline_name = %s
    GROUP BY airport_city
    ORDER BY COUNT(ticket_id) DESC
    LIMIT 3'''
    cursor.execute(query1, (past_3_month, today, airline_name))
    data1 = cursor.fetchall()
    
    # the top 3 most popular destinations for last year
    past_year = today + datetime.timedelta(-365)
    query2 = '''SELECT airport_city
    FROM flight NATURAL JOIN ticket JOIN airport ON arrival_airport = airport_name
    WHERE arrival_time BETWEEN %s AND %s AND ticket.airline_name = %s
    GROUP BY airport_city
    ORDER BY COUNT(ticket_id) DESC
    LIMIT 3'''
    cursor.execute(query2, (past_year, today, airline_name))
    data2 = cursor.fetchall()  
    cursor.close()
    return render_template('top_des.html', email=email, post1=data1, post2=data2)

        
@app.route('/logout_air')
def logout_air():
    session.pop('email3')
    return render_template('logout_air.html')


app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)