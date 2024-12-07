from flask import Flask, render_template, request, redirect, jsonify
import psycopg2

app = Flask(__name__)

# Database connection settings
DB_SETTINGS = {
    "dbname": "community_event_app",
    "user": "shriyamohite",  # Replace with your username
    "password": "password123",  # Replace with your password, or comment out if no password
    "host": "localhost",
    "port": "5434"
}


def get_db_connection():
    """Create and return a new database connection."""
    return psycopg2.connect(**DB_SETTINGS)


@app.route("/")
def home():
    return render_template("index.html")


# Route to display all users
@app.route("/users")
def get_users():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM \"User\";")
            users = cursor.fetchall()
    return render_template("users.html", users=users)


# Route to display events
@app.route("/events")
def get_events():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM \"Event\";")
            events = cursor.fetchall()
    return render_template("events.html", events=events)


# Route to RSVP for an event
@app.route("/rsvp", methods=["GET", "POST"])
def manage_rsvp():
    if request.method == "POST":
        user_id = request.form["user_id"]
        event_id = request.form["event_id"]
        status = request.form["status"]
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO \"RSVP\" (UserID, EventID, Status) VALUES (%s, %s, %s)",
                    (user_id, event_id, status)
                )
                conn.commit()
        return redirect("/rsvp")
    else:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM \"RSVP\";")
                rsvps = cursor.fetchall()
        return render_template("rsvp.html", rsvps=rsvps)


# Route to send and view messages
@app.route("/messages", methods=["GET", "POST"])
def manage_messages():
    if request.method == "POST":
        message_content = request.form["message_content"]
        sent_by = request.form["sent_by"]
        sent_to = request.form["sent_to"]
        event_id = request.form.get("event_id", None)  # Optional
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO \"message\" (MessageContent, SentBy, SentTo, EventID) VALUES (%s, %s, %s, %s)",
                    (message_content, sent_by, sent_to, event_id)
                )
                conn.commit()
        return redirect("/messages")
    else:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT m.MessageID, m.MessageContent, u1.Name AS SentBy, u2.Name AS SentTo, e.Title AS EventTitle
                    FROM "message" m
                    LEFT JOIN "User" u1 ON m.SentBy = u1.UserID
                    LEFT JOIN "User" u2 ON m.SentTo = u2.UserID
                    LEFT JOIN "Event" e ON m.EventID = e.EventID;
                """)
                messages = cursor.fetchall()
        return render_template("messages.html", messages=messages)


# Route to view notifications
@app.route("/notifications")
def get_notifications():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT n.NotificationID, u.Name AS UserName, n.NotificationContent, n.NotificationType
                FROM "notification" n
                JOIN "User" u ON n.UserID = u.UserID;
            """)
            notifications = cursor.fetchall()
    return render_template("notifications.html", notifications=notifications)


# Route to create a new event
@app.route("/create_event", methods=["GET", "POST"])
def create_event():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        date = request.form["date"]
        time = request.form["time"]
        location = request.form["location"]
        created_by = request.form["created_by"]
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO \"Event\" (Title, Description, Date, Time, Location, CreatedBy) VALUES (%s, %s, %s, %s, %s, %s)",
                    (title, description, date, time, location, created_by)
                )
                conn.commit()
        return redirect("/events")
    else:
        return render_template("create_event.html")


if __name__ == "__main__":
    app.run(debug=True)
