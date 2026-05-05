# 🛒 Market-Place-Inc TP2

## 📌 Descripción

Este proyecto consiste en la evolución de un sistema monolítico hacia una arquitectura distribuida basada en microservicios.

Se implementaron distintos servicios independientes que se comunican mediante:
- gRPC (comunicación síncrona)
- RabbitMQ (comunicación asíncrona)

Además, se utilizó Docker y Kubernetes para la contenedorización y orquestación del sistema.

---

## 🏗️ Arquitectura

El sistema está compuesto por los siguientes servicios:

- **orders-service** → gestión de pedidos
- **inventory-service** → control de stock
- **catalog-service** → catálogo de productos
- **notifications-service** → envío de notificaciones
- **RabbitMQ** → mensajería

### Flujo principal
Cliente → orders-service
orders-service → inventory-service (gRPC)
orders-service → RabbitMQ → notifications-service

---

## 🐳 Docker

Cada microservicio está contenido en su propio contenedor Docker.

Para levantar el sistema completo:

```bash
docker compose up --build


Conclusión

El sistema evolucionó de un monolito a una arquitectura distribuida, mejorando:

escalabilidad
tolerancia a fallos
desacoplamiento