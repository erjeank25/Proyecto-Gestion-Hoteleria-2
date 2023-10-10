import csv #manipulacion de archivos csv
import os #eliminacion de archivos csv
import datetime #se utilizara para la fecha y hora exacta de un registro
import re

class PilaRegistro:
    def __init__(self):
        self.items = []

    def esta_vacia(self):
        return len(self.items) == 0

    def apilar(self, elemento):
        self.items.append(elemento)

    def desapilar(self):
        if not self.esta_vacia():
            return self.items.pop()
        else:
            raise IndexError("La pila está vacía")

    def cima(self):
        if not self.esta_vacia():
            return self.items[-1]
        else:
            raise IndexError("La pila está vacía")

    def tamano(self):
        return len(self.items)

pila_registros = PilaRegistro() #Se usara a lo largo del programa, por eso se pone acá
pila_nueva = PilaRegistro()

def logRegistrosyErrores(pila,pila_2,archivo_csv):
    with open(archivo_csv, 'w', newline='') as archivo: #Agregar los registros actuales al csv
        # Crea un objeto escritor CSV
        escritor = csv.writer(archivo,delimiter=';')
        escritor.writerow(['Tipo Accion','Detalles Adicionales','Fecha','Hora'])
        while not pila.esta_vacia():
            elemento = pila.desapilar()
            pila_2.apilar(elemento)
            escritor.writerow(elemento)
    while not pila_2.esta_vacia():
        elemento = pila_2.desapilar()
        pila.apilar(elemento)
    with open(archivo_csv, 'r', newline='') as archivo: #Listar lo anteriormente agregado
        lector = csv.reader(archivo,delimiter=';')
        next(lector)
        print("")
        print("Tipo                        Descripcion                                               Fecha                   Hora")
        for fila in lector:
            print("{:<10} {:<70} {:<25} {:^12}".format(fila[0],fila[1],fila[2],fila[3]))
    
class Hotel: #constructor hotel
    def __init__(self, nombre, direccion, telefono, habitaciones_disponibles, nro_reservas):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.habitaciones_disponibles = habitaciones_disponibles
        self.nro_reservas = nro_reservas
        
class NodoHotel: #constructor nodos hoteles
    def __init__(self, hotel):
        self.hotel = hotel
        self.siguiente = None # nodo siguiente

class NodoHabitacion: #constructor nodos habitaciones
    def __init__(self, numero, disponibilidad):
        self.numero = numero
        self.disponibilidad = disponibilidad
        self.siguiente = None #nodo siguiente

