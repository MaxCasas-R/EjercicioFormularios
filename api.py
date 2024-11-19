from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
from pydantic import BaseModel
import shutil
import os  # Para acceder a la ruta del home
import uuid  # Para generar nombres aleatorios

app = FastAPI()

class Usuario(BaseModel):
    Nombre: Optional[str] = None
    Direccion: Optional[str] = None


@app.post("/datos")
async def guarda_foto(Nombre: str = Form(...), Direccion: str = Form(...), Fotografia: UploadFile = File(...), vip: bool = Form(False)):

    print("Nombre:", Nombre)
    print("Direccion:", Direccion)
    print(f"VIP: {'Sí' if vip else 'No'}")
    
    home_usuario = os.path.expanduser("~")  # Home del usuario
    nombre_archivo = uuid.uuid4()  # Generamos un nombre aleatorio en formato hexadecimal
    extension_foto = os.path.splitext(Fotografia.filename)[1]
    
    # Usamos os.path.join() para manejar las rutas de manera segura
    ruta_imagen = os.path.join(home_usuario, 'fotos-usuarios-vip' if vip 
                               else 'fotos-usuarios', f"{nombre_archivo}{extension_foto}")

    print("Guardando la foto en", ruta_imagen)
        # Verificamos si la carpeta existe, si no, la creamos
    os.makedirs(os.path.dirname(ruta_imagen), exist_ok=True)

    with open(ruta_imagen, "wb") as imagen:
        contenido = await Fotografia.read()
        imagen.write(contenido)

    respuesta = {
        "Nombre": Nombre,
        "Dirección": Direccion,
        "Ruta": ruta_imagen
    }

    return respuesta
