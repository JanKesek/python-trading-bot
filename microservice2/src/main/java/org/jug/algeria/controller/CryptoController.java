package org.jug.algeria.controller;

import org.json.JSONObject;
import org.jug.algeria.domain.AppUser;
import org.jug.algeria.domain.BuyRequest;
import org.jug.algeria.repository.UserRepository;
import org.jug.algeria.service.HeaderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.servlet.ModelAndView;

import javax.inject.Inject;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping(value = "/crypto", produces = MediaType.APPLICATION_JSON_VALUE)
public class CryptoController {

	UserRepository userRepository;
	@Autowired
	HeaderService headerService;
  	@Inject
  	public CryptoController(UserRepository userRepository) {
    	this.userRepository = userRepository;
  	}

  @PostMapping(value = "/buy/{market}", produces = MediaType.APPLICATION_JSON_VALUE)
  public ResponseEntity<String> buy(@RequestBody BuyRequest request, @PathVariable String market) {
  		System.out.println(request.getAmount());
    	System.out.println(request.getPrice());
   	 	RestTemplate restTemplate = new RestTemplate();
    	String url = String.format("https://api.bitbay.net/rest/trading/offer/%s", market);
// request body parameters
    	JSONObject body = request.toJson();
		HttpHeaders bitbayHeaders = headerService.getBitbayBuyHeader(request);
	    HttpEntity<String> httpRequest = new HttpEntity<String>(request.toString(),bitbayHeaders);
// send POST request
	    System.out.println(body.toString());
	    System.out.println(bitbayHeaders.toString());
	    System.out.println(url);
    	ResponseEntity<String> response = restTemplate.postForEntity(url,httpRequest, String.class);
    	System.out.println("ODPOWIEDZ: " + response.toString());
    	return response;
  }
}
