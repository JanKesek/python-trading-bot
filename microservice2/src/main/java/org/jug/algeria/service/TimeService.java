package org.jug.algeria.service;

import org.springframework.stereotype.Repository;

@Repository
public class TimeService {
	public String getTimestamp() {
		return String.valueOf(System.currentTimeMillis() / 1000L);
	}
}
