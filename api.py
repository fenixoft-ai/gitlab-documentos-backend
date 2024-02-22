from flask import Flask, request
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from functions_jwt import write_token, validate_token
from parser_register import parser_writer
from flask_restx import Resource, Api, fields#, reqparse
from flask_mail import Mail, Message
from email_sender import send

import bcrypt
import functions
import secrets

auth = HTTPTokenAuth(scheme='Bearer')

app = Flask(__name__)
api = Api(app, version='1.0', title='Documentos API', description='')
mail = Mail(app)

CORS(app)


#************************************************************************************************
#Parsers
#************************************************************************************************

'''parser_user = parser_writer([['email', str, 'the user email'], ['password', str, 'the user password'], \
            ['name', str, "the user name"], ['picture', str, "the user picture"]])'''

parser_roles_post = parser_writer([['name', str, 'the role name']])

parser_roles_put = parser_writer([['name', str, 'the role name']])

parser_organization_post = parser_writer([['email', str, 'the user email'], ['organization', str, 'the user organization']])

parser_organization_id_put = parser_writer([['name', str, 'the organization name']])

parser_user_organization_post = parser_writer([['email', str, 'the user email'], ['organization', str, 'the user organization'],['role', str, 'the user role']])

parser_user_organization_put = parser_writer([['organization', str, 'the user organization'],['role', str, 'the user role']])

parser_login_post = parser_writer([['email', str, 'the user email'],['password', str, 'the user password']])

'''parser_user.add_argument('email',type=str,help="the user email")'''

#************************************************************************************************
#Parsers - FIN
#************************************************************************************************

#************************************************************************************************
#Namespaces - Example: ns = api.namespace('prueba', description='prueba de namespace')
#************************************************************************************************

ns_organization = api.namespace('organization', description = 'manage organization')

ns_roles = api.namespace('role', description = 'manage roles')

ns_user_organization = api.namespace('user_organization', description = 'manage organization users')

ns_users = api.namespace('user', description = 'manage users')

ns_login = api.namespace('login', description = 'user login')

ns_password = api.namespace('password', description = 'manage password')

#************************************************************************************************
#Namespaces - FIN
#************************************************************************************************

#************************************************************************************************
#Models
#************************************************************************************************

user_model = api.model('user', {
    'email': fields.String(required=True, description='user email'),
    'password': fields.String(required=True, description='user password'),
    'name': fields.String(required=True, description='user name')#,
    #'picture': fields.String(required=False, description='user picture'),
})

login_model = api.model('login', {
    'email': fields.String(required=True, description='user email'),
    'password': fields.String(required=True, description='user password')
})

role_model = api.model('role', {
    'name': fields.String(required=True, description='role name')
})

organization_model = api.model('organization', {
    'email': fields.String(required=True, description='user email'),
    'organization': fields.String(required=True, description='user organization')
})

organization_id_model = api.model('organization_id', {
    'name': fields.String(required=True, description='organization name')
})

user_organization_model = api.model('user_organization', {
    'email': fields.String(required=True, description='user email'),
    'organization': fields.String(required=True, description='user organization'),
    'role': fields.String(required=True, description='user role')
})

user_organization_put_model = api.model('user_organization_put', {
    'organization': fields.Integer(required=True, description='user organization'),
    'role': fields.Integer(required=True, description='user role')
})

password_model = api.model('password_model', {
    'new_password': fields.String(required=True, description='user new password'),
    'confirm_password': fields.String(required=True, description='corfirm new password')
})

#************************************************************************************************
#Models - FIN
#************************************************************************************************

@auth.verify_token
def verify_token(token):
    
    if token:
        #decodificar el token para verificar que tiene la "huella"
        decoded = validate_token(token, True)#Falta confirmacion de prueba
        if decoded:
            valid = functions.user_token_get(token)
            if valid:
                record = functions.user_get_by_id(valid[1])
                if record:
                    user = {'id': record[0], 'uuid': record[1], 'email': record[2], 'name': record[4], 'picture': record[5]}
                    return user

def createJWT(user):
    #create JWT token
    jwt = write_token(user)
    return jwt

