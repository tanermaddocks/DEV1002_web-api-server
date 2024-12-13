# Development Feedback for Web API

## Initial Feedback on Idea and ERD
### Feedback
"Hi Taner. The idea and the ERD looks good. Approved. ✅ 
However, you can make it more complex if you want by making the relationship between bookings and tables as many-to-many. There can be multiple tables booked for a single booking." - Simon
### Action
Adding in additional many-to-many relation table named bookings_tables which will allow the model to include a situation where a booking involves more than one table.