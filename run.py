from flask import Flask, render_template, request, redirect, url_for, abort, flash, jsonify
from flask_cors import CORS
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse
from forms import SignupForm, LoginForm, ContractForm, WalletForm
import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from deployContract import newContract, movementHash, w3, abi, buyContract #contractAccount

app = Flask(__name__, static_folder = "./fronted/dist/static", template_folder = "./fronted/dist")
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/mercadoblockchain'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

login_manager = LoginManager(app)
login_manager.login_view = "login" #en caso de que no este identidicado, y la vista lo requiera te manda para aca
db = SQLAlchemy(app)

from models import User, Contract, Wallet

@app.route('/', defaults={'path': ''})

#@app.route('/')
#def dender_vue():
#    return login();

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    contracts = Contract.get_all()
    return render_template("index.html", contracts=contracts)


@app.route("/account", methods=['GET','POST'])
@login_required #añado en varios lugares el login_required, osea que es necesario estas registrado para que entren a estas rutas
def account():
    wallets = Wallet.get_by_idowner(current_user.id)
    form = WalletForm()
    if form.validate_on_submit():
        name = form.name.data
        key = form.key.data
        wallet = Wallet(name=name, owner_id=current_user.id, key = key)
        wallet.save()
        return redirect(url_for('account'))
    return render_template('myaccount.html', wallets=wallets, form=form)



@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    form = SignupForm(request.form)
    if request.method == 'POST':
        if form.validate():
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user is None:
                # Creamos el usuario y lo guardamos
                user = User(name=name, email=email)
                user.set_password(password)
                user.save()
                # Dejamos al usuario logueado
                login_user(user, remember=True)
                return redirect(url_for('account'))
            flash('A user already exists with that email address.')
            return redirect(url_for('show_signup_form'))
    return render_template("signup_form.html", form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user:
                if user.check_password(password=password):
                    login_user(user)
                    next = request.args.get('next')
                    return redirect(next or url_for('account'))
        flash('Invalid username/password combination')
        return redirect(url_for('login'))
    return render_template('login_form.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


#formulario para crear los contratos, tambien muestra los existentes
@app.route("/contract", methods=['GET','POST'], defaults={'id': None}) #defaults={'contract_id': None}
@app.route("/contract/<id>")
@login_required
def contract(id):
    contracts = Contract.get_by_idowner(current_user.id) #traigo todos los contratos del que este usuario es dueño
    form = ContractForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        price = form.price.data
        wallet = Wallet.get_by_idownerunico(current_user.id)
        contract_address = newContract(title, price, wallet.key) #inicio contrato y creo en la base de datos
        contract = Contract(owner_id= current_user.id, address = contract_address, title = title, description = description, price = price)
        contract.save()
        Contract.onSale_True(contract)
        return redirect(url_for('contract'))
    return render_template('contract.html', contracts=contracts, form=form)

@app.route("/wallet", methods=['GET','POST'])
@login_required
def wallet():
    wallets = Wallet.get_by_idowner(current_user.id)
    form = WalletForm()
    if form.validate_on_submit():
        name = form.name.data
        key = form.key.data
        wallet = Wallet(name=name, owner_id=current_user.id, key = key)
        wallet.save()
        return redirect(url_for('wallet'))
    return render_template('wallet.html', wallets=wallets, form=form)

@app.route ("/edit/<id>", methods= ['POST', 'GET'])
@login_required
def edit(id):
    contract = Contract.get_by_id(id)
    form = ContractForm()
    if contract.owner_id == current_user.id:
        return render_template('editar.html', contract = contract, form = form)
    flash ('No eres el dueño de este contrato')
    return render_template('contract.html')

@app.route ("/update/<id>", methods= ['POST', 'GET'])
@login_required
def update(id):
    contract = Contract.get_by_id(id)
    form = ContractForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        price = form.price.data

        Contract.update_title(contract, title)
        Contract.update_description(contract, description)
        Contract.update_price(contract, price)
        flash ('Contrato actualizado')
        return redirect(url_for('account'))
    flash ('No se pudo actualizar el contrato')
    return render_template('contract.html')

@app.route("/delete/<id>", methods=['GET','POST'] )
@login_required
def delete(id):
    contract = Contract.get_by_id(id)
    db.session.delete(contract)
    db.session.commit()
    flash('Contrato eliminado')
    return redirect (url_for('contract'))

@app.route("/buy/<id>", methods=['GET','POST'])
@login_required
def buy(id):

    contract = Contract.get_by_id(id) #instancio contrato 
    user = User.get_by_id(current_user.id) #instancio comprador
    if (contract.owner_id == current_user.id):
        flash('Usted es el dueño de este contrato')
        return render_template('newContract.html') 

    walletV =  Wallet.get_by_idownerunico(contract.owner_id) 
    acctV = w3.eth.account.privateKeyToAccount(walletV.key) #direccion vendedor

    walletC = Wallet.get_by_idownerunico(current_user.id)
    acctC = w3.eth.account.privateKeyToAccount(walletC.key) #direccion comprador

    signed_txn = w3.eth.account.signTransaction(dict(
    nonce=w3.eth.getTransactionCount(str(acctC.address)),
    gasPrice=w3.eth.gasPrice,
    gas=100000,
    to=str(acctV.address),  
    value=int(contract.price),
    data=b'',
    ),
    str(walletC.key),
    )
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    hash = w3.toHex(tx_receipt['transactionHash'])
    Contract.update_idowner(contract, current_user.id)
    Contract.onSale_False(contract)

    hash2= buyContract(acctC.address, contract.address)
    print (hash)
    print (hash2)
    flash('Contract adquired {hash}, {hash2}')
    return render_template('newContract.html', hash=hash, hash2 = hash2) #hash2 = hash2hash2 = hash2

@app.route("/contratosdisponibles" , methods=['GET'])
@login_required
def contratosdisponibles():

    availablecontracts = Contract.get_all()
    availablecontracts2 = []
    for availablecontract in availablecontracts:
        if availablecontract.onSale==True:
            if availablecontract.owner_id != current_user.id:
                availablecontracts2.append(availablecontract)
   
    return render_template('contratosdisponibles.html', availablecontracts=availablecontracts2)

@app.route("/onsale/<id>")
@login_required
def onSale(id):
    contract = Contract.get_by_id(id)
    if (contract.onSale==False):
        Contract.onSale_True(contract)
        flash('Contrato puesto a la venta')
        return redirect (url_for('contract'))
    
    flash ('El contrato ya se encuentra a la venta')
    return redirect (url_for('contract'))


    
        


