package org.jug.algeria.domain;

import lombok.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ApiKeysRequest {
	private String publicKey;
	private String privateKey;
	private String login;
}
