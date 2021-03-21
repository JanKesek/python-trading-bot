package service;

import org.jug.algeria.domain.BuyRequest;
import org.jug.algeria.service.ApiHashGenerator;
import org.jug.algeria.service.KeyService;
import org.jug.algeria.service.TimeService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.math.BigDecimal;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.when;

public class ApiHashGeneratorTest {
	String pubKey = KeyService.getPubKey();
	String privKey = KeyService.getPrivKey();

	@Mock
	TimeService timeService;
	@InjectMocks
	ApiHashGenerator apiHashGenerator;

	@BeforeEach
	void initialize() {
		MockitoAnnotations.initMocks(this);
	}

	@Test
	void generateHMACKeyed() {
		String data=null;
		when(timeService.getTimestamp()).thenReturn("1616269998238");
		String input = apiHashGenerator.prepareData(data,pubKey,privKey);
		assertEquals("",input);
		String apiHash = apiHashGenerator.hashWithSecretKey(input,privKey);
		assertEquals(
			"",
			                  apiHash);
	}
	@Test
	void generateKeyedWithPayload() {
		BuyRequest buyRequest = BuyRequest.builder()
			.amount(BigDecimal.ONE)
			.price(BigDecimal.valueOf(50))
			.offerType("BUY")
			.rate(null)
			.postOnly(true)
			.mode("market")
			.fillOrKill(false).build();
		when(timeService.getTimestamp()).thenReturn("1616270681124");
		String input = apiHashGenerator.prepareData(buyRequest.toString(),pubKey,privKey);
		assertEquals("",input);
		String apiHash = apiHashGenerator.hashWithSecretKey(input,privKey);
		assertEquals(""
			,apiHash);
	}
}
