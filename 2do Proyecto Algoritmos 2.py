import csv #manipulacion de archivos csv
import os #eliminacion de archivos csv

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
        
        habitaciones_hotel = ListaHabitaciones() #se crea instancia de ListaHabitaciones() para hacer un nuevo archivo csv

        with open(f'habitaciones_{nombre.lower()}.csv','w',newline='') as nuevo_csv: #creacion del nuevo archivo
            escritor = csv.writer(nuevo_csv,delimiter=';')
            escritor.writerow(['Numero Habitaciones', 'Disponibilidad']) #encabezados del nuevo archivo

            for i in range(1,habitaciones_disponibles + 1):
                escritor.writerow([i, 'Disponible'])

            for i in range(habitaciones_disponibles + 1, habitaciones_disponibles + nro_reservas + 1):
                escritor.writerow([i, 'No Disponible'])

        nuevo_hotel.habitaciones_disponibles = habitaciones_disponibles        
        
        nuevo_nodo = NodoHotel(nuevo_hotel)        

        if not self.inicio:
            self.inicio = nuevo_nodo
        else:
            nodo_actual = self.inicio
            while nodo_actual.siguiente:
                nodo_actual = nodo_actual.siguiente
            nodo_actual.siguiente = nuevo_nodo

    #modificar hotel
    def modificar(self, nombre, nueva_direccion, nuevo_telefono,nuevas_habitaciones_disponibles,nuevos_nros_reserva):
        nodo_actual = self.inicio
        while nodo_actual:
            if nodo_actual.hotel.nombre == nombre:
                nodo_actual.hotel.direccion = nueva_direccion
                nodo_actual.hotel.telefono = nuevo_telefono
                nodo_actual.hotel.habitaciones_disponibles = nuevas_habitaciones_disponibles
                nodo_actual.hotel.nro_reservas = nuevos_nros_reserva
                return
            nodo_actual = nodo_actual.siguiente

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
            self.inicio = self.inicio.siguiente
            return

        nodo_anterior = self.inicio
        nodo_actual = self.inicio.siguiente
        while nodo_actual:
            if nodo_actual.hotel.nombre == nombre:
                os.remove(f'habitaciones_{nombre.lower()}.csv') #elimina el archivo de habitaciones
                nodo_anterior.siguiente = nodo_actual.siguiente
                return
            nodo_anterior = nodo_actual
            nodo_actual = nodo_actual.siguiente       

    #actualizar csv de los hoteles
    def actualizar_csv(self,archivo):
        with open(archivo, 'w',newline='') as archivo_csv:
            sobreescritura = csv.writer(archivo_csv, delimiter=';')
            sobreescritura.writerow(['Nombre', 'Direccion', 'Telefono', 'Habitaciones Disponibles', 'Numero de Reservas'])
            nodo_actual = self.inicio
            while nodo_actual:
                hotel = nodo_actual.hotel
                sobreescritura.writerow([hotel.nombre, hotel.direccion, hotel.telefono, hotel.habitaciones_disponibles, hotel.nro_reservas])
                nodo_actual = nodo_actual.siguiente

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
        try:
            with open(f'habitaciones_{archivo}.csv', 'r') as archivo_csv:
                lector = csv.reader(archivo_csv, delimiter=';')
                next(lector)

                for fila in lector:
                    numero_habitacion, disponibilidad = fila
                    numero_habitacion = int(numero_habitacion)
                    self.agregar_habitacion(numero_habitacion, disponibilidad)
        except FileNotFoundError:
            print("No se encontro el archivo de habitaciones")

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

