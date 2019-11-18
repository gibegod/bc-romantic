from flask import url_for
from flask_login import UserMixin
from slugify import slugify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update
from werkzeug.security import generate_password_hash, check_password_hash
from run import db


class User(db.Model, UserMixin):

    __tablename__ = '_user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
 
class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('_user.id', ondelete='CASCADE'), nullable=False)
    address = db.Column(db.String(50), nullable =False)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable =False)
    price = db.Column(db.Integer, nullable = False)
    onSale = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Contract {self.address}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                count += 1

    @staticmethod
    def get_by_address(address):
        return Contract.query.filter_by(address=address).first()
    
    @staticmethod
    def get_by_idowner(owner_id):
        return Contract.query.filter_by(owner_id=owner_id).all()

    @staticmethod
    def get_by_id(id):
        return Contract.query.filter_by(id=id).first()

    @staticmethod
    def get_all():
        return Contract.query.all()

    @staticmethod 
    def onSale_True(self):
        stmt = (update(Contract)
            .where(Contract.id == self.id)
            .values(onSale= True)
             )
        db.session.execute(stmt)
        db.session.commit()
    
    @staticmethod 
    def onSale_False(self):
        stmt = (update(Contract)
            .where(Contract.id == self.id)
            .values(onSale= False)
             )
        db.session.execute(stmt)
        db.session.commit()

    @staticmethod 
    def update_idowner(self, newowner_id):
        stmt = (update(Contract)
            .where(Contract.id == self.id)
            .values(owner_id= newowner_id)
             )
        db.session.execute(stmt)
        db.session.commit()

    @staticmethod #updates metodos
    def update_title(self, newtitle):
        stmt = (update(Contract)
            .where(Contract.id == self.id)
            .values(title= newtitle)
             )
        db.session.execute(stmt)
        db.session.commit()
    
    @staticmethod #updates metodos
    def update_description(self, newdescription):
        stmt = (update(Contract)
            .where(Contract.id == self.id)
            .values(description= newdescription)
             )
        db.session.execute(stmt)
        db.session.commit()
    
    @staticmethod #updates metodos
    def update_price(self, newprice):
        stmt = (update(Contract)
            .where(Contract.id == self.id)
            .values(price= newprice)
             )
        db.session.execute(stmt)
        db.session.commit()


class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    owner_id = db.Column(db.Integer, db.ForeignKey('_user.id', ondelete='CASCADE'), nullable=False)
    key = db.Column(db.String(70), nullable =False)

    def __repr__(self):
        return f'<Wallet {self.id}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                count += 1

    @staticmethod
    def get_by_id(id):
        return Wallet.query.filter_by(id=id).first()
    
    @staticmethod
    def get_by_idowner(owner_id):
        return Wallet.query.filter_by(owner_id=owner_id).all()

    @staticmethod
    def get_by_idownerunico(owner_id):
        return Wallet.query.filter_by(owner_id=owner_id).first()

    @staticmethod
    def get_all():
        return Wallet.query.all()
    