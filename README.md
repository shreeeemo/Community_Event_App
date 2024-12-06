# Community Event Management App

The **Community Event Management App** is a Flask-based web application that allows users to create, manage, RSVP for, and discover community events. This project demonstrates how to interact with a PostgreSQL database and build a functional backend for community-driven applications.

## Features
- View a list of users, events, RSVPs, messages, and notifications.
- Easily add, update, or delete events, RSVPs, and notifications.
- Connect and communicate with other users in the community.
- Intuitive and clean user interface.

## Prerequisites
- Python 3.12 or later
- PostgreSQL (with the database `community_event_app` set up)
- Required Python libraries (see below)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/shreeeemo/Community_Event_App.git
    cd Community_Event_App
    ```

2. Set up a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install flask psycopg2
    ```

4. Set up the PostgreSQL database:
   - Make sure your PostgreSQL service is running.
   - Create the database `community_event_app`.
   - Execute the provided SQL statements to create tables and insert sample data.

5. Start the Flask app:
    ```bash
    python app.py
    ```

6. Open the application in your browser:
    ```
    http://127.0.0.1:5000
    ```


## Database Schema
The database has the following tables:
1. **User**: Stores user information such as name and location.
2. **Event**: Contains event details such as title, description, date, time, location, and creator.
3. **RSVP**: Tracks user RSVPs for events.
4. **Message**: Facilitates communication between users.
5. **Notification**: Stores user notifications related to events or messages.

## Example Queries
- **Get all users who RSVP'd for a specific event:**
    ```sql
    SELECT u.Name, r.Status
    FROM "User" u
    JOIN "RSVP" r ON u.UserID = r.UserID
    WHERE r.EventID = 1;
    ```
- **Insert a new event:**
    ```sql
    INSERT INTO "Event" (Title, Description, Date, Time, Location, CreatedBy) 
    VALUES ('Holiday Party', 'End of year celebration', '2024-12-31', '20:00:00', 'Tempe Hall', 5);
    ```

## To-Do
- Add more routes for creating, updating, and deleting entries.
- Improve the frontend with CSS and JavaScript.
- Deploy the application to a cloud platform like Heroku or AWS.

## Contributors
- **Shriya Mohite**
- **Tanu Siddappa**
- **Kamden Watterberg**

