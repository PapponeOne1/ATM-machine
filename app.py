from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# Global variables for balance, correct PIN, and attempts
balance = 1052.34
correct_pin = 1234
attempts = 0
max_attempts = 3

@app.route('/')
def home():
    return render_template('pin.html')

@app.route('/validate_pin', methods=['POST'])
def validate_pin():
    global attempts
    pin = int(request.form['pin'])
    
    if pin == correct_pin:
        attempts = 0  # Reset attempts on correct PIN
        return redirect(url_for('menu'))
    else:
        attempts += 1
        if attempts >= max_attempts:
            return "Too many incorrect attempts. Your card has been blocked.", 403
        return render_template('pin.html', error="Incorrect PIN. Please try again.")

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/balance')
def check_balance():
    return render_template('balance.html', balance=balance)

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    global balance
    if request.method == 'POST':
        amount = float(request.form['amount'])
        balance += amount
        return render_template('menu.html', message=f"Deposit successful. New balance: £{balance:.2f}")
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    global balance
    if request.method == 'POST':
        amount = float(request.form['amount'])
        if amount > balance:
            return render_template('withdraw.html', error="Insufficient funds.")
        balance -= amount
        return render_template('menu.html', message=f"Withdrawal successful. New balance: £{balance:.2f}")
    return render_template('withdraw.html')

@app.route('/exit')
def exit():
    return "Thank you for using our ATM service. Goodbye!"

if __name__ == '__main__':
    app.run(debug=True)
