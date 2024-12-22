# Table Reservation System README

This API is designed to manage table reservations for restaurants. The API will include data on the guests who make the reservations, the total number of guests, the tables they need and the time when tables are reserved.

---

## Compatibility
Tested on Linux systems, other systems may be incompatible.

## Installation for Local Environments

1. From the terminal run the command ```bash install/initial.sh```.
2. Create a database using postgreSQL and input the DATABASE_URI using the following format:
    - DATABASE_URI="postgresql+psycopg2://DATABASE_OWNER:PASSWORD@localhost:5432/DATABASE_NAME"
    - Or, run the command ```bash install/create_database.sh``` to create a generic database and automatically input the DATABASE_URI.
3. Create the relations for the database and seed with sample data by running the command ```bash install/tables.sh```
4. Use a browser, Insomnia or a similar program to access the database information.

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
![Initial ERD](images/TRS_ERD_first.drawio.png)

### Final ERD
![Final ERD](images/TRS_ERD_final.drawio.png)