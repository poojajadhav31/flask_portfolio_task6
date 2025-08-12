from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

# Optional: file to store contact submissions
SUBMISSIONS_FILE = "submissions.csv"

def save_submission(name, email, message):
    """Save contact form submission to a CSV file (append mode)."""
    file_exists = os.path.isfile(SUBMISSIONS_FILE)
    with open(SUBMISSIONS_FILE, mode="a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            # write header once
            writer.writerow(["Name", "Email", "Message"])
        writer.writerow([name, email, message])

@app.route("/")
def home():
    # You can pass variables into the template if needed
    return render_template("index.html", title="Pooja Jadhav | Portfolio")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Get form fields
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        # Basic validation
        if not name or not email or not message:
            error = "Please fill in all fields."
            return render_template("contact.html", error=error, name=name, email=email, message=message)

        # Save submission (or send email/store in DB)
        try:
            save_submission(name, email, message)
        except Exception as e:
            # if saving fails, log and still show success message or show error
            print("Error saving submission:", e)

        # render success page with user's name
        return render_template("success.html", name=name)

    # GET -> show contact form
    return render_template("contact.html")

# Optional route to view submissions (dev use only)
@app.route("/submissions")
def submissions():
    rows = []
    if os.path.isfile(SUBMISSIONS_FILE):
        with open(SUBMISSIONS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    return render_template("submissions.html", rows=rows)

if __name__ == "__main__":
    # debug=True for development only; remove or set False for production
    app.run(debug=True, host="127.0.0.1", port=5000)
