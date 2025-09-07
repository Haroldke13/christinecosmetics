from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app
from flask_mail import Message

contact_bp = Blueprint("contact", __name__)

@contact_bp.route("/contact-us", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip()
        phone = (request.form.get("phone") or "").strip()
        message = (request.form.get("message") or "").strip()

        if not name or not email or not message:
            flash("Name, email, and message are required.", "warning")
            return redirect(url_for("contact.contact"))

        # Save to Mongo
        doc = {
            "name": name,
            "email": email,
            "phone": phone,
            "message": message,
        }
        current_app.mongo.contacts.insert_one(doc)

        # Send confirmation email
        try:
            msg = Message(
                subject="Thank you for contacting Christine Cosmetics",
                recipients=[email],
                html=f"""
                    <h3>Hi {name},</h3>
                    <p>Thanks for reaching out to Christine Cosmetics.</p>
                    <p><b>Your message:</b></p>
                    <p>{message}</p>
                    <br>
                    <p>We’ll get back to you soon!</p>
                """
            )
            current_app.mail.send(msg)
            flash("Message saved and confirmation email sent.", "success")
        except Exception as e:
            flash(f"Message saved but email not sent: {e}", "warning")

        return redirect(url_for("contact.contact"))

    return render_template("contact-us.html")
