package br.com.ernanilima.producer;

import com.google.protobuf.InvalidProtocolBufferException;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import proto.DataInOuterClass;
import proto.DataOutOuterClass;

@SpringBootApplication
public class ProducerApplication implements ApplicationRunner {

    private final KafkaTemplate<String, byte[]> kafkaTemplate;

    public ProducerApplication(KafkaTemplate<String, byte[]> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public static void main(String[] args) {
        SpringApplication.run(ProducerApplication.class, args);
    }

    @Override
    public void run(ApplicationArguments args) {
        final var data = DataInOuterClass.DataIn.newBuilder()
                .setId("ID-Enviado")
                .setName1("Nome Enviado")
                .build();

        kafkaTemplate.send("TOPICO.IN", data.toByteArray());
    }

    @KafkaListener(topics = "TOPICO.OUT", groupId = "consumer-java-group")
    public void consumer(ConsumerRecord<String, byte[]> consumerRecord) throws InvalidProtocolBufferException {
        final var dataOut = DataOutOuterClass.DataOut.parseFrom(consumerRecord.value());
        System.out.printf("Recebido DataOut %s%n", dataOut);
    }

}
