
# Import required modules
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///commodities.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Commodity model
class Commodity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    starting_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    seller = db.relationship('Seller', backref=db.backref('commodities', lazy=True))

# Define the Seller model
class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create the database tables
db.create_all()

# Define the home page route
@app.route('/')
def home():
    return render_template('index.html')

# Define the seller dashboard route
@app.route('/seller_dashboard')
def seller_dashboard():
    return render_template('seller_dashboard.html')

# Define the user dashboard route
@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')

# Define the commodity creation route
@app.route('/list_commodity', methods=['GET', 'POST'])
def list_commodity():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        starting_price = request.form['starting_price']
        seller_id = request.form['seller_id']
        commodity = Commodity(name=name, description=description, starting_price=starting_price, seller_id=seller_id)
        db.session.add(commodity)
        db.session.commit()
        flash('Commodity listed successfully!')
        return redirect(url_for('seller_dashboard'))
    return render_template('list_commodity.html')

# Define the commodity browsing route
@app.route('/browse_commodities')
def browse_commodities():
    commodities = Commodity.query.all()
    return render_template('browse_commodities.html', commodities=commodities)

# Define the bidding page route
@app.route('/bidding_page/<int:commodity_id>')
def bidding_page(commodity_id):
    commodity = Commodity.query.get_or_404(commodity_id)
    return render_template('bidding_page.html', commodity=commodity)

# Define the bid placement route
@app.route('/place_bid', methods=['POST'])
def place_bid():
    commodity_id = request.form['commodity_id']
    bid_amount = request.form['bid_amount']
    commodity = Commodity.query.get_or_404(commodity_id)
    if bid_amount > commodity.current_price:
        commodity.current_price = bid_amount
        db.session.commit()
        flash('Bid placed successfully!')
    else:
        flash('Bid amount must be greater than the current price!')
    return redirect(url_for('bidding_page', commodity_id=commodity_id))

# Define the bid management route
@app.route('/manage_bids')
def manage_bids():
    commodities = Commodity.query.filter_by(seller_id=request.args.get('seller_id')).all()
    return render_template('manage_bids.html', commodities=commodities)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
