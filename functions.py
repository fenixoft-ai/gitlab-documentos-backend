import os
import mariadb
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=db_user,
        password=db_pass,
        host=db_host,
        port=int(db_port),
        database=db_name
    )
    conn.autocommit = False
except mariadb.Error as e:
    print(f"Documentos: Error connecting to MariaDB Platform: {e}")

def user_get_by_email(email):
    record = None
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM user WHERE email = ?"
        values = (email, )
        cursor.execute(sql, values)
        for item in cursor:
            record = item
        return record
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return record

def user_get_by_id(id):
    record = None
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM user WHERE id = ?"
        values = (id, )
        cursor.execute(sql, values)
        for item in cursor:
            record = item
        return record
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return record

def user_insert(email, password, name, picture, active):
    record = None
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO user (email, password, name, picture, active) VALUES (?, ?, ?, ?, ?) RETURNING id, uuid"
        values = (email, password, name, picture, active)
        cursor.execute(sql, values)
        conn.commit()
        for item in cursor:
            record = item
        return record
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return record

def user_token_insert(user_id, token):
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO user_token (user_id, token) VALUES (?, ?)"
        values = (user_id, token)
        cursor.execute(sql, values)
        conn.commit()
        return True
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return False

def user_token_get(token):
    record = False
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM user_token WHERE token = ?"
        values = (token, )
        cursor.execute(sql, values)
        for item in cursor:
            record = item
        return record
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return record
    
def role_get(name='', state = False):
    record = False
    try:
        cursor = conn.cursor()
        if state == False:
            
            sql = "SELECT * FROM role"
            cursor.execute(sql)
            record = cursor.fetchall()

        if state == True:
            
            sql = "SELECT * FROM role WHERE name = ?"
            values = (name, )
            cursor.execute(sql, values)

            for item in cursor:
                
                record = item

        return record
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return record
    
def role_get_by_id(id):
    record = None
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM role WHERE id = ?"
        values = (id, )
        cursor.execute(sql, values)
        for item in cursor:
            record = item
        return record
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return record

def role_put_by_id(id, name):
    
    try:
        cursor = conn.cursor()
        sql = "UPDATE role SET name = ? WHERE id = ?"
        values = (name, id)
        cursor.execute(sql, values)
        conn.commit()
        return True
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return False

def role_insert(role):
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO role (name) VALUES (?)"
        values = (role, )
        cursor.execute(sql, values)
        conn.commit()
        return True
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return False
    
def organization_insert(uuid, name, user_id):
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO organization (uuid, name, user_id) VALUES (?, ?, ?)"
        values = (uuid, name, user_id, )
        cursor.execute(sql, values)
        conn.commit()
        return True
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return False
    
def organization_get(name='', state = False):
    record = False
    try:
        cursor = conn.cursor()
        if state == False:
            
            sql = "SELECT * FROM organization"
            cursor.execute(sql)
            record = cursor.fetchall()

        if state == True:
            
            sql = "SELECT * FROM organization WHERE name = ?"
            values = (name, )
            cursor.execute(sql, values)

            for item in cursor:
                
                record = item

        return record
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return record

def organization_get_by_id(id):
    record = False
    try:
        cursor = conn.cursor()
            
        sql = "SELECT * FROM organization WHERE id = ?"
        values = (id, )
        cursor.execute(sql, values)
        
        for item in cursor:
            
            record = item

        return record
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return record

def organization_get_by_uuid(uuid):
    record = False
    try:
        cursor = conn.cursor()
            
        sql = "SELECT * FROM organization WHERE uuid = ?"
        values = (uuid, )
        cursor.execute(sql, values)
        
        for item in cursor:
            
            record = item

        return record
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return record
    
def organization_get_by_name(name):
    record = False
    try:
        cursor = conn.cursor()
            
        sql = "SELECT * FROM organization WHERE name = ?"
        values = (name, )
        cursor.execute(sql, values)
        
        for item in cursor:
            
            record = item

        return record
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return record

def organization_put_by_id(id, name):
    record = False
    try:
        cursor = conn.cursor()
            
        sql = "UPDATE organization SET name = ? WHERE id = ?"
        values = (name, id)
        cursor.execute(sql, values)
        conn.commit()

        return True

    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return record
    
def get_user_organization(name='', state = False):
    
    record = False

    try:
        
        cursor = conn.cursor()
            
        sql = "SELECT user_organization.id, user.email, organization.name, role.name "\
            "FROM user_organization "\
            "INNER JOIN user ON user_organization.user_id = user.id "\
            "INNER JOIN organization ON user_organization.organization_id = organization.id " \
            "INNER JOIN role ON user_organization.role_id = role.id "\
            "ORDER BY organization.name"
        cursor.execute(sql)
        record = cursor.fetchall()
        
        for item in cursor:
            
            record = item

        return record
    
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return record
    
def user_organization_insert(user_id, organization_id, role_id):
    
    record = False

    try:
        
        cursor = conn.cursor()
        sql = "INSERT INTO user_organization (user_id, organization_id, role_id) VALUES (?, ?, ?)"
        values = (user_id, organization_id, role_id, )
        
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        cursor.execute(sql, values)
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        conn.commit()
        
        return True
    
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return record
    
def put_user_organization(id, organization_id, role_id):
    
    record = False

    try:
        
        cursor = conn.cursor()
        sql = "UPDATE user_organization SET organization_id = ?, role_id = ? WHERE id = ?"
        values = (organization_id, role_id,id, )
        
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        cursor.execute(sql, values)
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        conn.commit()
        
        return True
    
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return record
    
def put_user_password(id, password):
    
    record = False

    try:
        
        cursor = conn.cursor()
        sql = "UPDATE user SET password = ? WHERE id = ?"
        values = (password,id, )
        
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        cursor.execute(sql, values)
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        conn.commit()
        
        return True
    
    except mariadb.Error as e:
        print(f"Documentos: Error: {e}")
        return record