import json
import pika
import threading
import time
from fastapi import FastAPI

app = FastAPI(title="Notifications Service")

processed_orders = set()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "notifications"
    }


def consume_messages():
    while True:
        try:
            print("Intentando conectar con RabbitMQ...")

            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host="rabbitmq",
                    port=5672,
                    heartbeat=60
                )
            )

            channel = connection.channel()
            channel.queue_declare(queue="order_created", durable=True)

            def callback(ch, method, properties, body):
                data = json.loads(body)
                order_id = data.get("order_id")

                if order_id in processed_orders:
                    print(f"Mensaje duplicado ignorado: {order_id}")
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    return

                processed_orders.add(order_id)

                print(f"Notificación enviada para el pedido: {data}")

                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_qos(prefetch_count=1)

            channel.basic_consume(
                queue="order_created",
                on_message_callback=callback,
                auto_ack=False
            )

            print("Notifications service conectado a RabbitMQ y esperando mensajes...")
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ no está listo. Reintentando en 5 segundos...")
            time.sleep(5)

        except Exception as e:
            print(f"Error en notifications-service: {e}")
            time.sleep(5)


@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=consume_messages, daemon=True)
    thread.start()