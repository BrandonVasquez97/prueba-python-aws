import json
import pymysql
import boto3
import base64
from botocore.exceptions import ClientError
from datetime import datetime
from pytz import timezone
from responses import Error_response

#Funcion para INSERT/UPDATE
def executeCommit(query):
    try:
        print("executeCommit", query)
        #Obtiene las credenciales con el SECRET MANAGER
        credenciales = json.loads(get_secret_db("commit"))
        #Llamado de datos del JSON
        endpoint = credenciales['endpoint']
        db_user = credenciales['user']
        db_pass = credenciales['password']
        db_name = "tareas_bd"
        connection = pymysql.connect(
            host=endpoint, user=db_user, password=db_pass, db=db_name, port=3306)
        #Ejecuta la consulta
        cursor = connection.cursor()
        cursor.execute("SET TIME_ZONE='America/Bogota'")
        cursor.execute("SET @@session.time_zone = 'America/Bogota'")
        res = cursor.execute(query)
        res = cursor.lastrowid
        print("resCommit", res)
        connection.commit()

    except Exception as err:
        res = "error"
        print(Error_response(err, "executeCommit - Error interno", 110))
    finally:
        connection.close()
    return res


#Funcion para SELECT
def executeQuery(query):
    try:
        print("executeQuery", query)
        #Obtiene las credenciales con el SECRET MANAGER
        credenciales = json.loads(get_secret_db("commit"))
        #Llamado de datos del JSON
        endpoint = credenciales['endpoint']
        db_user = credenciales['user']
        db_pass = credenciales['password']
        db_name = "tareas_bd"
        connection = pymysql.connect(
            host=endpoint, user=db_user, password=db_pass, db=db_name, port=3306)

        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)

        rows = cursor.fetchall()
        print("rows =>", rows, "type(rows)", type(rows))

        rows = json.dumps(rows, indent=4, sort_keys=True, default=str)
        # print("json.dumps rows =>", rows, "type(rows)",type(rows))
        rows = json.loads(rows)
        # print("json.loads rows =>", rows, "type(rows)",type(rows))

    except Exception as err:
        rows = "error"
        print(Error_response(err, "executeQuery - Error interno", 111))
    finally:
        connection.close()
    return rows



def executeQuerydict(query):
    try:
        print("executeQuery", query)
        #Obtiene las credenciales con el SECRET MANAGER
        credenciales = json.loads(get_secret_db("commit"))
        #Llamado de datos del JSON
        endpoint = credenciales['endpoint']
        db_user = credenciales['user']
        db_pass = credenciales['password']
        db_name = "tareas_bd"
        connection = pymysql.connect(
            host=endpoint, user=db_user, password=db_pass, db=db_name, port=3306)

        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)

        rows = cursor.fetchall()
        print("rows =>", rows, "type(rows)", type(rows))

        rows = json.dumps(rows, indent=4, sort_keys=True, default=str)
        # print("json.dumps rows =>", rows, "type(rows)",type(rows))
        rows = json.loads(rows)
        # print("json.loads rows =>", rows, "type(rows)",type(rows))

    except Exception as err:
        rows = "error"
        print(Error_response(err, "executeQuery - Error interno", 111))
    finally:
        connection.close()
    return rows


def getSysdate():
    try:
        # define date format
        fmt = '%Y-%m-%d %H:%M:%S'
        # fmt = '%Y-%m-%d %H:%M:%S %Z%z'
        # define eastern timezone
        eastern = timezone('US/Eastern')
        # naive datetime
        naive_dt = datetime.now()
        # localized datetime
        loc_dt = datetime.now(eastern)
        loc_dt = loc_dt.strftime(fmt)
        print("naive", naive_dt.strftime(fmt))
        print("loc_dt", loc_dt)
    except Exception as err:
        loc_dt = Error_response(err, "getSysdate - Error interno", 112)
    return loc_dt


def getDatetime():
    try:
        # define date format
        fmt = '%Y-%m-%d %H:%M:%S'
        # fmt = '%Y-%m-%d %H:%M:%S %Z%z'
        # define eastern timezone
        eastern = timezone('US/Eastern')
        # naive datetime
        naive_dt = datetime.now()
        # localized datetime
        loc_dt = datetime.now(eastern)
        print("naive", naive_dt.strftime(fmt))
        print("loc_dt", loc_dt)
    except Exception as err:
        loc_dt = Error_response(
            err, "getDatetime - Error interno", 113)
    return loc_dt


def validarFechas(fecha):
    if(fecha == None or fecha == ""):
        fecha = "null"
    else:
        fecha = f"'{fecha}'"

    return fecha


def get_secret_db(data):
    print("secretos", data)
    if data == 'commit':
        secret_name = "credenciales_db"
    elif data == 'select':
        secret_name = "credenciales_db_read_only"
    region_name = "us-east-2"

    print(secret_name)

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    
    return secret
