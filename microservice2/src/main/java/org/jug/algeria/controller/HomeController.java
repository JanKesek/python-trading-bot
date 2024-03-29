package org.jug.algeria.controller;

import org.jug.algeria.domain.AppUser;
import org.jug.algeria.repository.UserRepository;
import org.jug.algeria.service.HelloProducer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;

import javax.inject.Inject;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

@RestController
@RequestMapping(value = "/", produces = MediaType.APPLICATION_JSON_VALUE)
public class HomeController {

  private final UserRepository userRepository;
  private final HelloProducer helloProducer;
  @Inject
  public HomeController(UserRepository userRepository, HelloProducer helloProducer) {
    this.userRepository = userRepository;
    this.helloProducer = helloProducer;
  }

  @GetMapping
  public ModelAndView home() {
    return new ModelAndView("index");
  }

  @GetMapping(value = "/hello")
  public ResponseEntity<String> sayHello() {
    return ResponseEntity.ok().body("Hello there !");
  }
  @GetMapping(value = "/hellokafka/{msg}")
  public ResponseEntity<String> helloKafka(@PathVariable String msg) {
    helloProducer.send(msg);
    return ResponseEntity.ok().body("Hello from kafka!");
  }

  @PostMapping(value = "/user/{username}", produces = MediaType.APPLICATION_JSON_VALUE)
  public ResponseEntity<AppUser> create(@PathVariable String username) {
    AppUser appUser = new AppUser();
    appUser.setUsername(username);
    AppUser saved = userRepository.save(appUser);
    return ResponseEntity.ok().body(saved);
  }

  @GetMapping(value = "/user", produces = MediaType.APPLICATION_JSON_VALUE)
  public ResponseEntity<List<AppUser>> findAll() {
    final List<AppUser> resultList = new ArrayList<>();
    final Iterable<AppUser> all = userRepository.findAll();
    all.forEach(resultList::add);
    return ResponseEntity.ok().body(resultList);
  }

}
