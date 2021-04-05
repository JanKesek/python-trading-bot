package org.jug.algeria.service;

import lombok.SneakyThrows;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.jug.algeria.domain.ApiKeyPair;
import org.jug.algeria.repository.ApiKeyPairRepository;
import org.jug.algeria.repository.ApiKeyPairRepositoryCustom;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.ResourceUtils;

import java.io.File;
import java.io.FileReader;
import java.security.KeyPair;
import java.util.Optional;

@Service
public class KeyService {
	@Autowired
	ApiKeyPairRepositoryCustom apiKeyPairRepository;

	@SneakyThrows
	private static org.json.simple.JSONObject getKeys() {
		JSONParser jsonParser = new JSONParser();

		//File reader = ResourceUtils.getFile("classpath:keys.json");
		//Object obj = jsonParser.parse(new FileReader(reader));
		return new JSONObject();
		//return  (org.json.simple.JSONObject) obj;
	}
	@SneakyThrows
	public static String getPubKey() {
		//return (String)getKeys().get("pub");
		return "testpubkey";
	}
	@SneakyThrows
	public static String getPrivKey() {
		return "testprivkey";
		//return (String)getKeys().get("priv");
	}
	@SneakyThrows
	public Optional<ApiKeyPair> getKeyPairByExchangeId(long exchangeId) {
		return apiKeyPairRepository.findApiKeyPairByExchangeId(exchangeId);
	}
}
