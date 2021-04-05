package org.jug.algeria.repository;

import org.jug.algeria.domain.ApiKeyPair;

import java.util.Optional;

public interface ApiKeyPairRepositoryCustom {
	Optional<ApiKeyPair> findApiKeyPairByExchangeId(long exchangeId);
}
