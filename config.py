import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "evalynemarch22")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://test:fEdVuETIqrHr1fCB@chatroom.5vtda.mongodb.net/GBCosmetics?retryWrites=true&w=majority&appName=GBCosmetics")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "geniusbabycosmetics")
    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "evalynemwende20")
    PER_PAGE = int(os.getenv("PER_PAGE", "12"))
     # M-Pesa
    MPESA_CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
    MPESA_CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")
    MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE", "174379")
    MPESA_PASSKEY = os.getenv("MPESA_PASSKEY")
    MPESA_CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL")

    # Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "1") in ("1", "true", "True")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)