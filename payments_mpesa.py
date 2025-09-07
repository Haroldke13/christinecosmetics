import os, re, base64, logging
from datetime import datetime
import requests
from flask import Blueprint, request, jsonify, current_app
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

mpesa_bp = Blueprint("mpesa", __name__, url_prefix="/mpesa")

# --- Helpers ---
def _pdf_dir():
    d = os.path.join(current_app.root_path, "static", "mpesa_logs")
    os.makedirs(d, exist_ok=True)
    return d

def _save_pdf(title, data, prefix):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{ts}.pdf"
    path = os.path.join(_pdf_dir(), filename)

    c = canvas.Canvas(path, pagesize=A4)
    w, h = A4
    y = h - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, title)
    y -= 20
    c.setFont("Helvetica", 10)
    for k, v in data.items():
        c.drawString(50, y, f"{k}: {v}")
        y -= 14
    c.save()
    return f"static/mpesa_logs/{filename}"

def _format_phone(phone: str) -> str | None:
    if re.match(r"^(?:2547\d{8}|07\d{8})$", phone):
        return "254" + phone[1:] if phone.startswith("07") else phone
    return None

def _get_token():
    key = current_app.config["MPESA_CONSUMER_KEY"]
    secret = current_app.config["MPESA_CONSUMER_SECRET"]
    creds = base64.b64encode(f"{key}:{secret}".encode()).decode()
    headers = {"Authorization": f"Basic {creds}"}
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()["access_token"]

def _stk_password(ts):
    sc = current_app.config["MPESA_SHORTCODE"]
    pk = current_app.config["MPESA_PASSKEY"]
    raw = f"{sc}{pk}{ts}"
    return base64.b64encode(raw.encode()).decode()

# --- API Routes ---
@mpesa_bp.route("/stk_push", methods=["POST"])
def stk_push():
    body = request.get_json(force=True)
    phone = _format_phone(body.get("phone_number", ""))
    amount = int(float(body.get("amount", 0)))

    if not phone or amount <= 0:
        return jsonify({"error": "Invalid phone or amount"}), 400

    token = _get_token()
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    payload = {
        "BusinessShortCode": current_app.config["MPESA_SHORTCODE"],
        "Password": _stk_password(ts),
        "Timestamp": ts,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": current_app.config["MPESA_SHORTCODE"],
        "PhoneNumber": phone,
        "CallBackURL": current_app.config["MPESA_CALLBACK_URL"],
        "AccountReference": body.get("account_ref", "Christine Order"),
        "TransactionDesc": body.get("desc", "Payment for order"),
    }

    r = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        timeout=30,
    )
    data = r.json()
    _save_pdf("STK Push Request", data, "stk")
    return jsonify(data)

@mpesa_bp.route("/callback", methods=["POST"])
def callback():
    payload = request.get_json(force=True)
    _save_pdf("M-Pesa Callback", payload, "callback")
    return jsonify({"ok": True, "payload": payload})

# --- Helper for direct call from checkout ---
def trigger_stk_push(phone_number, amount, account_ref="order"):
    phone = _format_phone(phone_number)
    if not phone:
        return {"error": "Invalid phone number"}

    token = _get_token()
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    payload = {
        "BusinessShortCode": current_app.config["MPESA_SHORTCODE"],
        "Password": _stk_password(ts),
        "Timestamp": ts,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,
        "PartyB": current_app.config["MPESA_SHORTCODE"],
        "PhoneNumber": phone,
        "CallBackURL": current_app.config["MPESA_CALLBACK_URL"],
        "AccountReference": str(account_ref),
        "TransactionDesc": "Cosmetics order",
    }

    r = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        timeout=30,
    )
    data = r.json()
    _save_pdf("STK Push Direct", data, "direct")
    return data
