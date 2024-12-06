from flask import Flask, render_template, request, redirect, jsonify
import psycopg2

app = Flask(__name__)

# Database connection
conn = psycopg2.connect(
    dbname="community_event_app",
    user="shriyamohite",
    password="password123",
    host="localhost",
    port="5434"
)
cursor = conn.cursor()

@app.route("/")
def home():
    return render_template("index.html")

# Route to display all users
@app.route("/users")
def get_users():
    cursor.execute("SELECT * FROM \"User\";")
    users = cursor.fetchall()
    return render_template("users.html", users=users)

# Route to display all events
@app.route("/events")
def get_events():
    cursor.execute("SELECT * FROM \"Event\";")
    events = cursor.fetchall()
    return render_template("events.html", events=events)

# Route to RSVP for an event
@app.route("/rsvp", methods=["GET", "POST"])
def rsvp():
    if request.method == "POST":
        user_id = request.form["user_id"]
        event_id = request.form["event_id"]
        status = request.form["status"]
        cursor.execute("INSERT INTO RSVP (UserID, EventID, Status) VALUES (%s, %s, %s)", (user_id, event_id, status))
        conn.commit()
        return redirect("/rsvp")
    cursor.execute("SELECT * FROM \"Event\";")
    events = cursor.fetchall()
    return render_template("rsvp.html", events=events)

# Route to view notifications
@app.route("/notifications")
def notifications():
    cursor.execute("SELECT * FROM notification WHERE notificationtype = 'Event Reminder';")
    notifications = cursor.fetchall()
    return render_template("notifications.html", notifications=notifications)

# Route to send a message
@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "POST":
        message_content = request.form["message_content"]
        sent_by = request.form["sent_by"]
        sent_to = request.form["sent_to"]
        event_id = request.form["event_id"]
        cursor.execute(
            "INSERT INTO message (MessageContent, SentBy, SentTo, EventID) VALUES (%s, %s, %s, %s)",
            (message_content, sent_by, sent_to, event_id)
        )
        conn.commit()
        return redirect("/messages")
    cursor.execute("SELECT * FROM \"Event\";")
    events = cursor.fetchall()
    return render_template("messages.html", events=events)

if __name__ == "__main__":
    app.run(debug=True)