class ListaHoteles:
    #Opciones de hoteles
    def __init__(self): #constructor hotel
        self.inicio = None

    def cargar_csv(self, archivo): #carga de datos de .csv
        with open(archivo, 'r') as archivo_csv:
            lector = csv.reader(archivo_csv, delimiter=';')
            next(lector)

            #lectura del csv de los hoteles
            for fila in lector:
                nombre, direccion, telefono, habitaciones_disponibles, nro_reservas = fila
                habitaciones_disponibles = int(habitaciones_disponibles) #parseo a entero
                nro_reservas = int(nro_reservas) #parseo a entero
                nuevo_hotel = Hotel(nombre, direccion, telefono, habitaciones_disponibles, nro_reservas)
                self.agregar(nombre, direccion, telefono, habitaciones_disponibles, nro_reservas)

    #agregar hotel
    def agregar(self, nombre, direccion, telefono, habitaciones_disponibles, nro_reservas):

        nuevo_hotel = Hotel(nombre, direccion, telefono, habitaciones_disponibles, nro_reservas)
        
        nuevo_hotel.habitaciones_disponibles = habitaciones_disponibles        
        
        nuevo_nodo = NodoHotel(nuevo_hotel)        

        if not self.inicio:
            self.inicio = nuevo_nodo
        else:
            nodo_actual = self.inicio
            while nodo_actual.siguiente:
                nodo_actual = nodo_actual.siguiente
            nodo_actual.siguiente = nuevo_nodo

    def crear(self, nombre, direccion, telefono, habitaciones_disponibles, nro_reservas):
        try:
            nuevo_hotel = Hotel(nombre, direccion, telefono, habitaciones_disponibles, nro_reservas)
            
            with open(f'habitaciones_{nombre.lower()}.csv','w',newline='') as nuevo_csv: #creacion del nuevo archivo de habitaciones
                escritor = csv.writer(nuevo_csv,delimiter=';')
                escritor.writerow(['Numero Habitaciones', 'Disponibilidad']) #encabezados de habitaciones

                for i in range(1,habitaciones_disponibles + 1):
                    escritor.writerow([i, 'Disponible'])

                for i in range(habitaciones_disponibles + 1, habitaciones_disponibles + nro_reservas + 1):
                    escritor.writerow([i, 'No Disponible'])

            with open(f'reservaciones_{nombre.lower()}.csv','w',newline='') as nuevo_csv: #creacion del nuevo archivo de reservas
                escritor = csv.writer(nuevo_csv, delimiter=';')
                escritor.writerow(['Nombre', 'Fecha Reserva', 'Fecha Entrada', 'Fecha Salida', 'Nro Habitacion', #encabezados de reservas
                                    'Duracion Estadia', 'Tipo Habitacion', 'Nro Personas', 'Telefono', 'Contacto', 
                                    'Precio Total', 'ID'])

            nuevo_hotel.habitaciones_disponibles = habitaciones_disponibles        
            
            nuevo_nodo = NodoHotel(nuevo_hotel)        

            if not self.inicio:
                self.inicio = nuevo_nodo
            else:
                nodo_actual = self.inicio
                while nodo_actual.siguiente:
                    nodo_actual = nodo_actual.siguiente
                nodo_actual.siguiente = nuevo_nodo
        except FileNotFoundError as e:
            print("Error: ",e)
            descripcion_registro = e
            elemento_registrado = registrar('Error',descripcion_registro)
            pila_registros.apilar(elemento_registrado)


    #modificar hotel
    def modificar(self, nombre, nueva_direccion, nuevo_telefono,nuevas_habitaciones_disponibles,nuevos_nros_reserva):
        nodo_actual = self.inicio
        while nodo_actual:
            if nodo_actual.hotel.nombre == nombre:
                nodo_actual.hotel.direccion = nueva_direccion
                nodo_actual.hotel.telefono = nuevo_telefono
                nodo_actual.hotel.habitaciones_disponibles = nuevas_habitaciones_disponibles
                nodo_actual.hotel.nro_reservas = nuevos_nros_reserva

                self.actualizar_modificacion(nombre, nueva_direccion, nuevo_telefono, nuevas_habitaciones_disponibles, nuevos_nros_reserva)
                return
            nodo_actual = nodo_actual.siguiente

    def actualizar_modificacion(self, nombre, nueva_direccion, nuevo_telefono, nuevas_habitaciones_disponibles, nuevos_nros_reserva):

        # actualizar csv de hoteles
        try:
            datos = []
            with open('hoteles.csv', 'r', newline='', encoding='utf-8') as archivo_csv:
                lector = csv.reader(archivo_csv, delimiter=';')
                # Buscar y modificar la información del hotel
                for fila in lector:
                    if fila[0] == nombre:
                        fila[1] = nueva_direccion
                        fila[2] = nuevo_telefono
                        fila[3] = str(nuevas_habitaciones_disponibles)  # Convertir a str para escribir en CSV
                        fila[4] = str(nuevos_nros_reserva)  # Convertir a str para escribir en CSV

                    datos.append(fila)
            
            # actualizar csv de reservas
            with open('hoteles.csv', 'w', newline='') as archivo_csv:
                escritor = csv.writer(archivo_csv, delimiter=';')
                escritor.writerows(datos)

            with open(f'habitaciones_{nombre.lower()}.csv','w',newline='') as nuevo_csv: #creacion del nuevo archivo de habitaciones
                escritor = csv.writer(nuevo_csv,delimiter=';')
                escritor.writerow(['Numero Habitaciones', 'Disponibilidad']) #encabezados de habitaciones

                for i in range(1,nuevas_habitaciones_disponibles + 1):
                    escritor.writerow([i, 'Disponible'])

                for i in range(nuevas_habitaciones_disponibles + 1, nuevas_habitaciones_disponibles + nuevos_nros_reserva + 1):
                    escritor.writerow([i, 'No Disponible'])
        except FileNotFoundError as e:
            print("Error: ",e)
            descripcion_registro = e
            elemento_registrado = registrar('Error',descripcion_registro)
            pila_registros.apilar(elemento_registrado)


    #listar hoteles
    def listar(self):
        nodo_actual = self.inicio
        while nodo_actual:
            print("Nombre: ", nodo_actual.hotel.nombre)
            print("Direccion: ", nodo_actual.hotel.direccion)
            print("Telefono: ", nodo_actual.hotel.telefono)
            print("Habitaciones disponibles: ", nodo_actual.hotel.habitaciones_disponibles)
            print("Numero de Reservas: ", nodo_actual.hotel.nro_reservas)
            print("\n-------------------------------------\n")
            nodo_actual = nodo_actual.siguiente

    #eliminar hoteles
    def eliminar(self, nombre):
        if not self.inicio:
            return

        #verificar hotel existe
        if self.inicio.hotel.nombre == nombre:
            os.remove(f'habitaciones_{nombre.lower()}.csv') #elimina el archivo de habitaciones
            os.remove(f'reservaciones_{nombre.lower()}.csv') #elimina el archivo de reservas
            self.inicio = self.inicio.siguiente
            return

        nodo_anterior = self.inicio
        nodo_actual = self.inicio.siguiente
        while nodo_actual:
            if nodo_actual.hotel.nombre == nombre:
                os.remove(f'habitaciones_{nombre.lower()}.csv') #elimina el archivo de habitaciones
                os.remove(f'reservaciones_{nombre.lower()}.csv') #elimina el archivo de reservas                
                nodo_anterior.siguiente = nodo_actual.siguiente
                return
            nodo_anterior = nodo_actual
            nodo_actual = nodo_actual.siguiente       

    #actualizar csv de los hoteles
    def actualizar_csv(self,archivo):
        try:
            with open(archivo, 'w',newline='') as archivo_csv:
                sobreescritura = csv.writer(archivo_csv, delimiter=';')
                sobreescritura.writerow(['Nombre', 'Direccion', 'Telefono', 'Habitaciones Disponibles', 'Numero de Reservas'])
                nodo_actual = self.inicio
                while nodo_actual:
                    hotel = nodo_actual.hotel
                    sobreescritura.writerow([hotel.nombre, hotel.direccion, hotel.telefono, hotel.habitaciones_disponibles, hotel.nro_reservas])
                    nodo_actual = nodo_actual.siguiente
        except FileNotFoundError as e:
            print("Error: ",e)
            descripcion_registro = e
            elemento_registrado = registrar('Error',descripcion_registro)
            pila_registros.apilar(elemento_registrado)

