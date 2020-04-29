import datetime
from flask import redirect, url_for, render_template, session, request, Blueprint
from flask.views import MethodView
from Auction.auctions.forms import AddAuctionForm, EditAuctionForm
from Auction import db
# from models.user import User
from Auction.models import Auction, User
from flask_login import current_user, login_required
from .picture_handler import add_auction_image
from faker import Faker
from faker.providers import lorem, python, date_time, bank
auctions = Blueprint('auctions', __name__)

@auctions.route('/auctions/<int:id>')
def auction(id):
    auction = Auction.query.get_or_404(id)
    maxOffer = auction.min_price
    if not auction.offers:
        maxOffer = "None"
    for offer in auction.offers:
        if offer.price >= maxOffer:
            maxOffer = offer.price

    author = User.query.filter_by(id=auction.user_id).first()
    auction.views += 1
    db.session.commit()

    return render_template('auction.html', auction=auction, author=author, maxOffer=maxOffer)

@auctions.route('/my-auctions')
def my_auctions():
    page = request.args.get('page', 1, type=int)
    auctions = Auction.query.filter_by(user_id=current_user.id).order_by(Auction.id.desc()).paginate(page=page, per_page=5)
    return render_template('my_auctions.html', auctions=auctions)

@auctions.route('/auction/<int:id>/edit', methods=['GET', 'POST'])
def edit_auction(id):
    auction = Auction.query.get_or_404(id)

    if auction.user_id != current_user.id:
        abort(403)

    form = EditAuctionForm()
    if form.validate_on_submit():
        pic = 'default_image.jpg'
        if form.image.data:
            pic = add_auction_image(form.image.data)

        auction.name = form.name.data
        auction.category = form.category.data
        auction.description = form.description.data
        auction.country = form.country.data
        if auction.auction_image == 'default_image.jpg':
            auction.auction_image = pic
        db.session.commit()
        return redirect(url_for('auctions.auction', id=id))

    elif request.method == 'GET':
        form.name.data = auction.name
        form.category.data = auction.category
        form.description.data = auction.description
        form.country.data = auction.country
        form.image.data = auction.auction_image

    return render_template('edit_auction.html', form=form)

@auctions.route('/auction/<int:id>/delete')
def delete_auction(id):
    auction = Auction.query.get_or_404(id)
    if auction.user_id != current_user.id:
        abort(403)
    
    db.session.delete(auction)
    db.session.commit()
    return redirect(url_for('auctions.my_auctions'))

@auctions.route('/generate')
@login_required
def generate():
    fake = Faker()
    fake.add_provider(lorem)
    fake.add_provider(python)
    fake.add_provider(date_time)
    fake.add_provider(bank)
    for _ in range(5):
        time = datetime.datetime.strptime(fake.time(pattern='%H:%M', end_datetime=None), "%H:%M").time()
        print(type(time))
        new_auction = Auction(name=fake.name(),
                        category=fake.name(),
                        country=fake.bank_country(),
                        min_price=fake.pydecimal(left_digits=None, right_digits=2, positive=True, min_value=1, max_value=None),
                        auction_image='default_image.jpg',
                        end_day=fake.date_this_year(before_today=False, after_today=True),
                        end_time=time,
                        description=fake.paragraphs(nb=3, ext_word_list=None),
                        user_id=current_user.id)
        db.session.add(new_auction)
        
    db.session.commit()
    return render_template('index.html')


class CreateAuction(MethodView):
    def get(self):
        if not current_user.is_authenticated:
            return redirect(url_for('main.index'))

        form = AddAuctionForm()
        return render_template('add_auction.html', form=form)
    
    def post(self):
        form = AddAuctionForm()

        if form.validate_on_submit():
            pic = 'default_image.jpg'
            if form.image.data:
                pic = add_auction_image(form.image.data)
                
            end_day = datetime.datetime.strptime(str(form.end_day.data), '%Y-%m-%d')
            new_auction = Auction(name=form.name.data,
                                  category=form.category.data,
                                  country=form.country.data,
                                  min_price=form.min_price.data,
                                  auction_image=pic,
                                  end_day=end_day,
                                  end_time=form.end_time.data,
                                  description=form.description.data,
                                  user_id=current_user.id,
                                  views=0)
                                  
            db.session.add(new_auction)
            db.session.commit()
            print(new_auction.id)
            return redirect(url_for('auctions.auction', id=new_auction.id))
        print(form.errors)
        return render_template('add_auction.html', form=form)


auction_view = CreateAuction.as_view('auction_api')
