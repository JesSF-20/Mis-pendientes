# Agenda de contactos

def agregar_contacto():
    nombre = input("Nombre: ")
    telefono = input("Teléfono: ")
    correo = input("Correo: ")
    linea = nombre + "\t" + telefono + "\t" + correo + "\n"
    with open("contactos.txt", "a") as archivo:
        archivo.write(linea)
    print("Contacto agregado correctamente.\n")

def ver_contactos():
    print("\n-- Lista de Contactos --")
    try:
        with open("contactos.txt", "r") as archivo:
            for linea in archivo:
                print(linea.strip())
    except FileNotFoundError:
        print("No hay contactos guardados aún.")
    print()

def buscar_contacto():
    nombre_buscado = input("Ingrese el nombre a buscar: ")
    encontrado = False
    try:
        with open("contactos.txt", "r") as archivo:
            for linea in archivo:
                campos = linea.strip().split("\t")
                nombre = campos[0]
                if nombre == nombre_buscado:
                    print("Contacto encontrado:", linea.strip())
                    encontrado = True
    except FileNotFoundError:
        print("No hay contactos guardados aún.")
    if not encontrado:
        print("No se encontró el contacto.\n")

def eliminar_contacto():
    nombre_a_eliminar = input("Ingrese el nombre a eliminar: ")
    try:
        with open("contactos.txt", "r") as archivo:
            lineas = archivo.readlines()
        nuevas_lineas = []
        eliminado = False
        for linea in lineas:
            campos = linea.strip().split("\t")
            nombre = campos[0]
            if nombre != nombre_a_eliminar:
                nuevas_lineas.append(linea)
            else:
                eliminado = True
        with open("contactos.txt", "w") as archivo:
            archivo.writelines(nuevas_lineas)
        if eliminado:
            print("Contacto eliminado correctamente.\n")
        else:
            print("No se encontró el contacto.\n")
    except FileNotFoundError:
        print("No hay contactos guardados aún.\n")

# Programa principal
while True:
    print("---- Agenda de Contactos ----")
    print("Agregar")
    print("Buscar")
    print("Eliminar")
    print("Ver")
    print("Salir")
    
    accion = input("Elige una acción: ")

    if accion == "Agregar":
        agregar_contacto()
    elif accion == "Buscar":
        buscar_contacto()
    elif accion == "Eliminar":
        eliminar_contacto()
    elif accion == "Ver":
        ver_contactos()
    elif accion == "Salir":
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida, intenta de nuevo.\n")