class ListaHabitaciones:
    def __init__(self):
        self.inicio = None

    def agregar_habitacion (self, numero, disponibilidad):
        nueva_habitacion = NodoHabitacion(numero, disponibilidad)
        if not self.inicio:
            self.inicio = nueva_habitacion
        else:
            nodo_actual = self.inicio
            while nodo_actual.siguiente:
                nodo_actual = nodo_actual.siguiente
            nodo_actual.siguiente = nueva_habitacion

    def cargar_desde_csv(self, archivo):
        with open(f'habitaciones_{archivo}.csv', 'r') as archivo_csv:
            lector = csv.reader(archivo_csv, delimiter=';')
            next(lector)

            for fila in lector:
                numero_habitacion, disponibilidad = fila
                numero_habitacion = int(numero_habitacion)
                self.agregar_habitacion(numero_habitacion, disponibilidad)

    def guardar_a_csv(self, archivo):
        with open(archivo, 'w', newline='') as archivo_csv:
            sobreescritura = csv.writer(archivo_csv, delimiter=';')
            nodo_actual = self.inicio
            while nodo_actual:
                sobreescritura.writerow([nodo_actual.numero, nodo_actual.disponibilidad])
                nodo_actual = nodo_actual.siguiente

    def listar_habitaciones(self):
        nodo_actual = self.inicio
        while nodo_actual:
            print("Numero de habitacion:",nodo_actual.numero)
            print("Disponibilidad:",nodo_actual.disponibilidad)
            print("\n------------------------------------\n")
            nodo_actual = nodo_actual.siguiente

    def consultar_disponibilidad(self, numero_habitacion):
        nodo_actual = self.inicio
        while nodo_actual:
            if nodo_actual.numero == numero_habitacion:
                return nodo_actual.disponibilidad
            nodo_actual = nodo_actual.siguiente
        return None

    def modificar_disponibilidad(self, numero_habitacion, nueva_disponibilidad):
        nodo_actual = self.inicio
        while nodo_actual:
            if nodo_actual.numero == numero_habitacion:
                nodo_actual.disponibilidad = nueva_disponibilidad
                return
            nodo_actual = nodo_actual.siguiente

class Reservacion:
    def __init__(self,nombre,fecha_reserva,fecha_entrada,fecha_salida,nro_habitacion,duracion_estadia,tipo_habitacion,nro_personas,telefono,contacto,precio_total,id):
        self.nombre = nombre
        self.fecha_reserva = fecha_reserva
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.nro_habitacion = nro_habitacion
        self.duracion_estadia = duracion_estadia
        self.tipo_habitacion = tipo_habitacion
        self.nro_personas = nro_personas
        self.telefono = telefono
        self.contacto = contacto
        self.precio_total = precio_total
        self.id = id
    
    def obtener_datos(self):
        return [self.nombre, self.fecha_reserva, self.fecha_entrada, self.fecha_salida, self.nro_habitacion,
                self.duracion_estadia, self.tipo_habitacion, self.nro_personas, self.telefono, self.contacto,
                self.precio_total, self.id]

    def __str__(self):
        return f"{self.nombre} {self.fecha_reserva} {self.fecha_entrada} {self.fecha_salida} {self.nro_habitacion} {self.duracion_estadia} {self.tipo_habitacion} {self.nro_personas} {self.telefono} {self.contacto} {self.precio_total} {self.id}"
    
class Reservaciones:
    def __init__(self, archivo_csv):
        self.archivo_csv = archivo_csv
    
    def guardar_csv(self, archivo, nueva_reserva): #modificacion de archivo csv de reservas
        with open(archivo, 'a', newline='') as archivo_csv:
            escritor = csv.writer(archivo_csv, delimiter=';')
            escritor.writerow(nueva_reserva.obtener_datos())

    def cargar_datos(self):
        datos = []
        with open(self.archivo_csv, 'r', newline='') as archivo:
            lector_csv = csv.reader(archivo,delimiter=";")
            next(lector_csv)
            for fila in lector_csv:
                reservacion = None
                reservacion = Reservacion(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], fila[9], fila[10],fila[11])
                datos.append(reservacion)
            return datos

    def eliminar_reservacion(self, id_reserva):
            datos = self.cargar_datos()  # Obtén todos los datos

            # Encuentra la reservación con el ID dado
            reservacion_encontrada = None
            for reservacion in datos:
                if reservacion.id == id_reserva:
                    reservacion_encontrada = reservacion
                    break

            if reservacion_encontrada:
                datos.remove(reservacion_encontrada)  # Elimina la reservación

                # Sobrescribe el archivo CSV con los datos actualizados
                with open(self.archivo_csv, 'w', newline='') as archivo:
                    escritor = csv.writer(archivo, delimiter=';')
                    escritor.writerow(['Nombre', 'Fecha Reserva', 'Fecha Entrada', 'Fecha Salida', 'Nro Habitacion',
                                    'Duracion Estadia', 'Tipo Habitacion', 'Nro Personas', 'Telefono', 'Contacto',
                                    'Precio Total', 'ID'])

                    for reserva in datos:
                        escritor.writerow([reserva.nombre, reserva.fecha_reserva, reserva.fecha_entrada, reserva.fecha_salida,
                                        reserva.nro_habitacion, reserva.duracion_estadia, reserva.tipo_habitacion,
                                        reserva.nro_personas, reserva.telefono, reserva.contacto, reserva.precio_total,
                                        reserva.id])
                print("Reservación eliminada exitosamente.")
            else:
                raise ValueError("No se encontró una reservación con el ID proporcionado.")

    def modificar_reservacion(self, id_reserva, nombre, fecha_reserva, fecha_entrada, fecha_salida, nro_habitacion,
                            duracion_estadia, tipo_habitacion, nro_personas, telefono, correo, precio_total):
        datos = self.cargar_datos()
        for reserva in datos:
            if reserva.id == id_reserva:
                # Modifica los datos de la reserva
                reserva.nombre = nombre
                reserva.fecha_reserva = fecha_reserva
                reserva.fecha_entrada = fecha_entrada
                reserva.fecha_salida = fecha_salida
                reserva.nro_habitacion = nro_habitacion
                reserva.duracion_estadia = duracion_estadia
                reserva.tipo_habitacion = tipo_habitacion
                reserva.nro_personas = nro_personas
                reserva.telefono = telefono
                reserva.contacto = correo
                reserva.precio_total = precio_total
            else:
                raise ValueError("El id introducido para modificar no existe en el sistema")

        # Guarda los datos modificados en el archivo CSV
        with open(self.archivo_csv, 'w', newline='') as archivo:
            escritor = csv.writer(archivo, delimiter=';')
            # Escribe los encabezados
            escritor.writerow(['Nombre', 'Fecha Reserva', 'Fecha Entrada', 'Fecha Salida', 'Nro Habitacion',
                            'Duracion Estadia', 'Tipo Habitacion', 'Nro Personas', 'Telefono', 'Contacto',
                            'Precio Total', 'ID'])
            # Escribe las reservas modificadas
            for reserva in datos:
                escritor.writerow([reserva.nombre, reserva.fecha_reserva, reserva.fecha_entrada, reserva.fecha_salida,
                                reserva.nro_habitacion, reserva.duracion_estadia, reserva.tipo_habitacion,
                                reserva.nro_personas, reserva.telefono, reserva.contacto, reserva.precio_total,
                                reserva.id])         

