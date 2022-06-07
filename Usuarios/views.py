from pickle import FALSE
import conn as conn
import hashlib
import datetime
from pytz import timezone
from Tokens.token_func import generar_token, verificar_token, desactivar_token, crearTK
from responses import Error_response, Out_response

def crear(data):
    user = data.get("user", "")
    passwd = data.get("pass", "")
    tipoUser = data.get("tipo_usuario", "")
    if(user == "" or passwd == "" or tipoUser == ""):
        return Out_response(False, "Faltan campos por llenar", 103)
    bytePass = passwd.encode("utf-8")
    encryptPass = hashlib.md5(bytePass)
    encryptPass = encryptPass.hexdigest()
    q = f"SELECT usuario FROM usuarios WHERE usuario = '{user}' AND activo = 1"
    res = conn.executeQuerydict(q)
    if(res == "error"):
        return Out_response(False, "Error al validar usuario creado", 104)
    elif(len(res) > 0):
        return Out_response(False, "Usuario ya existe", 105)

    q2 = f"INSERT INTO usuarios (usuario, contra, tipo, activo) VALUES ('{user}', '{encryptPass}', {tipoUser}, 1)"
    res2 = conn.executeCommit(q2)
    if (res2 == "error"):
        return Out_response(False, "Error al insertar usuario", 106)
    
    return Out_response(False, "Usuario agregado exitosamente")
    
    

def login(data):
    print("logueo", data)
    user = data.get("user", "")
    passwd = data.get("pass", "")

    q = f"SELECT * FROM usuarios WHERE usuario = '{user}' AND activo = 1"
    res = conn.executeQuerydict(q)
    if(res == "error"):
        return Error_response(True, "Error consultando usuario", 100)
    elif(len(res) < 1):
        return Error_response(True, "No existe el usuario", 101)

    q2 = f"SELECT * FROM usuarios WHERE usuario = '{user}' AND activo = 1"
    res2 = conn.executeQuerydict(q2)
    if(res2 == "error"):
        return Error_response(True, "Error consultando contraseña", 107)

    contraBd = res2[0]["contra"]
    user_id = res2[0]["id"]
    bytePass = passwd.encode("utf-8")
    encryptPass = hashlib.md5(bytePass)
    encryptPass = encryptPass.hexdigest()
    if(contraBd != encryptPass):
        return Out_response(False, "Contraseña incorrecta", 108)
    
    crear = generar_token(user, passwd, "usuarios")
    token = crear.get("token", "")
    fecha_venc = crear.get("fecha_venc", "")
    fecha_venc = datetime.datetime.fromtimestamp(
        fecha_venc, timezone('America/Bogota'))
    print("token", token, "fecha_venc", fecha_venc)
    des = desactivar_token(False, user_id)

    if des == "error":
        return Out_response(False, "Error desactivando viejos tokens", 109)
    
    data = {
        "token": token,
        "activo": 1,
        "fecha_venc": fecha_venc,
        "usuario_id": user_id
    }
    crearToken = crearTK(data)
    if crearToken == "error":
        return Out_response(False, "Error al insertar token en bd", 110)
    return Out_response(False, "Login correcto", {"token": token})

def gestion(request):
    opciones = ['crear', 'login']
    funciones = [crear, login]
    op = request.get('op')

    token = request.get('token', None)

    if op in opciones:
        if (op != "login"):
            if not token:
                return Out_response(True, "Datos inválidos", {"token": token})
            if verificar_token(token) is not True:
                return Error_response(True, "Token inválido", 401)

        resp = funciones[opciones.index(op)](
            request) 
    else:
        resp = Out_response(True, "Operación Inválida")
    return resp


    
