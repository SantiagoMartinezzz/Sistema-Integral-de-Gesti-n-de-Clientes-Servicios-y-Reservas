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

class ErrorValidacion(ErrorSistema):
    pass

class ErrorReserva(ErrorSistema):
    pass


# ================================
# CLASE ABSTRACTA BASE
# ================================
class Entidad(ABC):
    @abstractmethod
    def descripcion(self):
        pass


# ================================
# CLIENTE
# ================================
class Cliente(Entidad):
    def __init__(self, nombre, correo):
        try:
            if not nombre:
                raise ErrorValidacion("Nombre vacío")
            if "@" not in correo:
                raise ErrorValidacion("Correo inválido")

            self.__nombre = nombre
            self.__correo = correo

        except Exception as e:
            registrar_log(f"Error creando cliente: {e}")
            raise

    def descripcion(self):
        return f"Cliente: {self.__nombre} - {self.__correo}"


# ================================
# SERVICIO ABSTRACTO
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
# SERVICIOS HIJOS
# ================================
class ServicioSala(Servicio):
    def calcular_costo(self, duracion):
        return self.precio_base * duracion

    def descripcion(self):
        return f"Sala: {self.nombre}"


class ServicioEquipo(Servicio):
    def calcular_costo(self, duracion):
        return (self.precio_base * duracion) + 10  # costo adicional

    def descripcion(self):
        return f"Equipo: {self.nombre}"


class ServicioAsesoria(Servicio):
    def calcular_costo(self, duracion):
        return self.precio_base * duracion * 1.2  # recargo

    def descripcion(self):
        return f"Asesoría: {self.nombre}"


# ================================
# RESERVA
# ================================
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        try:
            if duracion <= 0:
                raise ErrorReserva("Duración inválida")

            self.cliente = cliente
            self.servicio = servicio
            self.duracion = duracion
            self.estado = "pendiente"

        except Exception as e:
            registrar_log(f"Error creando reserva: {e}")
            raise

    def confirmar(self):
        try:
            self.estado = "confirmada"
        except Exception as e:
            registrar_log(f"Error confirmando reserva: {e}")

    def cancelar(self):
        try:
            self.estado = "cancelada"
        except Exception as e:
            registrar_log(f"Error cancelando reserva: {e}")

    def calcular_total(self):
        try:
            return self.servicio.calcular_costo(self.duracion)
        except Exception as e:
            registrar_log(f"Error cálculo total: {e}")
            return 0

    def descripcion(self):
        return f"{self.cliente.descripcion()} | {self.servicio.descripcion()} | Estado: {self.estado}"


# ================================
# SIMULACIÓN (10 OPERACIONES)
# ================================
if __name__ == "__main__":

    print("=== SISTEMA SOFTWARE FJ ===\n")

    # Lista de operaciones
    reservas = []

    try:
        # 1 válido
        c1 = Cliente("Ivan", "ivan@gmail.com")
        s1 = ServicioSala("Sala A", 50)
        r1 = Reserva(c1, s1, 2)
        r1.confirmar()
        reservas.append(r1)

        # 2 válido
        s2 = ServicioEquipo("Proyector", 30)
        r2 = Reserva(c1, s2, 3)
        r2.confirmar()
        reservas.append(r2)

        # 3 válido
        s3 = ServicioAsesoria("Consultoría", 100)
        r3 = Reserva(c1, s3, 1)
        reservas.append(r3)

        # 4 error cliente
        try:
            c2 = Cliente("", "correo")
        except Exception:
            pass

        # 5 error reserva
        try:
            r4 = Reserva(c1, s1, -5)
        except Exception:
            pass

        # 6 válido
        r5 = Reserva(c1, s1, 5)
        reservas.append(r5)

        # 7 válido
        r6 = Reserva(c1, s2, 2)
        reservas.append(r6)

        # 8 error servicio
        try:
            s4 = ServicioSala("Sala B", None)
        except Exception as e:
            registrar_log(f"Error servicio: {e}")

        # 9 válido
        r7 = Reserva(c1, s3, 4)
        reservas.append(r7)

        # 10 válido
        r8 = Reserva(c1, s1, 1)
        reservas.append(r8)

    except Exception as e:
        registrar_log(f"Error general: {e}")

    finally:
        print("Sistema ejecutado con control de errores.\n")

    # Mostrar resultados
    total_general = 0

    for r in reservas:
        print(r.descripcion())
        total = r.calcular_total()
        print(f"Total: {total}\n")
        total_general += total

    print("TOTAL GENERAL:", total_general)