class NodoCola:
    def __init__(self, objeto):
        self.objeto = objeto
        self.siguiente = None

class ColaReservaciones:
    def __init__(self):
        self.frente = None
        self.final = None

    def esta_vacia(self):
        return self.frente is None

    def encolar(self, objeto):
        nuevo_nodo = NodoCola(objeto)
        if self.final is None:
            self.frente = self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        print("{:<12} {:<15} {:<15} {:<15} {:<12} {:<8} {:<14} {:<8} {:<14} {:<32} {:<8} {:<6}".format(objeto.nombre,objeto.fecha_reserva,objeto.fecha_entrada,objeto.fecha_salida,objeto.nro_habitacion,objeto.duracion_estadia,objeto.tipo_habitacion,objeto.nro_personas,objeto.telefono,objeto.contacto,objeto.precio_total,objeto.id))

    def imprimir(self): #listar reservaciones
        nodo_actual = self.frente

        while nodo_actual:
            print("{:<12} {:<15} {:<15} {:<15} {:<12} {:<8} {:<14} {:<8} {:<14} {:<32} {:<8} {:<6}".format(nodo_actual.objeto.nombre,nodo_actual.objeto.fecha_reserva,nodo_actual.objeto.fecha_entrada,nodo_actual.objeto.fecha_salida,nodo_actual.objeto.nro_habitacion,nodo_actual.objeto.duracion_estadia,nodo_actual.objeto.tipo_habitacion,nodo_actual.objeto.nro_personas,nodo_actual.objeto.telefono,nodo_actual.objeto.contacto,nodo_actual.objeto.precio_total,nodo_actual.objeto.id))
            nodo_actual = nodo_actual.siguiente

    def eliminar_reservacion_y_sobreescribir_csv(self, id_reserva, archivo_csv):
        nodo_actual = self.frente
        nodo_anterior = None

        while nodo_actual:
            if nodo_actual.objeto.id == id_reserva:
                if nodo_anterior:
                    nodo_anterior.siguiente = nodo_actual.siguiente
                else:
                    # Si el nodo a eliminar es el primero de la cola
                    self.frente = nodo_actual.siguiente

                if nodo_actual == self.final:
                    # Si el nodo a eliminar es el último de la cola
                    self.final = nodo_anterior

                print("\nReservación eliminada exitosamente")

                # Sobreescribir el archivo CSV con el contenido actualizado
                with open(archivo_csv, 'w', newline='') as archivo:
                    escritor_csv = csv.writer(archivo, delimiter=";")
                    escritor_csv.writerow(["Nombre", "Fecha Reservacion", "Fecha Entrada", "Fecha Salida", "Nro Habitacion", "Duracion de la Estadía (días)", "Tipo de Habitacion", "Nro Personas", "Telefono", "Contacto", "Precio Total ($)", "ID"])
                    nodo_actual = self.frente
                    while nodo_actual:
                        objeto = nodo_actual.objeto
                        escritor_csv.writerow([objeto.nombre, objeto.fecha_reserva, objeto.fecha_entrada, objeto.fecha_salida, objeto.nro_habitacion, objeto.duracion_estadia, objeto.tipo_habitacion, objeto.nro_personas, objeto.telefono, objeto.contacto, objeto.precio_total, objeto.id])
                        nodo_actual = nodo_actual.siguiente
                return
            
            nodo_anterior = nodo_actual
            nodo_actual = nodo_actual.siguiente


#METODOS DE VALIDACION
def registrar(tipo,descripcion):
    fecha = datetime.datetime.today().strftime("%d de %B de %Y")
    hora = datetime.datetime.now().strftime("%H:%M:%S")
    cadena = tipo,descripcion,fecha,hora
    return cadena

def validar_nombre(nombre):
    if not nombre.isalpha():
        raise ValueError("Se introdujo un nombre con caracteres especiales y/o numeros")
    else:
        print("\nNombre validado")

def validar_fecha(fecha):
    patron = r'^\d{2}/\d{2}/\d{4}$'
    if re.match(patron, fecha):
        datetime.datetime.strptime(fecha, '%d/%m/%Y')
        return True
    return False

def validar_direccion(direccion):
    if not direccion:
        raise ValueError("\nNo se introdujo ninguna direccion")
    else:
        print("\nDireccion Validada")

def validar_numero_telefonico(numero):
    # Patrón de expresión regular para el formato 0XXX-XXXXXX
    patron = r'^0\d{3}-\d{7}$'
    # Verifica si el número coincide con el patrón
    if re.match(patron, numero):
        return True
    else:
        return False

def validar_habitaciones_disponibles(habitaciones_disponibles):
    if habitaciones_disponibles < 0:
        raise ValueError("\nSe introdujo un numero de habitaciones negativo")
    else:
        print("\nNumero de habitaciones disponibles validada")

def validar_reservaciones(numero_reservaciones):
    if numero_reservaciones < 0:
        raise ValueError("\nSe introdujo un numero de reservaciones negativo")
    else:
        print("\nNumero de reservaciones validada")

def validar_numero_de_habitacion(numero_habitacion):
    if numero_habitacion < 0:
        raise ValueError("\nLos numeros de habitacion negativos no existen")
    else:
        print("\nNumero de habitacion validada")

