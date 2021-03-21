package org.jug.algeria.service;

import lombok.SneakyThrows;
import org.json.JSONObject;
import org.json.simple.parser.JSONParser;
import org.springframework.util.ResourceUtils;

import java.io.File;
import java.io.FileReader;

public class KeyService {
	@SneakyThrows
	private static org.json.simple.JSONObject getKeys() {
		JSONParser jsonParser = new JSONParser();

		File reader = ResourceUtils.getFile("classpath:keys.json");
		Object obj = jsonParser.parse(new FileReader(reader));
		return  (org.json.simple.JSONObject) obj;
	}
	@SneakyThrows
	public static String getPubKey() {
		return (String)getKeys().get("pub");
	}
	@SneakyThrows
	public static String getPrivKey() {
		return (String)getKeys().get("priv");
	}
}
