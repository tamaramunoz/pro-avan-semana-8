def extraer_numero_id(cadena):
    valores = cadena.split(',')
    for valor in valores:
        if "ID" in valor:
            return int(valor.split(':')[1].strip())
    return None