def validar_disponibilidad(disponibilidad):
    if disponibilidad == 'disponible':
        print("Estado: Disponible")
        print("Disponibilidad validada")
        
    elif disponibilidad == 'no disponible':
        print("Estado: No Disponible")
        print("Disponibilidad validada")        
    else:
        raise ValueError("No se introdujo la disponibilidad tal y como fue indicado")

def validar_estadia(estadia):
    if estadia < 0:
        raise ValueError("\nSe introdujo un numero invalido para la estadia")
    else:
        print("\nDuracion de la estadia validada")

def validar_tipo_habitacion(tipo):
    if not tipo.isalpha():
        raise ValueError("\nSe introdujeron caracteres especiales y/o numeros")
    else:
        print("\nTipo de habitacion validado")

def validar_nro_personas(num_personas):
    if num_personas < 0:
        raise ValueError("\nEl numero que se introdujo de personas es negativo")
    else:
        print("\nNumero de personas validado")

def validar_correo(correo):
    # Patrón para validar una dirección de correo electrónico
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(patron, correo):
        return True
    else:
        return False

def validar_precio(precio):
    if precio < 0:
        raise ValueError("\nEl precio que se introdujo fue negativo")
    else:
        print("\nPrecio validado")

def validar_id(id):
    if id < 0:
        raise ValueError("\nEl ID que se introdujo fue negativo")
    else:
        print("\nID validado")

def validar_str_id(id_modificar):
    valor = float(id_modificar)
    if  valor >= 0:
        print("\nID a modificar validado")
    else:
        raise ValueError("\nSe introdujo un numero invalido en el ID de la reserva a modificar")