def main():

    archivo = 'hoteles.csv'
    lista_hoteles = ListaHoteles() #instanciacion de un objeto de ListaHoteles()
    lista_hoteles.cargar_csv(archivo) #lectura del archivo.csv

    opcion = 0
    opcion_2 = 0

    while True:
        print("\n****** BIENVENIDO AL SISTEMA DE GESTION DE HOTELERIA ******")
        print("Seleccione una opcion")
        print("1. Gestion de Hoteles")
        print("2. Gestion de Reservaciones")
        print("3. Modulo de Historial de Acciones")
        print("4. Salir")
        opcion = int(input())

        if opcion == 1:
            while True:
                print("\nSeleccione una opcion:")
                print("1. Crear otro hotel")
                print("2. Modificar hotel")
                print("3. Listar hoteles")
                print("4. Eliminar Hotel")
                print("5. Configuracion de Habitaciones de Hoteles")
                print("6. Regresar")
                opcion_2 = int(input())
                
                if opcion_2 == 1: #creacion de hotel
                    print("Selecciono: Crear otro hotel")
                    nombre = input("Introduzca el nombre del hotel: ")
                    direccion = input("Introduzca la direccion del hotel: ")
                    telefono = input("Introduzca el numero telefonico: ")
                    habitaciones_disponibles = int(input("Introduzca el numero de habitaciones: "))
                    nro_reservas = int(input("Introduzca el numero de reservas: "))
                    lista_hoteles.agregar(nombre, direccion, telefono, habitaciones_disponibles, nro_reservas)
                
                elif opcion_2 == 2: #modificacion de hotel
                    print("\nSelecciono: Modificar hotel")
                    nodo_actual = lista_hoteles.inicio
                    while nodo_actual:
                        nodo_actual = nodo_actual.siguiente

                    nombre_hotel_modificar = input("\nIntroduzca el nombre del hotel a modificar: ")
                    
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
                        nuevo_telefono = input("Introduce un nuevo numero telefonico: ")
                        nuevo_habitaciones_disponibles = int(input("Introduce un nuevo numero de habitaciones disponibles: "))
                        nuevo_nro_reservas = int(input("Introduce un nuevo numero de reservas disponibles: "))

                        lista_hoteles.modificar(nombre_hotel_modificar, nueva_direccion, nuevo_telefono,nuevo_habitaciones_disponibles, nuevo_nro_reservas)
                    else:
                        print("\nNo existe")

                elif opcion_2 == 3: #listar hoteles
                    print("\nSelecciono: Listar hoteles\n")
                    lista_hoteles.listar()
                    
                elif opcion_2 == 4: #eliminar hotel
                    print("\nSelecciono: Eliminar hoteles\n")
                    nombre_hotel_eliminar = input("\nIntroduzca el nombre del hotel a eliminar: ")
                    
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
                    else:
                        print("\nNo existe")

                elif opcion_2 == 5: #configuracion de habitaciones de hoteles
                    print("\nSelecciono: Configuracion de Habitaciones de Hoteles\n")
                    print("\nLista de Hoteles: ")
                    lista_hoteles.listar()
                    habitaciones_hotel_modificar = input("\nIntroduzca el nombre del hotel a modificar: ")

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
                                disponibilidad = input("Introduzca la disponibilidad (Disponible, No Disponible): ").lower()
                                habitaciones.agregar_habitacion(numero_habitacion, disponibilidad)

                            elif opcion == 2: #modificacion de habitacion    
                                numero_habitacion = int(input("Introduzca el numero de la habitacion a modificar: "))
                                disponibilidad = input("Introduzca la nueva disponibilidad (Disponible, No Disponible): ").lower()
                                habitaciones.modificar_habitaciones(numero_habitacion, disponibilidad)

                            elif opcion == 3: #impresion de habitaciones
                                habitaciones.listar_habitaciones()

                            elif opcion == 4: #consulta de disponibilidad
                                numero_habitacion = int(input("Introduzca el numero de la habitacion a consultar: "))
                                disponibilidad = habitaciones.consultar_disponibilidad(numero_habitacion)
                                if disponibilidad is not None:
                                    print("La disponibilidad de la habitacion",numero_habitacion,"es",disponibilidad)
                                else:
                                    print("No se encontro la habitacion numero",numero_habitacion)
                            elif opcion == 5:
                                print("")
                                #habitaciones.guardar_a_csv(hotel.nombre) #sobreescritura de csv de habitaciones
                    else:
                        print("Hotel no existente")            
                elif opcion_2 == 6:
                    break
        elif opcion == 2:
            print()
        elif opcion == 3:
            print()
        elif opcion == 4:
            break                

        ##lista_hoteles.actualizar_csv(archivo) #sobreescritura de csv de Hoteles                                                      
main()