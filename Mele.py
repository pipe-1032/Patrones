"""
Módulo pubsub.py
Implementación del patrón Publish-Subscribe usando un bus de eventos centralizado.
Permite suscribir y desuscribir suscriptores dinámicamente.
"""

from abc import ABC, abstractmethod
from typing import List, Callable

# ------------------------------
# 1. Interfaz del Suscriptor (opcional para tipado)
# ------------------------------
class Subscriber(ABC):
    """Interfaz que deben implementar todos los suscriptores."""
    @abstractmethod
    def update(self, mensaje: str):
        pass

# ------------------------------
# 2. Implementaciones concretas de suscriptores
# ------------------------------
class EmailSubscriber(Subscriber):
    """Suscriptor que simula el envío de un correo electrónico."""
    def __init__(self, nombre: str):
        self.nombre = nombre

    def update(self, mensaje: str):
        print(f"[EmailSubscriber-{self.nombre}] Recibido: {mensaje} (enviando email...)")

class SMSSubscriber(Subscriber):
    """Suscriptor que simula el envío de un SMS."""
    def __init__(self, numero: str):
        self.numero = numero

    def update(self, mensaje: str):
        print(f"[SMSSubscriber-{self.numero}] Recibido: {mensaje} (enviando SMS...)")

# ------------------------------
# 3. Publicador base
# ------------------------------
class Publisher:
    """Clase base para los publicadores. Cada publicador publica en un tópico específico."""
    def __init__(self, bus: 'EventBus', topico: str):
        self.bus = bus
        self.topico = topico

    def publish(self, mensaje: str):
        """Publica un mensaje en el tópico asociado."""
        self.bus.notify(self.topico, mensaje)

# ------------------------------
# 4. Publicadores concretos (al menos dos)
# ------------------------------
class NewsPublisher(Publisher):
    """Publicador de noticias (tópico 'noticias')."""
    def __init__(self, bus: 'EventBus'):
        super().__init__(bus, "noticias")

class WeatherPublisher(Publisher):
    """Publicador de clima (tópico 'clima')."""
    def __init__(self, bus: 'EventBus'):
        super().__init__(bus, "clima")

# ------------------------------
# 5. Bus de eventos (mediador)
# ------------------------------
class EventBus:
    """
    Bus de eventos que gestiona las suscripciones y la entrega de mensajes.
    Permite suscribir y desuscribir suscriptores a un tópico de forma dinámica.
    """
    def __init__(self):
        # Diccionario: clave = tópico, valor = lista de suscriptores (funciones de callback)
        self._subscriptions: dict[str, List[Callable[[str], None]]] = {}

    def subscribe(self, topico: str, subscriber: Subscriber):
        """
        Suscribe un suscriptor a un tópico.
        Si el tópico no existe, se crea la lista.
        """
        if topico not in self._subscriptions:
            self._subscriptions[topico] = []
        self._subscriptions[topico].append(subscriber.update)
        print(f"[EventBus] {subscriber.__class__.__name__} suscrito a '{topico}'")

    def unsubscribe(self, topico: str, subscriber: Subscriber):
        """
        Desuscribe un suscriptor de un tópico.
        Si después de eliminar no quedan suscriptores, se elimina el tópico.
        """
        if topico in self._subscriptions:
            self._subscriptions[topico].remove(subscriber.update)
            if not self._subscriptions[topico]:
                del self._subscriptions[topico]
            print(f"[EventBus] {subscriber.__class__.__name__} desuscrito de '{topico}'")

    def notify(self, topico: str, mensaje: str):
        """
        Notifica a todos los suscriptores de un tópico.
        Si no hay suscriptores, simplemente no hace nada.
        """
        if topico in self._subscriptions:
            for callback in self._subscriptions[topico]:
                callback(mensaje)

# ------------------------------
# 6. Demostración del patrón
# ------------------------------
if __name__ == "__main__":
    # Crear el bus
    bus = EventBus()

    # Crear publicadores (dos)
    news_pub = NewsPublisher(bus)
    weather_pub = WeatherPublisher(bus)

    # Crear suscriptores (dos)
    email_sub = EmailSubscriber("principal")
    sms_sub = SMSSubscriber("+573001234567")
    email_sub2 = EmailSubscriber("secundario")

    # Suscripciones dinámicas
    bus.subscribe("noticias", email_sub)
    bus.subscribe("noticias", sms_sub)
    bus.subscribe("clima", email_sub2)

    # Publicar mensajes
    print("\n--- Publicando noticia ---")
    news_pub.publish("Nueva ley de protección de datos aprobada.")

    print("\n--- Publicando clima ---")
    weather_pub.publish("Pronóstico: soleado, 28°C.")

    # Desuscribir un suscriptor y volver a publicar
    print("\n--- Desuscribiendo SMS de noticias ---")
    bus.unsubscribe("noticias", sms_sub)

    print("\n--- Publicando otra noticia ---")
    news_pub.publish("Bolsa de valores cierra al alza.")