package org.jug.algeria.repository;

import org.jug.algeria.domain.ApiAccount;
import org.springframework.data.repository.CrudRepository;

import java.util.Optional;

public interface ApiAccountRepository extends CrudRepository<ApiAccount, Long> {
	Optional<ApiAccount> findApiAccountByLogin(String login);
}
