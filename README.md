# Taller Semana 7 – Patrones Publish‑Subscribe e Inyección de Dependencia

**Gestores de Oportunidades**  
Universidad XYZ – 2026

## Descripción del proyecto

Este repositorio contiene la implementación práctica de dos patrones de diseño de software:

1. **Publish‑Subscribe** (`Mele`): Un bus de eventos que permite a publicadores enviar mensajes a tópicos y a suscriptores recibirlos, con suscripción/desuscripción dinámica.
2. **Inyección de Dependencia** (`Mele2`): Uso de constructor injection y setter injection para desacoplar componentes, con una interfaz que permite intercambiar implementaciones reales o mocks para pruebas.

Ambos ejemplos están escritos en Python 3 y no requieren librerías externas.

## Patrones implementados

- **Publish‑Subscribe**: Desacopla emisores (publishers) de receptores (subscribers) mediante un mediador (EventBus). Los suscriptores pueden agregarse o eliminarse en tiempo de ejecución.
- **Inyección de Dependencia**: Las clases dependen de abstracciones (interfaz `Notificador`) en lugar de implementaciones concretas. Se muestra inyección por constructor y por setter, facilitando el cambio de dependencias y la realización de pruebas unitarias con mocks.
  
##Salida esperada (ejemplo):

[EventBus] EmailSubscriber suscrito a 'noticias'
[EventBus] SMSSubscriber suscrito a 'noticias'
[EventBus] EmailSubscriber suscrito a 'clima'

--- Publicando noticia ---
[EmailSubscriber-principal] Recibido: Nueva ley de protección de datos aprobada. (enviando email...)
[SMSSubscriber-+573001234567] Recibido: Nueva ley de protección de datos aprobada. (enviando SMS...)

--- Publicando clima ---
[EmailSubscriber-secundario] Recibido: Pronóstico: soleado, 28°C. (enviando email...)

--- Desuscribiendo SMS de noticias ---
[EventBus] SMSSubscriber desuscrito de 'noticias'

--- Publicando otra noticia ---
[EmailSubscriber-principal] Recibido: Bolsa de valores cierra al alza. (enviando email...)x

##Salida esperada

=== Inyección por constructor ===
[Email] Enviando a maria@example.com: Bienvenido maria@example.com, tu cuenta ha sido activada.
[SMS] Enviando a +573001234567: Bienvenido +573001234567, tu cuenta ha sido activada.

=== Inyección por setter ===
No hay notificador configurado.
[Push] Enviando a admin@sistema.com: Servidor reiniciado correctamente.

=== Prueba con Mock ===
Mensajes almacenados por el mock: [('test@test.com', 'Bienvenido test@test.com, tu cuenta ha sido activada.'), ('otro@test.com', 'Bienvenido otro@test.com, tu cuenta ha sido activada.')]
Prueba pasada: el mock registró correctamente los mensajes

## Instrucciones para clonar y ejecutar

### Requisitos previos
- Tener instalado [Python 3.8+](https://www.python.org/downloads/)
- Git (para clonar)

### Clonación
```bash
git clone https://github.com/tu-usuario/semana7-patrones.git
cd semana7-patrones
