class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(100))

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True