import os
os.environ["GOOGLE_CLOUD_PROJECT"] = "admissionform-4ecb3"

from flask import Flask, render_template, request, redirect, session, jsonify
import firebase_admin
from firebase_admin import credentials, auth, firestore

app = Flask(__name__)
app.secret_key = "secret123"

# Firebase Admin SDK Initialization (Lazy)
_db = None
_auth_initialized = False

def init_firebase():
    global _auth_initialized
    if not _auth_initialized:
        try:
            cred = credentials.Certificate("firebase-key.json")
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            _auth_initialized = True
        except Exception as e:
            print(f"Firebase initialization error: {e}")
            raise

def get_db():
    global _db
    init_firebase()
    if _db is None:
        _db = firestore.client()
    return _db


# ---------------- HOME (LOGIN PAGE) ----------------
@app.route("/")
def home():
    return render_template("login.html")


# ---------------- SIGNUP PAGE ----------------
@app.route("/signup")
def signup_page():
    return render_template("signup.html")


# ---------------- VERIFY TOKEN ----------------
@app.route("/verify", methods=["POST"])
def verify():
    try:
        init_firebase()  # Ensure Firebase is initialized
        token = request.json.get("token")
        if not token:
            return jsonify({"status": "error", "message": "No token provided"}), 400
        decoded = auth.verify_id_token(token)
        session["user"] = decoded["email"]
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"Token verification error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 401


# ---------------- ADMISSION ----------------
@app.route("/admission", methods=["GET", "POST"])
def admission():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        data = request.form.to_dict()
        data["email"] = session["user"]
        get_db().collection("admissions").add(data)
        return redirect("/result")

    return render_template("admission.html", user=session["user"])


# ---------------- RESULT ----------------
@app.route("/result")
def result():
    if "user" not in session:
        return redirect("/")

    docs = get_db().collection("admissions").stream()
    data = [doc.to_dict() for doc in docs]
    return render_template("result.html", data=data, user=session["user"])


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
