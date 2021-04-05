package org.jug.algeria.repository;

import org.jug.algeria.domain.ApiKeyPair;
import org.springframework.data.repository.CrudRepository;

import java.util.Optional;

public interface ApiKeyPairRepository extends CrudRepository<ApiKeyPair,Long>, ApiKeyPairRepositoryCustom {
	Optional<ApiKeyPair> findApiKeyPairByPrivateKey(String privateKey);
}