def cleanEmail(email):
    email = email.lower().strip()
    return email

@api.route('/hello')
class hello_world(Resource):
    def get(self):
        #auth.current_user()
        return {'hey': 'you'}
    
#def hello_world():
    #return 'Hey you!'

    #Validacion de Token
    '''token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjksInV1aWQiOiI4NzNmOTI2Yy1jMjdiLTExZWQtOWJmZC0xODY2ZGEwZjdjMWEiLCJlbWFpbCI6InBAZG9tYWluLmNvbSIsIm5hbWUiOiJKZWFuMjUiLCJwaWN0dXJlIjoiIiwiZXhwIjoxNjc4OTY1NTMyfQ.3q5oeJL8ehkO36z6864DVLIyP0DoyH3I59eDRv8UpZE"
    #token="eJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjksInV1aWQiOiI4NzNmOTI2Yy1jMjdiLTExZWQtOWJmZC0xODY2ZGEwZjdjMWEiLCJlbWFpbCI6InBAZG9tYWluLmNvbSIsIm5hbWUiOiJKZWFuMjUiLCJwaWN0dXJlIjoiIiwiZXhwIjoxNjc4OTY1NTMyfQ.3q5oeJL8ehkO36z6864DVLIyP0DoyH3I59eDRv8UpZE"

    if token:
        #decodificar el token para verificar que tiene la "huella"
        decoded = validate_token(token, True)
        return decoded
    return decoded'''

#Login
@ns_login.route('/')#, methods=['POST'])
#def login():
class user(Resource):
    
    #@ns_login.doc(parser = parser_login_post)
    @ns_login.doc('user_post')#parser = parser_user)
    @ns_login.expect(login_model)
    #@auth.login_required
    def post(self):
    #vars = request.get_json()
    #aaa
        out = {'status': False}
        #vars = parser_user.parse_args()
        vars = request.get_json(force=True)    
        email = cleanEmail(vars['email'])
        password = vars['password']
        record = functions.user_get_by_email(email)
        print("Documentos: ", record)
        if record:
            if bcrypt.checkpw(password.encode('utf8'), record[3].encode('utf8')):
                user = {'id': record[0], 'uuid': record[1], 'email': record[2], 'name': record[4], 'picture': record[5]}
                jwt = createJWT(user)
                valid = functions.user_token_insert(record[0], jwt)
                if valid:
                    user['token'] = jwt
                    out = {'Message': 'Hi, ' + record[4] + '. Login Sucessful', 
                           'user': user}, 200
        else:
            #intentar un TRY and CATCH?
            out = {'Message': 'Unauthorized', 
                   'Details': 'user ' + email + ' not found'}, 401
            
        return out

#Obtener Usuarios
'''@api.route('/user')#, methods=['GET', 'PUT'])
class user(Resource):
    
    out = {'status': False}

    @auth.login_required
    #@verify_token
    def get(self):
        out = {'status': False}
        user = auth.current_user()
        #if request.method == 'GET':
        out = {'status': True, 'user': user}
        return out
    
    def put(self):
        out = {'status': False}
        #actualizar usuario
        out = {'status': True, 'user': user}
        return out'''

#Crear Usuarios
@ns_users.route('/')#, methods=['POST'])
class user(Resource):

    #@verify_token
    @ns_users.doc('user_get')
    @auth.login_required
    def get(self):
        out = {'status': False}
        user = auth.current_user()
        #if request.method == 'GET':
        out = {'status': True, 'user': user}
        return out
    
    @ns_users.doc('user_put')
    @auth.login_required
    def put(self):
        out = {'status': False}
        #actualizar usuario
        out = {'status': True, 'user': user}
        return out

    @ns_users.doc('user_post')#parser = parser_user)
    @ns_users.expect(user_model)
    #@ns_users.marshal_with(user_model)
    #@auth.login_required
    def post(self):
        out = {'status': False}
        vars = request.get_json(force=True)
        #vars = parser_user.parse_args()
		#return f"Hello name: {args['name']} an age: {args['age']}"
        email = cleanEmail(vars['email'])
        password = vars['password']
        hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf8')
        name = vars['name']
        active = 1
        picture = ''
        record = functions.user_insert(email, hashed, name, picture, active)
        if record:
            user = {'id': record[0], 'uuid': record[1], 'email': email, 'name': name, 'picture': picture}
            jwt = createJWT(user)
            valid = functions.user_token_insert(record[0], jwt)
            if valid:
                user['token'] = jwt
                out = {'status': True, 'user': user}, 200
        
        return out

