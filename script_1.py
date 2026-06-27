import ctypes
import random
class Registro(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_ubyte),
        ("valor", ctypes.c_byte)
    ]
def generar_y_guardar_registros(nombre_archivo, cantidad=100):

    ArrayRegistros = Registro * cantidad
    registros = ArrayRegistros()
    for i in range(cantidad):
        registros[i].id = random.randint(1, 5)
        registros[i].valor = random.randint(100, 255)
    with open(nombre_archivo, "wb") as f:
     f.write(bytes(registros))
    print(f"¡Archivo '{nombre_archivo}' creado exitosamente con {cantidad} registros!")


def leer_y_mostrar_archivo(nombre_archivo, cantidad=10):
    print(f"\nLeyendo los primeros {cantidad} registros para verificación:")
    registro_aux = Registro()
    tamano_registro = ctypes.sizeof(Registro)
    with open(nombre_archivo, "rb") as f:
     for _ in range(cantidad):
      datos = f.read(tamano_registro)
      if not datos:
         break
    ctypes.memmove(ctypes.byref(registro_aux), datos, tamano_registro)
    print(f"ID: {registro_aux.id} | Valor (c_byte): {registro_aux.valor}")


if __name__ == "__main__":
   archivo_destino = "datos_estructurados.bin"
   generar_y_guardar_registros(archivo_destino)
   leer_y_mostrar_archivo(archivo_destino)

   