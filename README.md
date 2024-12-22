# Table Reservation System README

This API is designed to manage table reservations for restaurants. The API will include data on the guests who make the reservations, the total number of guests, the tables they need and the time when tables are reserved.

**[DEPLOYED API LINK](https://dev1002-web-api-server.onrender.com)**

---

## Compatibility
Tested on Linux systems, other systems may be incompatible.

## Installation for Local Environments

1. From the terminal run the command ```bash install/initial.sh```.
2. Create a database with the following steps:
    1. Open postgreSQL using ```psql``` in a terminal.
        - If you issues with authentication use ```sudo -u postgres psql``` in the terminal.
    2. Enter the following commands to create the database and it's user, change the names or password as you see fit.
        ```sql
        CREATE DATABASE booking_app_db;
        CREATE USER booking_app_user WITH PASSWORD 'user_password_123';
        GRANT ALL PRIVILEGES ON DATABASE booking_app_db TO booking_app_user;
        ```
2. Input the DATABASE_URI into .env using the following format:
    - DATABASE_URI="postgresql+psycopg2://DATABASE_OWNER:PASSWORD@localhost:5432/DATABASE_NAME"
    - If you didn't change the names or password of the user or database in step one, run ```install/env_auto.sh``` to set the .env file automatically.
4. Close all open terminals.
3. Create the relations for the database and seed with sample data by running the command ```bash install/tables.sh``` which can also be used to reset the tables at any point.
4. Run ```flask run``` in terminal before using a browser, Insomnia or a similar program to access the database information on port 8081.

## Feedback for Web API

### Initial Feedback on Idea and ERD
"Hi Taner. The idea and the ERD looks good. Approved. ✅ 
However, you can make it more complex if you want by making the relationship between bookings and tables as many-to-many. There can be multiple tables booked for a single booking." - Simon

    Action: Adding in additional many-to-many relation table named bookings_tables which will allow the model to include a situation where a booking involves more than one table.

### Feedback on Models
"Consider adding in unique constraint for bookings_tables so that a table can't be booked twice by the same booking. Additionally, you could add in verification for phone numbers so that a user won't input an invalid phone number." - Brendon

    Action: Added in the aforementioned constraints and verifications.

### Feedback on Installation
"You can make installation more simple for the user if you make bash file with all of the necessary commands for the initial install." - Bolt

    Action: Created the install.sh and other bash files to simplify installation for the user.


## Planning

### Initial ERD
- Lacked join table that enabled a booking to reserve multiple tables.
- Changed bookings_tables to allocations for conciseness.
- Changed 'time' to 'booking_date' for clarification.

![Initial ERD](images/TRS_ERD_first.drawio.png)


### Final ERD
![Final ERD](images/TRS_ERD_final.drawio.png)


## Future Development
There were some features that I would like to add that were beyond my understanding. The most prevalent one was I want the database to reject booking on the same tables at the same time. At the moment the database only registers date, so that would be the first step, but I was unable to work out how to add that constraint without denormalising the database.  
The same was also true of adding a constraint to allocations and venues where an booking that has more than one allocation would be unable to have tables at two different venues.