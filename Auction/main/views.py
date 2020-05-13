from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from Auction.models import Auction
from Auction.helpers.categories import choices
from Auction.main.forms import SelectCategoryForm
main = Blueprint('main', __name__)

@main.route('/',  methods=['GET', 'POST'])
def index():
    form = SelectCategoryForm()
    page = request.args.get('page', 1, type=int)

    if form.validate_on_submit():

        if form.category.data == "all_categories":
            auctions = Auction.query.order_by(Auction.id.desc()).paginate(page=page, per_page=12)
            return render_template('index.html', auctions=auctions, form=form)

        auctions = Auction.query.filter_by(category=form.category.data).order_by(Auction.id.desc()).paginate(page=page, per_page=12)
        return render_template('index.html', auctions=auctions, form=form)
        

    auctions = Auction.query.order_by(Auction.id.desc()).paginate(page=page, per_page=12)
    return render_template('index.html', auctions=auctions, form=form)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

    
