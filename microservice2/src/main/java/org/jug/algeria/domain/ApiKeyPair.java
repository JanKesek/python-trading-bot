package org.jug.algeria.domain;

import lombok.*;

import javax.persistence.*;

@Entity
@Builder
@Data
@Table(name = "api_key_pair")
@AllArgsConstructor
@NoArgsConstructor
public class ApiKeyPair {
	@Id
	@GeneratedValue(strategy = GenerationType.AUTO)
	@Column(name = "id")
	private Long id;
	//@Column(name = "api_account_id")
	//private Long apiAccountId;
	@Column(name = "public_key")
	private String publicKey;

	@Column(name = "private_key")
	private String privateKey;

	@Column(name="exchange_id")
	private Long exchangeId;

	@ManyToOne
	@JoinColumn(name = "apiKeyPairSet", referencedColumnName = "id")
	private ApiAccount account;
}
