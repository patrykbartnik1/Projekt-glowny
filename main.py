from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SECRET_KEY'] = 'tajny_klucz_do_formularzy'
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))
    category = db.Column(db.String(50))
    amount = db.Column(db.Float)
    description = db.Column(db.String(200))
    receipt = db.Column(db.String(200))  # Dowód zakupu

@app.route('/')
def index():
    transactions = Transaction.query.all()
    balance = sum([t.amount if t.type == 'income' else -t.amount for t in transactions])
    return render_template('index.html', transactions=transactions, balance=balance)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        t_type = request.form['type']
        category = request.form['category']
        amount = float(request.form['amount'])
        description = request.form['description']
        receipt = request.form['receipt']
        new_transaction = Transaction(
            type=t_type, category=category,
            amount=amount, description=description,
            receipt=receipt
        )
        db.session.add(new_transaction)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    transaction = Transaction.query.get_or_404(id)
    if request.method == 'POST':
        transaction.type = request.form['type']
        transaction.category = request.form['category']
        transaction.amount = float(request.form['amount'])
        transaction.description = request.form['description']
        transaction.receipt = request.form['receipt']
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', transaction=transaction)

@app.route('/delete/<int:id>')
def delete(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
