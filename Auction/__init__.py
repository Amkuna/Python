from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from Auction.helpers.categories import choices
import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app)
db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from Auction.users.views import users
app.register_blueprint(users)

from Auction.main.views import main
app.register_blueprint(main)

from Auction.auctions.views import auction_view
app.add_url_rule('/add-auction/', view_func=auction_view, methods=['GET', 'POST'])

from Auction.auctions.views import auctions
app.register_blueprint(auctions)

from Auction.models import Offer, Auction, User

@app.context_processor
def categories():
    return dict(choices)

#check time every second
@socketio.on('auction_finished')
def handle_auction_finish(auction_id):
    auction = Auction.query.filter_by(id=auction_id).first()
    end_day = auction.end_day
    end_time = auction.end_time
    
    today = datetime.datetime.now()
    rd = relativedelta(end_day, today)
    print(rd)
    if rd.seconds <= 0:
        maxOffer = Offer.query.filter_by(auction_id=auction_id).order_by(Offer.price.desc()).first()
        if maxOffer:
            user = User.query.filter_by(id=maxOffer.user_id).first()
            emit("auction_finish_result", {'success': 'yep', 'maxOffer': maxOffer.price, 'user': user.username}, broadcast=True)
        else:
            emit("auction_finish_result", {'maxOffer': None}, broadcast=True)
    else:
        emit("auction_finish_result", {'error': "Auction is not finished"}, broadcast=True)

@socketio.on('message')
def handle_message(json):
    print("Received message: " + str(json))
    # return 'one', 2
    send(json, broadcast=True) #sends to all the clients

@socketio.on('bid')
def handle_bid(bid, prevBid, auction_id, user_id):
    auction = Auction.query.filter_by(id=auction_id).first()
    new_max_bid = False
    if prevBid == 'None':
        prevBid = auction.min_price
        if int(bid) >= int(prevBid):
            new_max_bid = True
            new_offer = Offer(
                auction_id=auction_id,
                user_id=user_id,
                price=bid
            )
            db.session.add(new_offer)
            db.session.commit()
            emit('bid_result', {"id": new_offer.id, "bid": new_offer.price}, broadcast=True)
            
    elif( (not auction.offers and int(bid) > int(auction.min_price)) or 
            (auction.offers and int(bid) > int(prevBid)) ):
        new_max_bid = True
        new_offer = Offer(
            auction_id=auction_id,
            user_id=user_id,
            price=bid
        )
        db.session.add(new_offer)
        db.session.commit()
        emit('bid_result', {"id": new_offer.id, "bid": new_offer.price}, broadcast=True)
    else:
        emit('bid_result', {'error': 'Offer must be at least ' + str(prevBid)}, broadcast=True)
        




