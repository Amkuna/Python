from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from Auction.models import Auction
main = Blueprint('main', __name__)

@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    auctions = Auction.query.order_by(Auction.id.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', auctions=auctions)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

    