#Roles
@ns_roles.route('/')#, methods=['GET','POST'])
class roles(Resource):

    out = {'status': False}

    @ns_roles.doc('role_get')#parser = parser_user)
    @auth.login_required
    #@ns_roles.expect(role_model)
    def get(self):

        #traer total roles
        record = functions.role_get(False)

        if record:
            out = {'status': True, 'record': record}

        else:
            out = {'status': False}

        return out
    
    #@ns_roles.doc(parser = parser_roles_post)
    @ns_roles.doc('role_post')#parser = parser_user)
    @ns_roles.expect(role_model)
    @auth.login_required
    def post(self):

        vars = request.get_json(force=True)
        #vars = parser_roles_post.parse_args()
        role = vars['name']

        record = functions.role_insert(role)
        if record:
            out = {'status': True}

        else:
            out = {'status': False}

        return out

#Roles by id
@ns_roles.route('/<int:id>')#, methods=['GET','PUT'])
class roles_id(Resource):

    out = {'status': False}

    @ns_roles.doc('role_get_by_id')
    @auth.login_required
    def get(self, id):

        #traer rol especifico
        record = functions.role_get_by_id(id)

        if record:
            out = {'status': True, 'role': record}

        else:
            out = {'status': False}

        return out

    @ns_roles.doc('role_put_by_id')#parser = parser_roles_put)
    @ns_roles.expect(role_model)
    @auth.login_required
    def put(self, id):

        vars = request.get_json(force=True)
        #vars = parser_roles_put.parse_args()
        name = vars['name']

        put_record = functions.role_put_by_id(id, name)
        
        if put_record:
            out = {'status': True}

        else:
            out = {'status': False}

        return out

#organization (GET, POST, PUT)
#organization (GET con uuid. Colocar en ruta /:uuid)
@ns_organization.route('/')#, methods=['GET','POST'])
class organization(Resource):
#def organization():
    out = {'status': False}

    @ns_organization.doc('organization_get')
    @auth.login_required
    def get(self):

        #Traer todas las organizaciones
        record = functions.organization_get(False)

        if record:
            out = {'status': True, 'record': record}
        else:
            out = {'status': False}

        return out

    #elif request.method == 'POST':
    @ns_organization.doc('organization_post')#parser = parser_organization_post)
    @ns_organization.expect(organization_model)
    @auth.login_required
    def post(self):

        vars = request.get_json(force=True)
        #vars = parser_organization_post.parse_args()
        organization = vars['organization']

        email = cleanEmail(vars['email'])
        record = functions.user_get_by_email(email)
        record_insert = functions.organization_insert(record[1], organization, record[0])
        
        if record_insert:
            out = {'status': True}

        return out

@ns_organization.route('/<string:uuid>')#, methods=['GET'])
class organization_uuid(Resource):
#def organization_uuid(uuid):
    out = {'status': False}
    @ns_organization.doc('organization_get_by_uuid')
    @auth.login_required
    def get(self, uuid):

        record = functions.organization_get_by_uuid(uuid)

        if record:
            out = {'status': True, 'organization': record}
        else:
            out = {'status': False}

        return out

@ns_organization.route('/<int:id>')#, methods=['PUT'])
#def organization_id(id):
class organization_id(Resource):

    out = {'status': False}

    @api.doc('put_organization_by_id')#parser = parser_organization_id_put)
    @ns_organization.expect(organization_id_model)
    @auth.login_required
    def put(self,id):

        vars = request.get_json(force=True)
        #vars = parser_organization_id_put.parse_args()

        name = vars['name']

        put_record = functions.organization_put_by_id(id, name)
        
        if put_record:
            out = {'status': True}

        return out

