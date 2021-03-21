package org.jug.algeria.service;

import lombok.Getter;
import org.apache.commons.codec.digest.DigestUtils;
import org.apache.commons.codec.digest.HmacAlgorithms;
import org.apache.commons.codec.digest.HmacUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.text.SimpleDateFormat;
import java.util.Date;

@Getter
@Repository
public class ApiHashGenerator {
	private String timeStamp;
	@Autowired
	TimeService timeService;
	public String prepareData(String data, String pubKey, String privKey) {
		/*
		klucz_publiczny + aktualny_timestamp_unix + parametry_metody_JSON
		 */
		timeStamp = timeService.getTimestamp();
		if(data != null) {
			return pubKey + timeStamp + data;
		}
		else {
			return pubKey + timeStamp;
		}
	}
	public String generateSimple(String value) {
		System.out.println("DATA TO HASH: " + value);
		return new DigestUtils("SHA-512").digestAsHex(value);
	}
	public String hashWithSecretKey(String data, String key) {
		return new HmacUtils(HmacAlgorithms.HMAC_SHA_512, key).hmacHex(data);
	}
	public String generate(String data, String key) {

		String result = "";

		try{
			byte [] byteKey = key.getBytes("UTF-8");
			final String HMAC_SHA512 = "HmacSHA512";
			Mac sha512_HMAC = null;
			sha512_HMAC = Mac.getInstance(HMAC_SHA512);
			  SecretKeySpec keySpec = new SecretKeySpec(byteKey, HMAC_SHA512);

			sha512_HMAC.init(keySpec);
			byte [] mac_data = sha512_HMAC.
				doFinal(data.getBytes("UTF-8"));
			result = bytesToHex(mac_data);
		} catch (Exception e) {
			e.printStackTrace();
		}

		return result;
	}

	private static String bytesToHex(byte[] hashInBytes) {

		StringBuilder sb = new StringBuilder();

		for (byte b : hashInBytes) {
			sb.append(String.format("%02x", b));
		}

		return sb.toString();

	}
}