#GESTION DE HOTELES
def gestionHoteles(lista_hoteles):
    opcion_2 = 0
    while True:
        try:
            descripcion_registro = ''
            print("\nSeleccione una opcion:")
            print("1. Crear otro hotel")
            print("2. Modificar hotel")
            print("3. Listar hoteles")
            print("4. Eliminar Hotel")
            print("5. Configuracion de Habitaciones de Hoteles")
            print("6. Regresar")
            opcion_2 = int(input())
            
            if opcion_2 == 1: #creacion de hotel

                print("\nSelecciono: Crear otro hotel")
                nombre = input("\nIntroduzca el nombre del hotel: ")
                if not nombre:
                    raise ValueError("\nNo se introdujo ningun nombre")
                else:
                    validar_nombre(nombre)

                direccion = input("\nIntroduzca la direccion del hotel: ")
                validar_direccion(direccion)

                telefono = input("\nIntroduzca el numero telefonico (0XXX-XXXXXXX): ")
                if not telefono:
                    raise ValueError("No se introdujo ningun numero telefonico")
                else:
                    if validar_numero_telefonico(telefono):
                        print("\nNumero telefonico Validado")
                    else:
                        raise ValueError("Se introdujo un numero de telefono con el formato incorrecto")
                    
                habitaciones_disponibles = int(input("\nIntroduzca el numero de habitaciones: "))
                validar_habitaciones_disponibles(habitaciones_disponibles)
                nro_reservas = int(input("\nIntroduzca el numero de reservas: "))
                validar_reservaciones(nro_reservas)
                lista_hoteles.crear(nombre, direccion, telefono, habitaciones_disponibles, nro_reservas)
                
                descripcion_registro = 'Se creó de manera exitosa el hotel ',nombre
                elemento_registrado = registrar('Accion',descripcion_registro)

                pila_registros.apilar(elemento_registrado)
            
            elif opcion_2 == 2: #modificacion de hotel
                print("\nSelecciono: Modificar hotel")
                nodo_actual = lista_hoteles.inicio
                while nodo_actual:
                    nodo_actual = nodo_actual.siguiente

                nombre_hotel_modificar = input("\nIntroduzca el nombre del hotel a modificar: ")
                if not nombre_hotel_modificar:
                    raise ValueError("No se introdujo ningun nombre de hotel a modificar")
                else:
                    validar_nombre(nombre_hotel_modificar)

                #Verificar si el hotel existe
                existe = False
                nodo_actual = lista_hoteles.inicio
                while nodo_actual:
                    if nodo_actual.hotel.nombre == nombre_hotel_modificar:
                        existe = True
                        break
                    nodo_actual = nodo_actual.siguiente

                if existe:
                    nueva_direccion = input("Introduce una nueva direccion: ")
                    if not nueva_direccion:
                        raise ValueError("No se introdujo ninguna direccion")
                    else:
                        print("")
                        print("Direccion Validada")
                    nuevo_telefono = input("\nIntroduce un nuevo numero telefonico: ")
                    if not nuevo_telefono:
                        raise ValueError("\nNo se introdujo ningun numero telefonico")
                    else:
                        if validar_numero_telefonico(nuevo_telefono):
                            print("\nNumero telefonico Validado")
                        else:
                            raise ValueError("\nSe introdujo un numero de telefono con el formato incorrecto")
                        
                    nuevo_habitaciones_disponibles = int(input("\nIntroduce un nuevo numero de habitaciones disponibles: "))
                    validar_habitaciones_disponibles(nuevo_habitaciones_disponibles)

                    nuevo_nro_reservas = int(input("\nIntroduce un nuevo numero de reservas disponibles: "))
                    validar_reservaciones(nuevo_nro_reservas)

                    lista_hoteles.modificar(nombre_hotel_modificar, nueva_direccion, nuevo_telefono,nuevo_habitaciones_disponibles, nuevo_nro_reservas)
                    
                    descripcion_registro = 'Se hizo la modificacion de manera exitosa sobre el hotel ',nombre_hotel_modificar
                    elemento_registrado = registrar('Accion',descripcion_registro)
                    
                    pila_registros.apilar(elemento_registrado)

                else:
                    raise ValueError("El hotel a modificar no existe")

            elif opcion_2 == 3: #listar hoteles

                print("\nSelecciono: Listar hoteles\n")
                lista_hoteles.listar()

                descripcion_registro = 'Se listó los hoteles actuales'
                elemento_registrado = registrar('Accion',descripcion_registro)

                pila_registros.apilar(elemento_registrado)
                
            elif opcion_2 == 4: #eliminar hotel
                print("\nSelecciono: Eliminar hoteles\n")
                nombre_hotel_eliminar = input("\nIntroduzca el nombre del hotel a eliminar: ")
                if not nombre_hotel_eliminar:
                    raise ValueError("No se introdujo ningun nombre del hotel a eliminar")
                else:
                    validar_nombre(nombre)

                #Verificar si el hotel existe
                existe = False
                nodo_actual = lista_hoteles.inicio
                while nodo_actual:
                    if nodo_actual.hotel.nombre == nombre_hotel_eliminar:
                        existe = True
                        break
                    nodo_actual = nodo_actual.siguiente

                if existe:
                    lista_hoteles.eliminar(nombre_hotel_eliminar)
                    descripcion_registro = 'Se eliminó el hotel ',nombre_hotel_eliminar
                    elemento_registrado = registrar('Accion',descripcion_registro)

                    pila_registros.apilar(elemento_registrado)

                else:
                    raise ValueError("El hotel a eliminar no existe")

            elif opcion_2 == 5: #configuracion de habitaciones de hoteles
                print("\nSelecciono: Configuracion de Habitaciones de Hoteles\n")

                print("\nLista de Hoteles: \n")
                lista_hoteles.listar()
                habitaciones_hotel_modificar = input("\nIntroduzca el nombre del hotel a modificar: ")
                
                if not habitaciones_hotel_modificar:
                    ValueError("No se introdujo ningun nombre de hotel a configurar")
                else:
                    validar_nombre(habitaciones_hotel_modificar)

                existe = False #verificar si el nombre del hotel existe
                nodo_actual = lista_hoteles.inicio
                while nodo_actual:
                    if nodo_actual.hotel.nombre == habitaciones_hotel_modificar:
                        existe = True
                        break
                    nodo_actual = nodo_actual.siguiente
                
                if existe:

                    hotel = nodo_actual.hotel
                    habitaciones = ListaHabitaciones() #se instancia un objeto de la clase ListaHabitaciones()
                    habitaciones.cargar_desde_csv(habitaciones_hotel_modificar) #se cargan los registros de habitaciones y disponibilidades
                    
                    descripcion_registro = 'Se inicia una configuracion del hotel ',habitaciones_hotel_modificar
                    elemento_registrado = registrar('Accion',descripcion_registro)
                    
                    pila_registros.apilar(elemento_registrado)
                    
                    while True:
                        print("\nSeleccione una opcion: ")
                        print("1. Crear habitacion")
                        print("2. Modificar habitacion")
                        print("3. Listar habitaciones")
                        print("4. Consultar disponibilidad de una habitacion")
                        print("5. Guardar cambios y volver")
                        opcion = int(input())

                        if opcion == 1: #creacion de habitacion

                            numero_habitacion = int(input("Introduzca el numero de la habitacion: "))
                            validar_numero_de_habitacion(numero_habitacion)
                            disponibilidad = input("Introduzca la disponibilidad (Disponible, No Disponible): ").strip().lower()
                            validar_disponibilidad(disponibilidad)
                            habitaciones.agregar_habitacion(numero_habitacion, disponibilidad)

                            descripcion_registro = 'Se creó una nueva habitacion del hotel ',habitaciones_hotel_modificar
                            elemento_registrado = registrar('Accion',descripcion_registro)

                            pila_registros.apilar(elemento_registrado)

                        elif opcion == 2: #modificacion de habitacion

                            numero_habitacion = int(input("Introduzca el numero de la habitacion a modificar: "))
                            validar_numero_de_habitacion(numero_habitacion)
                            disponibilidad = input("Introduzca la nueva disponibilidad (Disponible, No Disponible): ").strip().lower()
                            validar_disponibilidad(disponibilidad)
                            habitaciones.modificar_disponibilidad(numero_habitacion, disponibilidad)
                            
                            descripcion_registro = 'Se modifico la habitacion ',numero_habitacion,' del hotel ',habitaciones_hotel_modificar
                            elemento_registrado = registrar('Accion',descripcion_registro)
                            
                            pila_registros.apilar(elemento_registrado)

                        elif opcion == 3: #impresion de habitaciones

                            habitaciones.listar_habitaciones()
                            descripcion_registro = 'Se listaron las habitaciones del hotel ',habitaciones_hotel_modificar
                            elemento_registrado = registrar('Accion',descripcion_registro)
                            
                            pila_registros.apilar(elemento_registrado)

                        elif opcion == 4: #consulta de disponibilidad

                            numero_habitacion = int(input("Introduzca el numero de la habitacion a consultar: "))
                            validar_numero_de_habitacion(numero_habitacion)
                            disponibilidad = habitaciones.consultar_disponibilidad(numero_habitacion)

                            if disponibilidad is not None:
                                print("La disponibilidad de la habitacion ",numero_habitacion," es ",disponibilidad)
                                descripcion_registro = 'Se busco la disponibilidad de la habitacion numero ',numero_habitacion,' del hotel ',habitaciones_hotel_modificar
                                elemento_registrado = registrar('Accion',descripcion_registro)
                                pila_registros.apilar(elemento_registrado)
                            else:
                                raise ValueError("No se encontro la habitacion numero ",numero_habitacion)
                            
                        elif opcion == 5:
                            print("")
                            habitaciones.guardar_a_csv(hotel.nombre) #sobreescritura de csv de habitaciones
                            break

                else:
                    raise ValueError("El hotel a configurar no existe o se escribio de manera incorrecta.")
                      
            elif opcion_2 == 6:
                break

        except Exception as e: #aqui se listan errores
            print("\nError: ",e)
            descripcion_registro = e
            elemento_registrado = registrar('Error',descripcion_registro)
            pila_registros.apilar(elemento_registrado)

