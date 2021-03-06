import conn as conn
import hashlib
import datetime
from pytz import timezone
from Tokens.token_func import generar_token, verificar_token, desactivar_token, crearTK
from responses import Error_response, Out_response

def crear(data):
    print("crear tarea: ", data)
    titulo = data.get("titulo", "")
    descripcion = data.get("descripcion", "")
    responsable_id = data.get("responsable_id", "")
    if(titulo == "" or descripcion == ""):
        return Out_response(False, "Campos faltantes titulo o descripcion", 110)
    
    q = f"INSERT INTO tareas (titulo, descripcion, responsable_id, estado_id) VALUES ('{titulo}', '{descripcion}', {responsable_id}, 1)"
    res = conn.executeCommit(q)
    if(res == "error"):
        return Out_response(True, "Error al insertar tarea en bd", 111)
    id_tarea = res
    resp = {
        "id_tarea" : id_tarea
    }
    return Out_response(False, "Tarea creada exitosamente", resp)

def actualizar(data):
    print("actualizar tarea", data)
    id_tarea = data.get("id_tarea", "")
    titulo = data.get("titulo", "")
    descripcion = data.get("descripcion", "")
    responsable_id = data.get("responsable_id", "")
    estado_id = data.get("estado_id", "")
    if(titulo == "" or descripcion == "" or estado_id == "" or responsable_id == "" or id_tarea == ""):
        return Out_response(False, "No puede dejar en blanco campos al actualizar", 112)
    q2 = f"SELECT * FROM tareas WHERE id = {id_tarea}"
    res2 = conn.executeQuerydict(q2)
    if(res2 == "error"):
        return Out_response(True, "Error al consultar tarea en bd", 117)
    if(len(res2) < 1):
        return Out_response(True, "No hay tarea asociada en la bd", 118)
    q = f"UPDATE tareas SET titulo = '{titulo}', descripcion = '{descripcion}', responsable_id = {responsable_id}, estado_id = {estado_id} WHERE id = {id_tarea}"
    res = conn.executeCommit(q)
    if(res == "error"):
        return Out_response(True, "Error al actualizar tarea en bd", 113)
    return Out_response(False, "Tarea actualizada exitosamente")


def listarTarea(data):
    print("listar tarea", data)
    id_tarea = data.get("id_tarea", "")
    q2 = f"SELECT * FROM tareas WHERE id = {id_tarea}"
    res2 = conn.executeQuerydict(q2)
    if(res2 == "error"):
        return Out_response(True, "Error al consultar tarea en bd", 119)
    if(len(res2) < 1):
        return Out_response(True, "No hay tarea asociada en la bd", 120)
    q = f"SELECT titulo, t.descripcion, responsable_id, e.descripcion AS estado FROM tareas AS t INNER JOIN estado_tarea AS e ON t.estado_id = e.id WHERE t.id = {id_tarea}"
    res = conn.executeQuerydict(q)
    if(res == "error"):
        return Out_response(True, "Error al consultar tarea en bd", 114)
    titulo = res[0]["titulo"]
    descripcion = res[0]["descripcion"]
    responsable = res[0]["responsable_id"]
    estado = res[0]["estado"]
    resp = {
        "titulo" : titulo,
        "descripcion" : descripcion,
        "responsable" : responsable,
        "estado" : estado
    }
    return Out_response(False, "Operacion exitosa", resp)

def listarTodasLasTareas(data):
    print("listar todas las tarea", data)
    q = f"SELECT titulo, t.descripcion, responsable_id, e.descripcion AS estado FROM tareas AS t INNER JOIN estado_tarea AS e ON t.estado_id = e.id"
    res = conn.executeQuerydict(q)
    if(res == "error"):
        return Out_response(True, "Error al consultar las tareas en bd", 115)
    resp = []
    for i in res:
        titulo = i["titulo"]
        descripcion = i["descripcion"]
        responsable = i["responsable_id"]
        estado = i["estado"]
        tarea = {
            "titulo" : titulo,
            "descripcion" : descripcion,
            "responsable" : responsable,
            "estado" : estado
        }
        resp.append(tarea)
    return Out_response(False, "Operacion exitosa", resp)
    
def eliminar(data):
    print("eliminar tarea", data)
    id_tarea = data.get("id_tarea", "")
    q2 = f"SELECT * FROM tareas WHERE id = {id_tarea}"
    res2 = conn.executeQuerydict(q2)
    if(res2 == "error"):
        return Out_response(True, "Error al consultar tarea en bd", 121)
    if(len(res2) < 1):
        return Out_response(True, "No hay tarea asociada en la bd", 122)
    q = f"DELETE FROM tareas WHERE id = {id_tarea}"
    res = conn.executeCommit(q)
    if(res == "error"):
        return Out_response(True, "Error al eliminar la tarea en bd", 116)
    return Out_response(False, "Tarea eliminada exitosamente")


def gestion(request):
    opciones = ['crear', "actualizar", "listarUna", "listarTodas", "eliminar"]
    funciones = [crear, actualizar, listarTarea, listarTodasLasTareas, eliminar]
    op = request.get('op')

    token = request.get('token', None)

    if op in opciones:
        if (op != "login"):
            if not token:
                return Out_response(True, "Datos inv??lidos", {"token": token})
            if verificar_token(token) is not True:
                return Error_response(True, "Token inv??lido", 401)

        resp = funciones[opciones.index(op)](
            request) 
    else:
        resp = Out_response(True, "Operaci??n Inv??lida")
    return resp