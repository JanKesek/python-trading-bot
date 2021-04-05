package org.jug.algeria.domain;

import lombok.*;

import javax.persistence.*;
import java.math.BigDecimal;
import java.util.Set;


@Data
@Builder
@Entity
@Table(name = "exchange")
@AllArgsConstructor
@NoArgsConstructor
public class Exchange {
	@Id
	@GeneratedValue(strategy = GenerationType.AUTO)
	private Long id;
	private String exchangeName;
	@OneToMany
	@JoinColumn(name = "id", referencedColumnName = "id")
	private Set<Crypto> cryptoCurrencies;

}
