import datetime
from flask import redirect, url_for, render_tmeplate, session, request, Blueprint
from flask.views import MethodView
from form.auction_form import AuctionForm
from Auction import db
from models.user import User
from models.auction import Auction

auctions = Blueprint('auctions', __name__)

class CreateAuction(MethodView):
    def get(self):
        auction_form = AuctionForm()

        if session.get('username') is None:
            return redirect(url_for('index'))
        return render_template('create_auction.html', title='Create Auction', auction_form=auction_form)

    def post(self):
        auction_form = AuctionForm()
        end_day = datetime.datetime.strptime(auction_form.end_day.data, '%d-%m-%Y')

        if auction_form.validate_on_submit():
            current_user = User.query.filter_by(username=session.get('username')).first()

            image_path = auction_form.auction_image.data

            new_auction = Auction(name=auction_form.name.data,
                                  category=auction_form.category.data,
                                  town=auction_form.town.data,
                                  minimal_price=auction_form.minimal_price.data,
                                  auction_image=image_path,
                                  end_day=end_day,
                                  end_time=auction_form.end_time.data,
                                  description=auction_form.description.data,
                                  user_id=current_user.id)

            db.session.add(new_auction)
            db.session.commit()

            return redirect(url_for('auction', auction_id=Auction.query.order_by(Auction.id.desc()).first().id))
        else:
            return redirect(url_for('create_auction'))