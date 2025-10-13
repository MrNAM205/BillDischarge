from flask import Flask, request
from packages.backend.config import config
from packages.backend.models import Bill, db

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/bills', methods=['POST'])
def add_bill():
    data = request.get_json()
    new_bill = Bill(bill_number=data['bill_number'], amount=data['amount'])
    db.session.add(new_bill)
    db.session.commit()
    return 'Bill added successfully!'

if __name__ == '__main__':
    app.run(debug=True)
