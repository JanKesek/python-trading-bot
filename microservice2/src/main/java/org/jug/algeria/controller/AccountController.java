package org.jug.algeria.controller;

import org.jug.algeria.domain.ApiAccount;
import org.jug.algeria.domain.ApiKeysRequest;
import org.jug.algeria.service.AccountService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;

@RestController
@RequestMapping(value = "/account", produces = MediaType.APPLICATION_JSON_VALUE)
public class AccountController {
	@Autowired
	AccountService accountService;
	@PostMapping(value = "/register", produces = MediaType.APPLICATION_JSON_VALUE)
	public ResponseEntity<String> register(@RequestBody ApiKeysRequest request) {
		Optional<ApiAccount> apiAccount = accountService.getExchangeAccountByLogin(request.getLogin());
		if(!apiAccount.isPresent()) {
			apiAccount = accountService.createNewApiAccount(request.getLogin());
		}
		try {
			accountService.createNewApiKeysPair(request, apiAccount.get());
		} catch (Exception e) {
			return ResponseEntity.status(HttpStatus.CONFLICT).body("This api key already exists");
		}
		return ResponseEntity.ok().body("New Api key registered");
	}
}