#GESTION DE RESERVACIONES
def gestionReservaciones():

    try:

        while True:

            descripcion_registro = ''
            archivo_reservaciones = input("\nIntroduzca el nombre del hotel para la configuracion de reservaciones: ")
            if not archivo_reservaciones:
                raise ValueError("\nNo se introdujo ningun nombre de hotel\n")
            else:
                validar_nombre(archivo_reservaciones) #se valida el nombre del hotel
                archivo_reservas = f'reservaciones_{archivo_reservaciones}.csv' #se guarda el nombre del archvio junto con su extension csv de reservaciones
                lista_reservas = Reservaciones(archivo_reservas) #Se carga el archivo CSV de las reservaciones en una instancia de la clase Reservaciones()
                lista = lista_reservas.cargar_datos()              
                cola = ColaReservaciones() #se instancia objeto

                print("\nNombre       F. Reserva      F. Entrada     F. Salida    Nro. Habit    Dur. Est   T. Habit    Nro Pers.       Telef             Cont                   Precio T.     ID")
                print("")
                for objeto in lista:
                    cola.encolar(objeto) #Se encolan los objetos de la clase Reservaciones

                print("\nOpcion seleccionada: Gestion de Reservaciones\n")
                print("\nSeleccione una opcion:")
                print("1. Crear reservacion")
                print("2. Modificar reservacion")
                print("3. Listar reservaciones")
                print("4. Eliminar reservacion")
                print("5. Regresar")
                accion = int(input())      

                if accion == 1:
                    
                    print("\nOpción seleccionada: Crear reservación\n")
                    print("Hotel selecionado (archivo): ",archivo_reservas)
                    nombre = input("Nombre del cliente: ")
                    if not nombre:
                        raise ValueError("No se introdujo ningun nombre")
                    else:
                        validar_nombre(nombre)
                    fecha_reserva = input("Fecha de reserva (DD/MM/YYYY): ")
                    if validar_fecha(fecha_reserva):
                        print("Fecha de reserva validada")
                        print("")
                    else:
                        raise ValueError("Se introdujo la fecha de reserva de manera incorrecta")
                    fecha_entrada = input("Fecha de entrada (DD/MM/YYYY): ")
                    if validar_fecha(fecha_entrada):
                        print("Fecha de entrada validada")
                        print("")
                    else:
                        raise ValueError("Se introdujo la fecha de entrada de manera incorrecta")
                    fecha_salida = input("Fecha de salida (DD/MM/YYYY): ")
                    if validar_fecha(fecha_salida):
                        print("Fecha de salida validada")
                        print("")
                    else:
                        raise ValueError("Se introdujo la fecha de salida de manera incorrecta")
                    nro_habitacion = int(input("Número de habitación: "))
                    validar_numero_de_habitacion(nro_habitacion)
                    duracion_estadia = int(input("Duración de la estancia (en días): "))
                    validar_estadia(duracion_estadia)
                    tipo_habitacion = input("Tipo de habitación: ")
                    if not tipo_habitacion:
                        raise ValueError("No se introdujo ningun tipo de habitacion")
                    else:
                        validar_tipo_habitacion(tipo_habitacion)
                    nro_personas = int(input("Número de personas: "))
                    validar_nro_personas(nro_personas)
                    telefono = input("Teléfono del cliente: ")
                    if not telefono:
                        raise ValueError("No se introdujo ningun numero telefonico")
                    else:
                        if validar_numero_telefonico(telefono):
                            print("Numero telefonico Validado")
                        else:
                            raise ValueError("Se introdujo un numero de telefono con el formato incorrecto")
                    correo = input("Correo del cliente: ")
                    if validar_correo(correo):
                        print("")
                        print("Correo validado")
                        print("")
                    else:
                        raise ValueError("El correo que se introdujo para crear una reservacion no fue validada")
                    precio_total = float(input("Precio total: "))
                    validar_precio(precio_total)
                    id_reserva = input("ID de la reserva: ")
                    validar_str_id(id_reserva)

                    descripcion_registro = 'Se creó exitosamente la reservacion en el hotel ',archivo_reservaciones
                    elemento_registrado = registrar('Accion',descripcion_registro)
                    pila_registros.apilar(elemento_registrado)

                    nueva_reservacion = Reservacion(nombre, fecha_reserva, fecha_entrada, fecha_salida, nro_habitacion,
                                                    duracion_estadia, tipo_habitacion, nro_personas, telefono, correo,
                                                    precio_total, id_reserva)

                    cola.encolar(nueva_reservacion) #Llamamos al método para encolar la nueva reservación
                    lista_reservas.guardar_csv(archivo_reservas, nueva_reservacion) #Se cambia el csv

                elif accion == 2:
                    id_reserva_modificar = input("Introduce el ID de la reserva a modificar: ")
                    if not id_reserva_modificar:
                        raise ValueError("No se introdujo ningun id de la reserva modificar")
                    else:
                        validar_str_id(id_reserva_modificar)
                    nuevo_nombre = input("Nombre del cliente: ")
                    if not nuevo_nombre:
                        raise ValueError("No se introdujo ningun nombre")
                    else:
                        validar_nombre(nombre)
                    nueva_fecha_reserva = input("Fecha de reserva (DD/MM/YYYY): ")
                    if not nueva_fecha_reserva:
                        raise ValueError("No se introdujo ninguna fecha de reserva nueva")
                    else:
                        if validar_fecha(nueva_fecha_reserva):
                            print("")
                            print("Fecha validada")
                        else:
                            raise ValueError("Se introdujo una fecha de reserva nueva con el formato incorrecto")
                    
                    nueva_fecha_entrada = input("Fecha de entrada (DD/MM/YYYY): ")
                    if not nueva_fecha_entrada:
                        raise ValueError("No se introdujo ninguna fecha de entrada nueva")
                    else:
                        if validar_fecha(nueva_fecha_entrada):
                            print("")
                            print("Fecha validada")
                        else:
                            raise ValueError("Se introdujo una fecha de entrada nueva con el formato incorrecto")
                    
                    nueva_fecha_salida = input("Fecha de salida (DD/MM/YYYY): ")
                    if not nueva_fecha_salida:
                        raise ValueError("No se introdujo ninguna fecha de salida nueva")
                    else:
                        if validar_fecha(nueva_fecha_salida):
                            print("")
                            print("Fecha validada")
                        else:
                            raise ValueError("Se introdujo una fecha de salida nueva con el formato incorrecto")
                        
                    nuevo_nro_habitacion = int(input("Número de habitación: "))
                    validar_numero_de_habitacion(nuevo_nro_habitacion)
                    nuevo_duracion_estadia = int(input("Duración de la estancia (en días): "))
                    validar_estadia(nuevo_duracion_estadia)
                    nuevo_tipo_habitacion = input("Tipo de habitación: ")
                    validar_tipo_habitacion(nuevo_tipo_habitacion)
                    nuevo_nro_personas = int(input("Número de personas: "))
                    validar_nro_personas(nuevo_nro_personas)
                    nuevo_telefono = input("Teléfono del cliente: ")

                    if not nuevo_telefono:
                        raise ValueError("\nNo se introdujo ningun numero telefonico\n")
                    else:
                        if validar_numero_telefonico(nuevo_telefono):
                            print("\nNumero telefonico nuevo Validado\n")
                        else:
                            raise ValueError("\nSe introdujo un numero de telefono nuevo con el formato incorrecto\n")
                    nuevo_correo = input("Correo del cliente: ")

                    if validar_correo(nuevo_correo):
                        print("\nNuevo correo validado\n")
                    else:
                        raise ValueError("\nEl correo que se introdujo para modificar una reservacion no fue validada\n")
                    
                    nuevo_precio_total = float(input("Precio total: "))
                    validar_precio(nuevo_precio_total)
                    descripcion_registro = 'Se modificó exitosamente la reservacion en el hotel ',archivo_reservaciones
                    elemento_registrado = registrar('Accion',descripcion_registro)
                    pila_registros.apilar(elemento_registrado)
                    lista_reservas.modificar_reservacion(id_reserva_modificar, nuevo_nombre, nueva_fecha_reserva, nueva_fecha_entrada, 
                                                            nueva_fecha_salida, nuevo_nro_habitacion, nuevo_duracion_estadia, 
                                                            nuevo_tipo_habitacion, nuevo_nro_personas, nuevo_telefono, nuevo_correo, nuevo_precio_total)
                elif accion == 3:

                    if not cola.esta_vacia():                
                        print("\nOpcion seleccionada: Listar reservaciones\n")
                        print("Nombre       F. Reserva      F. Entrada     F. Salida    Nro. Habit    Dur. Est   T. Habit    Nro Pers.       Telef             Cont                   Precio T.     ID")
                        print("")
                        cola.imprimir()
                        descripcion_registro = 'Se listaron las reservaciones creadas para el hotel ',archivo_reservaciones
                        elemento_registrado = registrar('Accion',descripcion_registro)
                        pila_registros.apilar(elemento_registrado)
                    else:
                        raise ValueError("No hubieron reservadas creadas")

                elif accion == 4:

                    print("\nOpcion seleccionada: Eliminar reservaciones\n")
                    id_a_eliminar = input("Introduzca el ID de la reserva a eliminar: ")
                    lista_reservas.eliminar_reservacion(id_a_eliminar)
                    descripcion_registro = 'Se elimino exitosamente la reservacion en el hotel ',archivo_reservaciones
                    elemento_registrado = registrar('Accion',descripcion_registro)
                    pila_registros.apilar(elemento_registrado)

                elif accion == 5:
                    break

    except Exception as e:
        print("Error: ",e)
        descripcion_registro = e
        elemento_registrado = registrar('Error',descripcion_registro)
        pila_registros.apilar(elemento_registrado)

