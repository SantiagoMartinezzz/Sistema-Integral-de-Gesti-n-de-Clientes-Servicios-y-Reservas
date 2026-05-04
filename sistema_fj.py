# ================================
# SISTEMA SOFTWARE FJ
# Grupo: 213023_337
# Autor: Ivan Santiago Rojas Martinez
# ================================

from abc import ABC, abstractmethod

# ================================
# LOGS
# ================================
def registrar_log(mensaje):
    with open("logs.txt", "a") as f:
        f.write(mensaje + "\n")


# ================================
# EXCEPCIONES PERSONALIZADAS
# ================================
class ErrorSistema(Exception):
    pass


# ================================
# CLASE CLIENTE (ENCAPSULACIÓN)
# ================================
class Cliente:
    def __init__(self, nombre, email):
        if not nombre:
            raise ErrorSistema("Nombre inválido")

        if "@" not in email:
            raise ErrorSistema("Email inválido")

        self.__nombre = nombre
        self.__email = email

    def get_info(self):
        return f"{self.__nombre} - {self.__email}"


# ================================
# CLASE ABSTRACTA SERVICIO
# ================================
class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, duracion):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# ================================
# SERVICIOS (HERENCIA)
# ================================
class ReservaSala(Servicio):
    def calcular_costo(self, duracion):
        return self.precio_base * duracion

    def descripcion(self):
        return f"Sala: {self.nombre}"


class AlquilerEquipo(Servicio):
    def calcular_costo(self, duracion):
        return self.precio_base * duracion + 20  # recargo

    def descripcion(self):
        return f"Equipo: {self.nombre}"


class Asesoria(Servicio):
    def calcular_costo(self, duracion):
        return self.precio_base * duracion * 2  # más caro

    def descripcion(self):
        return f"Asesoría: {self.nombre}"


# ================================
# CLASE RESERVA
# ================================
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        try:
            if duracion <= 0:
                raise ErrorSistema("Duración inválida")

            self.cliente = cliente
            self.servicio = servicio
            self.duracion = duracion
            self.estado = "pendiente"

        except Exception as e:
            registrar_log(f"Error creando reserva: {e}")
            raise

    def procesar(self):
        try:
            costo = self.servicio.calcular_costo(self.duracion)
            self.estado = "confirmada"
            registrar_log(f"Reserva procesada: {self.servicio.nombre}")
            return costo

        except Exception as e:
            registrar_log(f"Error procesando reserva: {e}")
            return 0

    def mostrar(self):
        return f"Cliente: {self.cliente.get_info()} | {self.servicio.descripcion()} | Estado: {self.estado}"


# ================================
# SIMULACIÓN (OBLIGATORIO)
# ================================
if __name__ == "__main__":

    total_general = 0

    try:
        # Clientes válidos
        c1 = Cliente("Ivan", "ivan@gmail.com")

        # Cliente inválido (para log)
        try:
            c2 = Cliente("", "correo_mal")
        except Exception as e:
            registrar_log(f"Error cliente: {e}")

        # Servicios
        s1 = ReservaSala("Sala A", 50)
        s2 = AlquilerEquipo("Proyector", 30)
        s3 = Asesoria("Consultoría", 80)

        # Reservas válidas
        r1 = Reserva(c1, s1, 2)
        r2 = Reserva(c1, s2, 1)
        r3 = Reserva(c1, s3, 3)

        # Reserva inválida (para log)
        try:
            r4 = Reserva(c1, s1, -5)
        except Exception as e:
            registrar_log(f"Error reserva: {e}")

        reservas = [r1, r2, r3]

        for r in reservas:
            print(r.mostrar())
            total = r.procesar()
            print("Total:", total, "\n")
            total_general += total

        print("TOTAL GENERAL:", total_general)

    except Exception as e:
        registrar_log(f"Error general: {e}")
