def Out_response(error=False, mensaje="Operación exitosa", datos=None):
    res = {
        "error": error,
        "mensaje": mensaje,
        "datos": datos,
    }
    return res


def Error_response(err, mensaje, codigo_error=None):
    res = {
        "error": True,
        "mensaje": mensaje,
        "data": {
            "Codigo interno": codigo_error,
            "Mensaje Error": err
        }
    }
    return res