def main():
    archivo = 'hoteles.csv' #variable del archivo de hoteles
    archivo_log = 'log_registros.csv' #variable del archivo de acciones/errore
    lista_hoteles = ListaHoteles() #instanciacion de un objeto de ListaHoteles()
    lista_hoteles.cargar_csv(archivo) #lectura del archivo.csv

    while True:

        try:
            opcion = 0
            print("\n****** BIENVENIDO AL SISTEMA DE GESTION DE HOTELERIA ******")
            print("Seleccione una opcion")
            print("1. Gestion de Hoteles")
            print("2. Gestion de Reservaciones")
            print("3. Modulo de Historial de Acciones")
            print("4. Salir")
            opcion = int(input())

            if opcion == 1:
                descripcion_registro = 'Se ingresó al modulo de Gestion de Hoteles'
                elemento_registrado = registrar('Accion',descripcion_registro)
                pila_registros.apilar(elemento_registrado)   
                gestionHoteles(lista_hoteles)

            elif opcion == 2:
                descripcion_registro = 'Se ingresó al modulo de Gestion de Reservaciones'
                elemento_registrado = registrar('Accion',descripcion_registro)
                pila_registros.apilar(elemento_registrado)   
                gestionReservaciones()

            elif opcion == 3:
                descripcion_registro = 'Se ingresó al modulo de registro de acciones y errores'
                elemento_registrado = registrar('Accion',descripcion_registro)
                pila_registros.apilar(elemento_registrado)
                logRegistrosyErrores(pila_registros,pila_nueva,archivo_log)
                
            elif opcion == 4:
                descripcion_registro = 'Se finalizó el programa'
                elemento_registrado = registrar('Accion',descripcion_registro)
                pila_registros.apilar(elemento_registrado)   
                break  

            else:
                raise ValueError("Se introdujo una opcion inexistente en el modulo Main")

        except Exception as e:
            print("Error ",e)
            descripcion_registro = e
            elemento_registrado = registrar('Error',descripcion_registro)
            pila_registros.apilar(elemento_registrado)                                                        
main()