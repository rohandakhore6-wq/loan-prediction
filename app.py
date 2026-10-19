import pickle
import numpy as np
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Load the trained model
model = pickle.load(open('logistic.pkl', 'rb'))

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rohan's AI Platform | Loan Estimator</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --accent: #ec4899;
            --bg-gradient: radial-gradient(circle at top left, #1e1b4b, #0f172a, #020617);
            --card-bg: rgba(30, 41, 59, 0.65);
            --border-color: rgba(255, 255, 255, 0.12);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        body {
            background: var(--bg-gradient);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
        }

        /* Navbar / Branding Header */
        .navbar {
            width: 100%;
            max-width: 900px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 25px;
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            margin-bottom: 25px;
        }

        .brand-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 800;
            font-size: 20px;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #a855f7, #6366f1, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .brand-logo i {
            font-size: 24px;
            color: #a855f7;
            -webkit-text-fill-color: initial;
        }

        .badge {
            background: rgba(99, 102, 241, 0.2);
            color: #818cf8;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            border: 1px solid rgba(99, 102, 241, 0.3);
        }

        /* Container & Glassmorphism */
        .container {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            padding: 35px 40px;
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            width: 100%;
            max-width: 900px;
            animation: slideUp 0.8s ease-out;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .header-title {
            text-align: center;
            margin-bottom: 30px;
        }

        .header-title h1 {
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 8px;
            background: linear-gradient(to right, #ffffff, #cbd5e1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header-title p {
            color: var(--text-muted);
            font-size: 15px;
        }

        /* Form Styling */
        .form-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 22px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }

        .form-group.full-width {
            grid-column: span 2;
        }

        label {
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 13px;
            color: #cbd5e1;
            display: flex;
            justify-content: space-between;
        }

        .slider-val {
            color: #818cf8;
            font-weight: 700;
        }

        input, select {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid var(--border-color);
            color: #ffffff;
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 14px;
            outline: none;
            transition: all 0.3s ease;
        }

        input:focus, select:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
            background: rgba(15, 23, 42, 0.9);
        }

        select option {
            background: #0f172a;
            color: white;
        }

        button.btn-submit {
            grid-column: span 2;
            background: linear-gradient(135deg, #6366f1, #a855f7);
            color: white;
            border: none;
            padding: 16px;
            font-size: 16px;
            font-weight: 700;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.5);
            margin-top: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
        }

        button.btn-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px -5px rgba(99, 102, 241, 0.7);
        }

        /* Result & Features Cards */
        .result-section {
            margin-top: 30px;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }

        .result-card {
            grid-column: span 2;
            padding: 20px;
            border-radius: 16px;
            text-align: center;
            font-size: 20px;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }

        .approved {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.4);
        }

        .rejected {
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.4);
        }

        .feature-box {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 20px;
            text-align: center;
        }

        .feature-box h4 {
            font-size: 14px;
            color: var(--text-muted);
            margin-bottom: 8px;
        }

        .feature-box .value {
            font-size: 22px;
            font-weight: 800;
            color: #38bdf8;
        }

        .btn-print {
            grid-column: span 2;
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.2s;
        }

        .btn-print:hover {
            color: white;
            background: rgba(255, 255, 255, 0.05);
        }

        /* Footer */
        .footer {
            margin-top: 30px;
            color: var(--text-muted);
            font-size: 13px;
            text-align: center;
        }

        .footer a {
            color: #818cf8;
            text-decoration: none;
            font-weight: 600;
        }

        @media (max-width: 768px) {
            .form-grid, .result-section {
                grid-template-columns: 1fr;
            }
            .form-group.full-width, button.btn-submit, .result-card, .btn-print {
                grid-column: span 1;
            }
        }
    </style>
