package org.jug.algeria.service;

import lombok.Getter;
import lombok.SneakyThrows;
import org.jug.algeria.domain.ApiAccount;
import org.jug.algeria.domain.ApiKeyPair;
import org.jug.algeria.domain.ApiKeysRequest;
import org.jug.algeria.repository.ApiAccountRepository;
import org.jug.algeria.repository.ApiKeyPairRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Getter
@Repository
public class AccountService {
	private String timeStamp;
	@Autowired
	ApiAccountRepository apiAccountRepository;
	@Autowired
	ApiKeyPairRepository apiKeyPairRepository;

	public Optional<ApiAccount> getExchangeAccountByLogin(String login) {
		return apiAccountRepository.findApiAccountByLogin(login);
	}

	@SneakyThrows
	public void createNewApiKeysPair(ApiKeysRequest request, ApiAccount account) {
		Optional<ApiKeyPair> apiKeyPair = apiKeyPairRepository.findApiKeyPairByPrivateKey(request.getPrivateKey());
		if(apiKeyPair.isPresent()) {
			throw new Exception("This api key already exists");
		}
		ApiKeyPair newApiKeyPair = ApiKeyPair.builder()
			.privateKey(request.getPrivateKey())
			.publicKey(request.getPublicKey())
			.account(account)
			.build();
		apiKeyPairRepository.save(newApiKeyPair);
	}
	public Optional<ApiAccount> createNewApiAccount(String login) {
		ApiAccount account = ApiAccount.builder().login(login).build();
		account = apiAccountRepository.save(account);
		return Optional.of(account);
	}
}
