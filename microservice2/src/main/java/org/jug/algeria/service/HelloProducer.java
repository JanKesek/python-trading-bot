package org.jug.algeria.service;

import org.apache.kafka.clients.KafkaClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Repository;
import org.springframework.stereotype.Service;

@Component
public class HelloProducer  {
	@Autowired
	private KafkaTemplate<String,String> kafkaTemplate;

	public void send(String msg) {
		System.out.println("Sending message "+msg);
		kafkaTemplate.send("testTopic",msg);
	}
}