</head>
<body>

    <!-- Navbar -->
    <div class="navbar">
        <div class="brand-logo">
            <i class="fa-solid fa-microchip"></i> Rohan's AI Platform
        </div>
        <div class="badge">Next-Gen ML Model</div>
    </div>

    <!-- Main Card -->
    <div class="container">
        <div class="header-title">
            <h1>Loan Eligibility & Analytics</h1>
            <p>Powered by Advanced Logistic Regression & Real-time Risk Engine</p>
        </div>

        <form action="/predict" method="POST">
            <div class="form-grid">
                <div class="form-group">
                    <label for="Gender"><i class="fa-solid fa-user"></i> Gender</label>
                    <select name="Gender" id="Gender" required>
                        <option value="1" {% if inputs and inputs['Gender']==1 %}selected{% endif %}>Male</option>
                        <option value="0" {% if inputs and inputs['Gender']==0 %}selected{% endif %}>Female</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="Married"><i class="fa-solid fa-heart"></i> Marital Status</label>
                    <select name="Married" id="Married" required>
                        <option value="1" {% if inputs and inputs['Married']==1 %}selected{% endif %}>Married</option>
                        <option value="0" {% if inputs and inputs['Married']==0 %}selected{% endif %}>Unmarried</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="Dependents"><i class="fa-solid fa-users"></i> Dependents</label>
                    <select name="Dependents" id="Dependents" required>
                        <option value="0" {% if inputs and inputs['Dependents']==0 %}selected{% endif %}>0</option>
                        <option value="1" {% if inputs and inputs['Dependents']==1 %}selected{% endif %}>1</option>
                        <option value="2" {% if inputs and inputs['Dependents']==2 %}selected{% endif %}>2</option>
                        <option value="3" {% if inputs and inputs['Dependents']==3 %}selected{% endif %}>3+</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="Education"><i class="fa-solid fa-graduation-cap"></i> Education</label>
                    <select name="Education" id="Education" required>
                        <option value="1" {% if inputs and inputs['Education']==1 %}selected{% endif %}>Graduate</option>
                        <option value="0" {% if inputs and inputs['Education']==0 %}selected{% endif %}>Not Graduate</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="Self_Employed"><i class="fa-solid fa-briefcase"></i> Self Employed</label>
                    <select name="Self_Employed" id="Self_Employed" required>
                        <option value="1" {% if inputs and inputs['Self_Employed']==1 %}selected{% endif %}>Yes</option>
                        <option value="0" {% if inputs and inputs['Self_Employed']==0 %}selected{% endif %}>No</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="Property_Area"><i class="fa-solid fa-building-user"></i> Property Area</label>
                    <select name="Property_Area" id="Property_Area" required>
                        <option value="2" {% if inputs and inputs['Property_Area']==2 %}selected{% endif %}>Urban</option>
                        <option value="1" {% if inputs and inputs['Property_Area']==1 %}selected{% endif %}>Semiurban</option>
                        <option value="0" {% if inputs and inputs['Property_Area']==0 %}selected{% endif %}>Rural</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="ApplicantIncome"><i class="fa-solid fa-wallet"></i> Applicant Income ($)</label>
                    <input type="number" step="any" name="ApplicantIncome" id="ApplicantIncome" placeholder="e.g. 5000" value="{{ inputs['ApplicantIncome'] if inputs else '' }}" required>
                </div>

                <div class="form-group">
                    <label for="CoapplicantIncome"><i class="fa-solid fa-hand-holding-dollar"></i> Coapplicant Income ($)</label>
                    <input type="number" step="any" name="CoapplicantIncome" id="CoapplicantIncome" placeholder="e.g. 1500" value="{{ inputs['CoapplicantIncome'] if inputs else '' }}" required>
                </div>

                <div class="form-group">
                    <label for="LoanAmount"><i class="fa-solid fa-sack-dollar"></i> Loan Amount (in $1,000s)</label>
                    <input type="number" step="any" name="LoanAmount" id="LoanAmount" placeholder="e.g. 150 (for $150k)" value="{{ inputs['LoanAmount'] if inputs else '' }}" required>
                </div>

                <div class="form-group">
                    <label for="Loan_Amount_Term"><i class="fa-solid fa-calendar-days"></i> Loan Term (Months)</label>
                    <input type="number" step="any" name="Loan_Amount_Term" id="Loan_Amount_Term" placeholder="e.g. 360" value="{{ inputs['Loan_Amount_Term'] if inputs else '360' }}" required>
                </div>

                <div class="form-group full-width">
                    <label for="Credit_History"><i class="fa-solid fa-chart-line"></i> Credit History Score</label>
                    <select name="Credit_History" id="Credit_History" required>
                        <option value="1" {% if inputs and inputs['Credit_History']==1 %}selected{% endif %}>Excellent (1.0 - Good credit standing)</option>
                        <option value="0" {% if inputs and inputs['Credit_History']==0 %}selected{% endif %}>Poor (0.0 - Defaults present)</option>
                    </select>
                </div>

                <button type="submit" class="btn-submit">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> Predict Approval Status
                </button>
            </div>
        </form>

        {% if prediction_text is not none %}
            <div class="result-section">
                <div class="result-card {% if prediction_text == 'Approved' %}approved{% else %}rejected{% endif %}">
                    {% if prediction_text == 'Approved' %}
                        <i class="fa-solid fa-circle-check"></i> Loan Status: Approved
                    {% else %}
                        <i class="fa-solid fa-circle-xmark"></i> Loan Status: Rejected
                    {% endif %}
                </div>

                <div class="feature-box">
                    <h4>Estimated Monthly EMI</h4>
                    <div class="value">${{ emi }}</div>
                </div>

                <div class="feature-box">
                    <h4>AI Risk Meter</h4>
                    <div class="value" style="color: {% if risk == 'Low Risk' %}#34d399{% elif risk == 'Moderate Risk' %}#fbbf24{% else %}#f87171{% endif %};">
                        {{ risk }}
                    </div>
                </div>

                <button class="btn-print" onclick="window.print()">
                    <i class="fa-solid fa-print"></i> Download Summary PDF
                </button>
            </div>
        {% endif %}
    </div>

    <!-- Footer Branding -->
    <div class="footer">
        Crafted with ❤️ by <a href="#">Rohan Dakhore</a> &copy; 2026 Rohan's AI Platform
    </div>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE, prediction_text=None, inputs=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        gender = float(request.form['Gender'])
        married = float(request.form['Married'])
        dependents = float(request.form['Dependents'])
        education = float(request.form['Education'])
        self_employed = float(request.form['Self_Employed'])
        applicant_income = float(request.form['ApplicantIncome'])
        coapplicant_income = float(request.form['CoapplicantIncome'])
        loan_amount = float(request.form['LoanAmount'])
        loan_term = float(request.form['Loan_Amount_Term'])
        credit_history = float(request.form['Credit_History'])
        property_area = float(request.form['Property_Area'])

        features = [
            gender, married, dependents, education, self_employed,
            applicant_income, coapplicant_income, loan_amount,
            loan_term, credit_history, property_area
        ]
        
        final_features = np.array([features])
        prediction = model.predict(final_features)
        
        output = 'Approved' if prediction[0] == 1 or prediction[0] == 'Y' else 'Rejected'

        # Feature: Calculate Monthly EMI (assuming 8.5% annual interest)
        P = loan_amount * 1000
        r = 0.085 / 12
        n = loan_term if loan_term > 0 else 360
        emi_val = (P * r * ((1 + r)**n)) / (((1 + r)**n) - 1) if P > 0 else 0
        emi_formatted = f"{emi_val:,.2f}"

        # Feature: Calculate Risk Indicator
        total_income = applicant_income + coapplicant_income
        if credit_history == 1 and (P / (total_income + 1)) < 30:
            risk = "Low Risk"
        elif credit_history == 1:
            risk = "Moderate Risk"
        else:
            risk = "High Risk"

        inputs_data = {
            'Gender': gender, 'Married': married, 'Dependents': dependents,
            'Education': education, 'Self_Employed': self_employed,
            'ApplicantIncome': applicant_income, 'CoapplicantIncome': coapplicant_income,
            'LoanAmount': loan_amount, 'Loan_Amount_Term': loan_term,
            'Credit_History': credit_history, 'Property_Area': property_area
        }

        return render_template_string(
            HTML_PAGE, 
            prediction_text=output, 
            emi=emi_formatted, 
            risk=risk,
            inputs=inputs_data
        )
    except Exception as e:
        return render_template_string(HTML_PAGE, prediction_text=f"Error: {str(e)}", inputs=None)

if __name__ == '__main__':
    app.run(debug=True)
