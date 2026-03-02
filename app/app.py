from flask import Flask, request

app = Flask(__name__)

@app.get("/")
def home():
    return "Hello Kevin — ZAP target is running."

@app.get("/search")
def search():
    q = request.args.get("q", "")
    return f"You searched for: {q}"

@app.after_request
def add_security_headers(response):
    #Anti-clickjacking
    response.headers["X-Frame-Options"] = "DENY"

    #Basic CSP (safe starter policy for simple apps)
    response.headers["Content-Security-Policy"] = "default-src 'self'"

    #Nice extra hardening (common baseline)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