@ns_user_organization.route('/')#, methods=['GET','POST'])
#def user_organization():
class user_organization(Resource):

    out = {'status': False}

    @ns_user_organization.doc('user_organization_get')
    @auth.login_required
    def get(self):

    #if request.method == 'GET':

        record = functions.get_user_organization()

        if record:
            out = {'status': True, 'record': record}
        else:
            out = {'status': False}

        return out

    #elif request.method == 'POST':

    @ns_user_organization.doc('user_organization_post')#parser = parser_user_organization_post)
    @ns_user_organization.expect(user_organization_model)
    @auth.login_required
    def post(self):

        vars = request.get_json(force=True)
        #vars = parser_user_organization_post.parse_args
        email = vars['email']
        organization = vars['organization']
        role = vars['role']
        
        record_user = functions.user_get_by_email(email)
        record_organization = functions.organization_get_by_name(organization)
        record_role = functions.role_get(role, True)

        record = functions.user_organization_insert(record_user[0], record_organization[0], record_role[0])

        if record:
            out = {'status': True}
        else:
            out = {'status': False}

        return out

@ns_user_organization.route('/<int:id>')#, methods=['PUT'])
#def put_user_organization(id):
class put_user_organization(Resource):

    out = {'status': False}

    @ns_user_organization.doc('user_organization_put')#parser = parser_user_organization_put)
    @ns_user_organization.expect(user_organization_put_model)
    @auth.login_required
    def put(self, id):

        vars = request.get_json(force=True)
        #vars = parser_user_organization_put.parse_args
        organization = vars['organization']
        role = vars['role']

        record = functions.put_user_organization(id, organization, role)

        if record:
            out = {'status': True}
        else:
            out = {'status': False}

        return out
    
##cambio de password por ID
@ns_password.route('/<int:id>')
class put_user_password(Resource):

    @ns_password.doc('user_password_put_by_id')
    @ns_password.expect(password_model)
    @auth.login_required
    
    def put(self, id):

        out = {'status': False}

        vars = request.get_json(force=True)

        new_password = vars['new_password']
        confirm_password = vars['confirm_password']

        if new_password != confirm_password:
            return {'Error': 'password mismatch'}, 401
        else:
            hashed = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt()).decode('utf8')
            record = functions.put_user_password(id, hashed)
            if record:
                out = {'status': True}

        return out
    
@ns_password.route('/')
class put_user_password(Resource):

    @ns_password.doc('user_password_put')
    @ns_password.expect(password_model)
    @auth.login_required
    
    def put(self):

        out = {'status': False}

        vars = request.get_json(force=True)

        new_password = vars['new_password']
        confirm_password = vars['confirm_password']

        user = auth.current_user()

        if new_password != confirm_password:
            return {'password error': 'password mismatch'}, 401
        else:
            hashed = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt()).decode('utf8')
            record = functions.put_user_password(user['id'], hashed)
            if record:
                out = {'status': True}

        return out
    @ns_password.doc('user_password_recovery')
    #@auth.login_required
    def get(self):

        #out = {'status': False}

        try:
            #cuerpo_email = "Este es un correo de pruebas desde notificaciones"
            html_file = open("index.html", "r")
            cuerpo_email = html_file.read()
            send("sigmarazor@gmail.com", "Encabezado del email HTML", cuerpo_email,)
        except Exception as e:

            return {'Error': 'An error occured while sending email'}

        return {'Mail Status' : 'Sent'}, 200



'''@ns_user_password.route('/user_password/<uuid>')#, methods=['PUT'])
#def put_user_organization(id):
class put_user_password(Resource):

    out = {'status': False}

    @ns_user_organization.doc(parser = parser_user_password_put)
    @auth.login_required
    def put(self, id):

        #vars = request.get_json()
        vars = parser_user_password_put.parse_args
        password = vars['password']

        record_id = functions.user_get_by_uuid()
	
        record = functions.put_user_password(id, password)

        if record:
            out = {'status': True}

        return record'''

app.run('0.0.0.0', 5000, debug=True)
