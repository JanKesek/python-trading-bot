package org.jug.algeria.service;


import lombok.SneakyThrows;
import org.jug.algeria.domain.ApiKeyPair;
import org.jug.algeria.domain.BuyRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Repository;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.Optional;
import java.util.UUID;

@Repository
public class HeaderService {
	private UUID uuid = UUID.randomUUID();

	@Autowired
	ApiHashGenerator apiHashGenerator;
	@Autowired
	KeyService keyService;

	String pubKey = KeyService.getPubKey();
	String privKey = KeyService.getPrivKey();

	@SneakyThrows
	public HttpHeaders getBitbayBuyHeader(BuyRequest request) {
		Optional<ApiKeyPair> apiKeyPairOptional = keyService.getKeyPairByExchangeId(1L);
		if(!apiKeyPairOptional.isPresent()) {
			throw new Exception("no key pair for exchange requested found");
		}
		String pubKey = apiKeyPairOptional.get().getPublicKey();
		String privKey = apiKeyPairOptional.get().getPrivateKey();
		String hashInput = apiHashGenerator.prepareData(request.toString(),pubKey,privKey);
		String apiHash = apiHashGenerator.hashWithSecretKey(hashInput,privKey);
		System.out.println("INPUT HASH: " + hashInput);
		System.out.println("API-HASH: " + apiHash);
		HttpHeaders httpHeaders = new HttpHeaders();
		httpHeaders.add("API-Key",pubKey);
		httpHeaders.add("API-Hash",apiHash);
				//apiHashGenerator.prepareData(request.toString(),pubKey,privKey)

		httpHeaders.add("operation-id",uuid.toString());
		httpHeaders.add("Request-Timestamp",apiHashGenerator.getTimeStamp());
		httpHeaders.add("Content-Type","application/json");
		return httpHeaders;
	}
}
