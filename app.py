from flask import Flask
from flask import request
from responses import Out_response
from Usuarios.views import gestion as gestionUsuarios
from Tareas.views import gestion as gestionTareas
import time
import json


app = Flask(__name__)

@app.route("/", methods=["POST"])
def bot():
	data = request.get_json()
	print("datos post ", data)
	modulo = data.get("mod", "")
	op = data.get("op", "")
	if (modulo != ""):
		if (op != ""):
			if modulo == "usuarios":
				res = gestionUsuarios(data)
			elif modulo == "tareas":
				res = gestionTareas(data)
			else:
				res = Out_response(True, "Módulo Inválido")
		else:
			res = Out_response(True, "Operacion no especificada")
	else:
		res = Out_response(True, "Módulo no especificado")
	
	print("res", res)

	#body = {
    #    "data": res
    #}

	response = {"statusCode": 200, "body": res}

	return response


if __name__ == "__main__":
	app.run()
