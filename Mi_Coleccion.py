import pickle
from datetime import datetime
import os

ctlg = []                          
binario_file = "popular"           
TXT_FILE = "canciones.txt"         

def rg_error(mensaje):
    with open("error", "a", encoding="utf-8") as log:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{fecha}] {mensaje}\n")

def cr_txt():
    if not os.path.exists(TXT_FILE):
        with open(TXT_FILE, "w", encoding="utf-8") as f:
            f.write("LISTA DE CANCIONES EN YOUTUBE MUSIC\n")

def agregar():
    try:
        print("\nDATOS DE LA CANCIÓN")
        print("**********************\n")

        tt = input("Nombre de la cancion: ").strip()
        if tt == "":
            raise ValueError("Ingresa un nombre valido para continuar.")

        art = input("Artista: ").strip()
        genero = input("Género: ").strip()

        while True:
            try:
                anio = int(input("Fecha de lanzamiento: ").strip())
                break
            except ValueError:
                print("Debes agregar valores validos. Volvamos a intentar")

        while True:
            try:
                popularidad = int(input("Nivel de Popularidad (1-100): ").strip())
                if not (1 <= popularidad <= 100):
                    raise ValueError("Sabemos tu aprecio a esta cancion, pero ingresa valores dentro del rango.")
                break
            except ValueError:
                print("Ingresa un número entre 1 y 100. Y sigamos disfrutando.")

        cancion = {
            "tt": tt,
            "art": art,
            "genero": genero,
            "anio": anio
        }

        ctlg.append(cancion)

        with open(TXT_FILE, "a", encoding="utf-8") as cat:
            cat.write(f"Título: {tt}\n")
            cat.write(f"Artista: {art}\n")
            cat.write(f"Género: {genero}\n")
            cat.write(f"Año: {anio}\n")
            cat.write("-" * 30 + "\n")

        guardar_binario(tt, popularidad)

        print(f'\n Exelente, añadimos "{tt}" exitosamente.\n')

    except Exception as e:
        rg_error(f"Ups, Error al agregar canción: {e}")
        print("Ocurrió un error. Intentemos nuevamente.\n")

def mostrar():
    print("\nLISTA DE NUESTRAS CANCIONES FAVORITAS\n")
    try:
        with open(TXT_FILE, "r", encoding="utf-8") as cat:
            contenido = cat.read()
            if contenido.strip() == "":
                print("El catálogo está vacío.\n")
            else:
                print(contenido)
    except Exception as e:
        rg_error(f"Lo lamentamos, hemos tenido problemas al mostrar catalogo: {e}")
        print(" Error al leer el archivo.\n")

def buscar():
    try:
        print("\nBUSCADOR DE CANCIÓNES\n")
        titulo_buscar = input("Título a buscar: ").strip().lower()

        encontrado = False
        for c in ctlg:
            if c["tt"].lower() == titulo_buscar:
                print("\nCanción encontrada:\n")
                print(f"Título: {c['tt']}")
                print(f"Artista: {c['art']}")
                print(f"Género: {c['genero']}")
                print(f"Año: {c['anio']}")

                popularidad = leer_bin(c["tt"])
                if popularidad is not None:
                    print(f"Popularidad: {popularidad}/100\n")

                encontrado = True

        if not encontrado:
            print("\n Lo Lamento Canción no encontrada.\n")

    except Exception as e:
        rg_error(f"Error al buscar canción: {e}")
        print("Error al buscar canción.\n")


# D6
def guardar_binario(tt, popularidad):
    try:
        datos = {}

        if os.path.exists(binario_file):
            with open(binario_file, "rb") as f:
                datos = pickle.load(f)

        datos[tt] = popularidad

        with open(binario_file, "wb") as f:
            pickle.dump(datos, f)

    except Exception as e:
        rg_error(f"Error al guardar binario: {e}")

def leer_bin(tt):
    try:
        with open(binario_file, "rb") as f:
            datos = pickle.load(f)
        return datos.get(tt, None)

    except FileNotFoundError:
        print("⚠ Archivo de popularidad no encontrado.")
    except Exception as e:
        rg_error(f"Error al leer binario: {e}")

    return None

def mtr_bin():
    print("\n POPULARIDAD DE CANCIONES\n")
    try:
        with open(binario_file, "rb") as f:
            datos = pickle.load(f)

        if len(datos) == 0:
            print("No hay datos en el archivo binario.\n")
        else:
            for tt, valor in datos.items():
                print(f"{tt}: {valor}/100")
        print()

    except FileNotFoundError:
        print("No existe el archivo de popularidad.\n")
    except Exception as e:
        rg_error(f"Error al mostrar binarios: {e}")
        print(" Error al mostrar datos.\n")

def main():
    cr_txt()

    while True:
        print("\nMENÚ SOLO PARA TI")
        print("**********************")
        print("1. Agregar canción")
        print("2. Mostrar colección completa")
        print("3. Buscar canción")
        print("4. Mostrar datos binarios (popularidad)")
        print("5. Salir")

        try:
            op = int(input("\nElige una opción: "))
        except:
            print("Oh no, Opción inválida.")
            continue

        if op == 1:
            agregar()
        elif op == 2:
            mostrar()
        elif op == 3:
            buscar()
        elif op == 4:
            mtr_bin()
        elif op == 5:
            print("Saliendo del sistema...")
            break
        else:
            print(" Opción inválida.\n")


main()
