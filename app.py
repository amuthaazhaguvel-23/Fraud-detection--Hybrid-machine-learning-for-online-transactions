from flask import Flask, request, render_template, redirect, url_for, session
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = "secret123"

# Load model
model = pickle.load(open("model.pkl", "rb"))

# ---------------- LOGIN ----------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "1234":
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Login"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template("dashboard.html")
    return redirect(url_for('login'))


# ---------------- PREDICTION PAGE ----------------
@app.route('/predict_page')
def predict_page():
    if 'user' in session:
        return render_template("predict.html")
    return redirect(url_for('login'))


# ---------------- PREDICTION ----------------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        time = float(request.form['time'])
        amount = float(request.form['amount'])

        features = np.array([[time, amount]])
        prediction = model.predict(features)[0]

        result = "Fraud" if prediction == 1 else "Not Fraud"

        return render_template("result.html", prediction=result)

    except Exception as e:
        return str(e)


# ---------------- CHART PAGE ----------------
@app.route('/chart')
def chart():
    if 'user' in session:
        return render_template("chart.html")
    return redirect(url_for('login'))


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
