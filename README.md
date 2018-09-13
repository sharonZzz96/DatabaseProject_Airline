# DatabaseProject_Airline

————Flight Booking System————


Work Allocation:
- Python flask, mysql codes: Yueying Zhang (Sharon)
- HTML, jinjia codes: Zhengyuan Ding (Carol)

SQL data:
- airline.sql
- insert.txt (txt version of insert data)

Python code:
- part3.py

User case:
- user case.txt: all use cases explanation and sql queries

Templates:
- public_info.html: It is the index page. All users whether logged in or not, can search upcoming flights and see flight status 

- register_cus.html: customer register page
  register_ba.html: booking agent register page
  register_air.html: airline staff register page

- login_cus.html: customer login page
  login_ba.html: booking agent login page
  login_air.html: airline staff login page

Customer use cases:
- home_cus.html: show the upcoming flight of the customers
- search_flight_cus.html: search upcoming flights based on city/airport/date
- purchase_ticket_cus.html: purchase ticket based on airline and flight number
- track_spending_cus.html: if no input: display total amount of monty spent in the past year and a bar
chart showing month wise money spent for last 6 months; if has date input: display the total amount and month wise spending in the date range
- logout_cus.html: customer logout

Booking agent use cases:
- home_ba.html: show the upcoming flight booked by the agent
- search_ba.html: search upcoming flights based on city/airport/date
- purchase_ticket_ba.html: purchase ticket for the customer based on airline and flight number
- view_commission_ba.html: if no input: display the total amount of commission revceived, average commission, number of tickets in the past 30 days; if has date input: display the commission, average commission, number of tickets in the date range
- view_top_ba.html: display top 5 customers based on number of tickets bought from the agent in the past 6 months and amount of commission in the last year in bar charts
- logout_ba.html: booking agent logout

Airline staff use cases:
- home_air.html: if no input: display all flights operated by the airline in the next 30 days; if has date, airprot, city inputs, display the flights meeting the selection rules. See the customer list of a flight operated by the airline
-create_new_flight.html: display all flights operated by the airline in the next 30 days; create new flight for the airline
- change_status.html: change flight status for the airline
- add_plane.html: add airplane for the airline and display confirmation message
- add_airport.html: add a new airport
- view_ba.html: display top 5 booking agents based on the ticket sales of the airline for past year/month; display top 5 booking agent based on commission of the airline for the past year/month
- frequent_cusomter.html: display the most frequent customer in the last year of the airline
- customer_list.html: display the list of all flights a customer has taken on that airline
- view_report.html: total tickets sold in date range; month wise tickets solds in bar chart
- compare_revenue.html: pie chart for total amount of revenue from direct sales and indirect sales in the past month and past year
- top_des.html: display top 3 destinations for the last 3 months and last year
- logout_air.html: airline staff logout



