"""
Módulo di.py
Implementación del patrón Inyección de Dependencia.
Se utiliza inyección por constructor y también se muestra un ejemplo de inyección por setter.
Las dependencias están basadas en una interfaz, lo que permite intercambiarlas y usar mocks en pruebas.
"""

from abc import ABC, abstractmethod

# ------------------------------
# 1. Interfaz de la dependencia (contrato)
# ------------------------------
class Notificador(ABC):
    """Interfaz que define el comportamiento de un servicio de notificación."""
    @abstractmethod
    def enviar(self, destinatario: str, mensaje: str):
        pass

# ------------------------------
# 2. Implementaciones concretas (dependencias reales)
# ------------------------------
class EmailNotificador(Notificador):
    """Implementación que simula el envío de notificaciones por correo."""
    def enviar(self, destinatario: str, mensaje: str):
        print(f"[Email] Enviando a {destinatario}: {mensaje}")

class SMSNotificador(Notificador):
    """Implementación que simula el envío de notificaciones por SMS."""
    def enviar(self, destinatario: str, mensaje: str):
        print(f"[SMS] Enviando a {destinatario}: {mensaje}")

class PushNotificador(Notificador):
    """Otra implementación: notificación push."""
    def enviar(self, destinatario: str, mensaje: str):
        print(f"[Push] Enviando a {destinatario}: {mensaje}")

# ------------------------------
# 3. Clase que depende de la abstracción (cliente)
# ------------------------------
class ControladorUsuario:
    """
    Controlador que utiliza inyección por constructor para recibir su dependencia.
    Depende de la interfaz Notificador, no de implementaciones concretas.
    """
    def __init__(self, notificador: Notificador):
        self._notificador = notificador  # dependencia inyectada

    def notificar_activacion(self, usuario: str):
        mensaje = f"Bienvenido {usuario}, tu cuenta ha sido activada."
        self._notificador.enviar(usuario, mensaje)

# ------------------------------
# 4. Inyección por setter (opcional, para cumplir con otro tipo de inyección)
# ------------------------------
class GestorEventos:
    """
    Clase que permite cambiar la dependencia en tiempo de ejecución mediante setter injection.
    """
    def __init__(self):
        self._notificador: Notificador = None

    def set_notificador(self, notificador: Notificador):
        """Inyección por setter de la dependencia."""
        self._notificador = notificador

    def alertar(self, mensaje: str):
        if self._notificador is None:
            print("No hay notificador configurado.")
            return
        self._notificador.enviar("admin@sistema.com", mensaje)

# ------------------------------
# 5. Mock para pruebas (dependencia intercambiable)
# ------------------------------
class MockNotificador(Notificador):
    """
    Implementación mock que registra los mensajes en una lista para verificación en pruebas.
    Demuestra cómo las dependencias pueden ser mockeadas sin cambiar el código cliente.
    """
    def __init__(self):
        self.mensajes_enviados = []

    def enviar(self, destinatario: str, mensaje: str):
        self.mensajes_enviados.append((destinatario, mensaje))
        # En pruebas no se imprime, solo se almacena para aserciones.

# ------------------------------
# 6. Demostración del patrón
# ------------------------------
if __name__ == "__main__":
    print("=== Inyección por constructor ===")
    # Usando EmailNotificador
    email_notif = EmailNotificador()
    controlador_email = ControladorUsuario(email_notif)
    controlador_email.notificar_activacion("maria@example.com")

    # Cambiando fácilmente a SMSNotificador
    sms_notif = SMSNotificador()
    controlador_sms = ControladorUsuario(sms_notif)
    controlador_sms.notificar_activacion("+573001234567")

    print("\n=== Inyección por setter ===")
    gestor = GestorEventos()
    gestor.alertar("Sin notificador")  # no configurado
    gestor.set_notificador(PushNotificador())
    gestor.alertar("Servidor reiniciado correctamente.")

    print("\n=== Prueba con Mock ===")
    mock = MockNotificador()
    controlador_mock = ControladorUsuario(mock)
    controlador_mock.notificar_activacion("test@test.com")
    controlador_mock.notificar_activacion("otro@test.com")
    print(f"Mensajes almacenados por el mock: {mock.mensajes_enviados}")
    assert len(mock.mensajes_enviados) == 2
    print("Prueba pasada: el mock registró correctamente los mensajes.")