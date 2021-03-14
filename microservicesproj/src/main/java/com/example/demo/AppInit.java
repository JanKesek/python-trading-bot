package com.example.demo;

import com.example.demo.models.Product;
import com.example.demo.repositroy.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import java.util.ArrayList;
import java.util.List;

@Component
public class AppInit {
    @Autowired
    ProductRepository productRepository;
    @PostConstruct
    private void init() {
       // productRepository.deleteAll();
        List<Product> products = new ArrayList<>();
        Product product = new Product();
        product.setDescription("product nr 1");
        products.add(product);
        //productRepository.saveAll(products);
    }
}
