"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """

    import pandas as pd
    import re

    # Leer archivo completo
    with open("files/input/clusters_report.txt", "r") as archivo:
        lineas = archivo.readlines()

    # Omitir encabezado (primeras 4 líneas)
    contenido = lineas[4:]

    # Unir fragmentos de múltiples líneas en un solo registro por cluster
    bloques = []
    buffer = ""

    for linea in contenido:
        limpia = re.sub(r"\s+", " ", linea.strip())  # normalizar espacios

        if not limpia:
            continue

        # Si empieza con número → comienza un nuevo cluster
        if re.match(r"^\d+\s", limpia):
            if buffer:
                bloques.append(buffer)
            buffer = limpia
        else:
            buffer += " " + limpia

    if buffer:
        bloques.append(buffer)

    # Extraer con expresión regular
    patron = re.compile(
        r"^(\d+)\s+(\d+)\s+([\d,]+ %)\s+(.*)$"
    )

    registros = []
    for linea in bloques:
        grupos = patron.match(linea).groups()
        registros.append(grupos)

    # Crear DataFrame
    df = pd.DataFrame(
        registros,
        columns=[
            "cluster",
            "cantidad_de_palabras_clave",
            "porcentaje_de_palabras_clave",
            "principales_palabras_clave"
        ]
    )

    # Conversiones
    df["cluster"] = df["cluster"].astype(int)
    df["cantidad_de_palabras_clave"] = df["cantidad_de_palabras_clave"].astype(int)
    df["porcentaje_de_palabras_clave"] = (
        df["porcentaje_de_palabras_clave"]
        .str.replace(",", ".")
        .str.replace(" %", "")
        .astype(float)
    )

    # Limpiar palabras clave
    df["principales_palabras_clave"] = (
        df["principales_palabras_clave"]
        .str.replace(r"\.$", "", regex=True)      # eliminar punto final
    )

    return df