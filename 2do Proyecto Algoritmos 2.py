import csv

class Hotel:
    def __init__(self, nombre, direccion, telefono, habitaciones_disponibles, nro_reservas):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.habitaciones_disponibles = habitaciones_disponibles
        self.nro_reservas = nro_reservas

    def incremento_reservas(self):
        self.nro_reservas += 1    
        
class NodoHotel:
    #Nodos para hoteles a crear
    def __init__(self, hotel):
        self.hotel = hotel #hoteles a modificar
        self.siguiente = None #atributo publico para usarlo como nodo siguiente

class ListaHoteles:
    #Opciones de hoteles
    def __init__(self):
        self.inicio = None

    def cargar_csv(self, archivo):
        with open(archivo, 'r') as archivo_csv:
            lector = csv.reader(archivo_csv, delimiter=';')
            next(lector)

            for fila in lector:
                nombre, direccion, telefono, habitaciones_disponibles, nro_reservas = fila
                habitaciones_disponibles = int(habitaciones_disponibles) #parseo a entero
                nro_reservas = int(nro_reservas) #parseo a entero
                self.agregar(nombre, direccion, telefono, habitaciones_disponibles, nro_reservas)

    def agregar(self, nombre, direccion, telefono, habitaciones_disponibles, nro_reservas):
        nuevo_hotel = Hotel(nombre, direccion, telefono, habitaciones_disponibles, nro_reservas)
        
        nuevo_nodo = NodoHotel(nuevo_hotel)        

        if not self.inicio:
            self.inicio = nuevo_nodo
        else:
            nodo_actual = self.inicio
            while nodo_actual.siguiente:
                nodo_actual = nodo_actual.siguiente
            nodo_actual.siguiente = nuevo_nodo

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

    def eliminar(self, nombre):
        if not self.inicio:
            return

        if self.inicio.hotel.nombre == nombre:
            self.inicio = self.inicio.siguiente
            return

        nodo_anterior = self.inicio
        nodo_actual = self.inicio.siguiente
        while nodo_actual:
            if nodo_actual.hotel.nombre == nombre:
                nodo_anterior.siguiente = nodo_actual.siguiente
                return
            nodo_anterior = nodo_actual
            nodo_actual = nodo_actual.siguiente       

def main():

    archivo = 'hoteles.csv'
    lista_hoteles = ListaHoteles() #instanciacion de un objeto de ListaHoteles()
    lista_hoteles.cargar_csv(archivo) #lectura del archivo.csv

    opcion = 0
    opcion_2 = 0

    while True:
        print("****** BIENVENIDO AL SISTEMA DE GESTION DE HOTELERIA ******")
        print("Seleccione una opcion")
        print("1. Gestion de Hoteles")
        print("2. Gestion de Reservaciones")
        print("3. Modulo de Historial de Acciones")
        print("4. Salir")
        opcion = int(input())

        if opcion == 1:
            while True:
                print("Seleccione una opcion:")
                print("1. Crear otro hotel")
                print("2. Modificar hotel")
                print("3. Listar hoteles")
                print("4. Eliminar Hotel")
                opcion_2 = int(input())
                
                if opcion_2 == 1:
                    print("Selecciono: Crear otro hotel")
                    nombre = input("Introduzca el nombre del hotel: ")
                    direccion = input("Introduzca la direccion del hotel: ")
                    telefono = input("Introduzca el numero telefonico: ")
                    habitaciones_disponibles = int(input("Introduzca el numero de habitaciones: "))
                    nro_reservas = int(input("Introduzca el numero de reservas: "))
                    lista_hoteles.agregar(nombre, direccion, telefono, habitaciones_disponibles, nro_reservas)
                
                elif opcion_2 == 2:
                    print("Selecciono: Modificar hotel")
                    print("\nLista de Hoteles: ")
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
                elif opcion_2 == 3:
                    print("Selecciono: Listar hoteles\n")
                    lista_hoteles.listar()
                    
                elif opcion_2 == 4:
                    print("Selecciono: Eliminar hoteles")
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
                        print("No existe")                                        



                
main()    
