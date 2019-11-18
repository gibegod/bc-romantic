# login-blockchain
Pasos: 
1. Crear una base de datos en MySQL con el nombre 'mercadoblockchain'.
2. Modificar el run.py con tus datos (mysql+pqmysql://user:password@host/database).
3. Crear un ambiente e instalar los paquetes ejecutando el siguiente comando: pip install -r requierements.txt
4. Instalar en consola:
npm install truffle
pip install web3
5. Dentro de la consola escribir 'python3', y luego:
>>> from run import db

>>> db.create_all()
6. Instalar los siguientes paquetes en la consola:
npm install -g vue-cli
npm install --save axios
pip install -U flask-cors
7. Ejecutar los siguientes comandos:
set "FLASK_APP=run.py"
set "FLASK_ENV=development"
8. Ejecutar 'flask run'.
9. Dirigirse a localhost:5000 y la magia ocurrira.

Base de datos en local: 'mysql+pymysql://root:@localhost/mercadoblockchain'
Base de datos en web: 'mysql+pymysql://gibegod:lopez999@gibegod.mysql.pythonanywhere-services.com/gibegod$miniblog'

Issues server: https://codigofacilito.com/articulos/integracion-vue-flask
