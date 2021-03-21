package org.jug.algeria.domain;

import lombok.*;
import org.json.JSONObject;

import java.math.BigDecimal;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class BuyRequest {
  private BigDecimal amount;
  private BigDecimal price;
  private String offerType;
  private BigDecimal rate;
  private Boolean postOnly;
  private String mode;
  private Boolean fillOrKill;

  public Map<String, String> toMap() {
    Map<String,String> jsonMap = new HashMap<>();
    jsonMap.put("amount",amount.toString());
    jsonMap.put("price",price.toString());
    jsonMap.put("offerType",offerType);
    if(rate != null) {
      jsonMap.put("rate", rate.toString());
    }
    jsonMap.put("postOnly",postOnly.toString());
    jsonMap.put("mode",mode);
    jsonMap.put("fillOrKill",fillOrKill.toString());
    return jsonMap;
  }
  public JSONObject toJson() {
    JSONObject jsonObject = new JSONObject();
    jsonObject.put("amount",amount);
    jsonObject.put("price",price);
    jsonObject.put("offerType",offerType);
    jsonObject.put("rate", rate);
    jsonObject.put("postOnly", postOnly.equals(Boolean.TRUE));
    jsonObject.put("mode",mode);
    jsonObject.put("fillOrKill",fillOrKill.equals(Boolean.TRUE));
    return jsonObject;
  }

  @Override
  public String toString() {
    return String.format("{\"amount\":%s," +
          "\"price\":%s," +
            "\"offerType\":\"%s\","+
            "\"rate\":%s," +
            "\"postOnly\":%s,"+
            "\"mode\":\"%s\"," +
            "\"fillOrKill\":%s}",
            amount.toString(),price.toString(), offerType, rate != null ? rate.toString() : null,
            postOnly.toString(),mode,fillOrKill.toString());
  }
}
