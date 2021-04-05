package org.jug.algeria.repository;

import org.jug.algeria.domain.ApiAccount;
import org.jug.algeria.domain.ApiKeyPair;
import org.jug.algeria.domain.Exchange;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.criteria.*;
import java.util.Optional;

public class ApiKeyPairRepositoryCustomImpl implements ApiKeyPairRepositoryCustom {
	@PersistenceContext
	EntityManager entityManager;

	@Override
	public Optional<ApiKeyPair> findApiKeyPairByExchangeId(long exchangeId) {
		CriteriaBuilder cb = entityManager.getCriteriaBuilder();
		CriteriaQuery cq = cb.createQuery(ApiKeyPair.class);
		Root<ApiKeyPair> apiKeyPairRoot = cq.from(ApiKeyPair.class);
		Join<ApiKeyPair, Exchange> exchangeJoin = apiKeyPairRoot.join("account", JoinType.LEFT)
			.join("exchange",JoinType.LEFT);
		cq.select(exchangeJoin).where(cb.equal(exchangeJoin.get("id"),exchangeId));
		return Optional.of((ApiKeyPair)entityManager.createQuery(cq).getSingleResult());
	}
}
