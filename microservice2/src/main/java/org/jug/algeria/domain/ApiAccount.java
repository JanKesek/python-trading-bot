package org.jug.algeria.domain;

import lombok.*;

import javax.persistence.*;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "api_account")
@Builder
@Data
@AllArgsConstructor
@NoArgsConstructor
public class ApiAccount {
	@Id
	@GeneratedValue(strategy = GenerationType.AUTO)
	@Column(name = "id")
	private Long id;

	@Column(name = "login")
	private String login;
	@Column(name = "password")
	private String password;


	@OneToMany(mappedBy = "account")
	private Set<ApiKeyPair> apiKeyPairSet = new HashSet<>();

	@OneToOne
	@JoinColumn(name = "id", referencedColumnName = "id")
	private Exchange exchange;

}
