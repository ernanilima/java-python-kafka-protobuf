from kafka import KafkaConsumer, KafkaProducer
from proto.data_in_pb2 import DataIn
from proto.data_out_pb2 import DataOut
from proto.log_data_out_pb2 import LogDataOut

def create_consumer(bootstrap_servers, topic):
    return KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="consumer-python-group",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        key_deserializer=lambda k: k.decode("utf-8") if k else None,
        value_deserializer=lambda b: DataIn.FromString(b)
    )

def create_producer(bootstrap_servers):
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        key_serializer=lambda k: k.encode("utf-8") if k else None,
        value_serializer=lambda msg: msg.SerializeToString()
    )

def main():
    brokers = ["localhost:29092"]
    in_topic   = "TOPICO.IN"
    out_topic  = "TOPICO.OUT"
    log_topic  = "TOPICO.LOG"

    consumer = create_consumer(brokers, in_topic)
    producer = create_producer(brokers)

    print(f"Consumindo de {in_topic}, produzindo em {out_topic} e logs em {log_topic}…")

    try:
        for msg in consumer:

            # desserializa e processa
            data_in: DataIn = msg.value
            print(f"Recebido DataIn: id={data_in.id}, name1={data_in.name1}, name2={data_in.name2}")

            # montando resultado
            data_out = DataOut(id="ID-Retornado", name="Nome Retornado", status="Ok")

            # envia o resultado
            producer.send(out_topic, value=data_out)
            producer.flush()
            print(f"Enviado DataOut: id={data_out.id}, name={data_out.name}, status={data_out.status}")

            # montando log
            log = LogDataOut(status="Ok", totalTime="35s")

            # envia o log
            producer.send(log_topic, value=log)
            producer.flush()
            print(f"Enviado LogDataOut: status={log.status}, totalTime={log.totalTime}")

            print(f"Processo finalizado.")

    except KeyboardInterrupt:
        print("Interrompido pelo usuário")
    finally:
        consumer.close()
        producer.close()
        print("Aplicação encerrada.")

if __name__ == "__main__":
    main()