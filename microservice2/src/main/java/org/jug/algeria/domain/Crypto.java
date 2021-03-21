package org.jug.algeria.domain;

import lombok.Data;
import lombok.RequiredArgsConstructor;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import java.math.BigDecimal;


@Entity
@Data
@RequiredArgsConstructor
public class Crypto {
  @Id
  @GeneratedValue(strategy = GenerationType.AUTO)
  private Long id;
  private String symbol;
  private String fullName;
  private BigDecimal price;
}
