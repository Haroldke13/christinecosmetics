from app import create_app

# Expose `app` for Gunicorn
app = create_app()

if __name__ == "__main__":
    # For local debugging only; Render uses Gunicorn with this file.
    app.run(host="0.0.0.0", port=5000)
