# Proyecto-Gestion-Hoteleria-2
<a href = "https://github.com/erjeank25/Proyecto-Gestion-Hoteleria-2/blob/main/2do%20Proyecto%20Algoritmos%202.py">4ta Evaluación de Algoritmos y Estructuras II.</a>

<h2>¿En qué consiste?</h2>
Esta evaluacion consiste en un sistema avanzado de Gestión de reservaciones. El sistema permitirá a un hotel o servicio similar gestionar las reservaciones de manera
eficiente, organizarlas según múltiples criterios y generar informes detallados.

Este programa contendrá los siguientes modulos:

<h2>Gestion de Hoteles</h2>

Este módulo se encargará de gestionar(crear, modificar, listar, eliminar) la información y la configuración de los hoteles que forman parte de la cadena. Se utilizó una lista enlazada para mantener un registro de todos los hoteles disponibles. Y guarda detalles importantes como el nombre del hotel, la dirección, el número de teléfono, habitaciones disponibles(crear modificar listar y consultar) y sus respectivas reservaciones.

<h2>Gestion de Reservaciones</h2>

Se utilizó una cola para llevar un registro de todas las reservaciones realizadas en cada hotel de la cadena. Cada nodo representa una reserva y contendrá información detallada sobre la reserva. La reserva tendrá detalles como el nombre de la persona que hizo la reservacion, fecha de la reserva, fecha de entrada, fecha de salida, etc.Los usuarios podrán agregar nuevas reservaciones, eliminarlas, listar por hotel o buscar reservaciones existentes en el registro.

<h2>Modulo de historial y accion de errores</h2>

Este módulo utiliza una pila para registrar las acciones realizadas en el sistema por parte de los usuarios y los errores. Cada vez que se realiza una acción importante, como agregar un hotel, eliminar una reserva, actualizar información de cliente, etc., se registra en la pila. Cada registro contiene información relevante, como el tipo de registro, es decir si fue una accion común o un error, una ligera descripción sobre el registro, la fecha y la hora en que ocurrió el registro.(Este historial se guarda en un <a href = "https://github.com/erjeank25/Proyecto-Gestion-Hoteleria-2/blob/main/log_registros.csv">archivo</a>) <br>

<h3>Las acciones de cada uno de los modulos, se guardarán en sus archivos respectivos, para mas detalles: <a href = "https://github.com/erjeank25/Proyecto-Gestion-Hoteleria-2">Ver repositorio</a></h3>

