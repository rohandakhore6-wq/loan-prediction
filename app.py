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
    <title>Loan Eligibility Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            --card-bg: rgba(30, 41, 59, 0.7);
            --border-color: rgba(255, 255, 255, 0.1);
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
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            width: 100%;
            max-width: 700px;
            animation: fadeIn 0.8s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h2 {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(to right, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        .header p {
            color: var(--text-muted);
            font-size: 14px;
        }

        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }

        .form-group.full-width {
            grid-column: span 2;
        }

        label {
            font-weight: 500;
            margin-bottom: 8px;
            font-size: 13px;
            color: #cbd5e1;
            letter-spacing: 0.3px;
        }

        input, select {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-color);
            color: white;
            padding: 12px 16px;
            border-radius: 10px;
            font-size: 14px;
            outline: none;
            transition: all 0.3s ease;
        }

        input::placeholder {
            color: #475569;
        }

        input:focus, select:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15);
            background: rgba(15, 23, 42, 0.9);
        }

        select option {
            background: #0f172a;
            color: white;
        }

        button {
            grid-column: span 2;
            background: linear-gradient(135deg, var(--primary), #818cf8);
            color: white;
            border: none;
            padding: 14px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
            margin-top: 10px;
        }

        button:hover {
            background: linear-gradient(135deg, var(--primary-hover), #6366f1);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
        }

        .result-card {
            margin-top: 25px;
            padding: 18px;
            border-radius: 12px;
            text-align: center;
            font-size: 17px;
            font-weight: 600;
            animation: popUp 0.5s ease-in-out;
        }

        @keyframes popUp {
            0% { transform: scale(0.9); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }

        .approved {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
            box-shadow: 0 4px 20px rgba(16, 185, 129, 0.1);
        }

        .rejected {
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
            box-shadow: 0 4px 20px rgba(239, 68, 68, 0.1);
        }

        @media (max-width: 650px) {
            .container {
                padding: 20px;
            }
            .form-grid {
                grid-template-columns: 1fr;
            }
            .form-group.full-width, button {
                grid-column: span 1;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Smart Loan Estimator</h2>
            <p>Enter your details below to check instant loan approval status</p>
        </div>

        <form action="/predict" method="POST">
            <div class="form-grid">
                <div class="form-group">
                    <label for="Gender">Gender</label>
                    <select name="Gender" id="Gender" required>
                        <option value="1">Male</option>
                        <option value="0">Female</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="Married">Marital Status</label>
                    <select name="Married" id="Married" required>
                        <option value="1">Married</option>
                        <option value="0">Unmarried</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="Dependents">Dependents</label>
                    <select name="Dependents" id="Dependents" required>
                        <option value="0">0</option>
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3+</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="Education">Education</label>
                    <select name="Education" id="Education" required>
                        <option value="1">Graduate</option>
                        <option value="0">Not Graduate</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="Self_Employed">Self Employed</label>
                    <select name="Self_Employed" id="Self_Employed" required>
                        <option value="1">Yes</option>
                        <option value="0">No</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="Property_Area">Property Area</label>
                    <select name="Property_Area" id="Property_Area" required>
                        <option value="2">Urban</option>
                        <option value="1">Semiurban</option>
                        <option value="0">Rural</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="ApplicantIncome">Applicant Income ($)</label>
                    <input type="number" step="any" name="ApplicantIncome" id="ApplicantIncome" placeholder="e.g., 5000" required>
                </div>

                <div class="form-group">
                    <label for="CoapplicantIncome">Coapplicant Income ($)</label>
                    <input type="number" step="any" name="CoapplicantIncome" id="CoapplicantIncome" placeholder="e.g., 0" required>
                </div>

                <div class="form-group">
                    <label for="LoanAmount">Loan Amount (in thousands)</label>
                    <input type="number" step="any" name="LoanAmount" id="LoanAmount" placeholder="e.g., 150" required>
                </div>

                <div class="form-group">
                    <label for="Loan_Amount_Term">Loan Term (Months)</label>
                    <input type="number" step="any" name="Loan_Amount_Term" id="Loan_Amount_Term" placeholder="e.g., 360" required>
                </div>

                <div class="form-group full-width">
                    <label for="Credit_History">Credit History</label>
                    <select name="Credit_History" id="Credit_History" required>
                        <option value="1">Good (All debts paid on time)</option>
                        <option value="0">Bad (History of defaults)</option>
                    </select>
                </div>

                <button type="submit">Check Eligibility</button>
            </div>
        </form>

        {% if prediction_text is not none %}
            <div class="result-card {% if prediction_text == 'Approved' %}approved{% else %}rejected{% endif %}">
                {% if prediction_text == 'Approved' %}
                    🎉 Congratulations! Your Loan is Approved.
                {% else %}
                    ⚠️ Sorry, Your Loan Application is Rejected.
                {% endif %}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE, prediction_text=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = [
            float(request.form['Gender']),
            float(request.form['Married']),
            float(request.form['Dependents']),
            float(request.form['Education']),
            float(request.form['Self_Employed']),
            float(request.form['ApplicantIncome']),
            float(request.form['CoapplicantIncome']),
            float(request.form['LoanAmount']),
            float(request.form['Loan_Amount_Term']),
            float(request.form['Credit_History']),
            float(request.form['Property_Area'])
        ]
        
        final_features = np.array([features])
        prediction = model.predict(final_features)
        
        output = 'Approved' if prediction[0] == 1 or prediction[0] == 'Y' else 'Rejected'
        
        return render_template_string(HTML_PAGE, prediction_text=output)
    except Exception as e:
        return render_template_string(HTML_PAGE, prediction_text=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
