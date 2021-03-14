package com.example.demo.controller;

import com.example.demo.models.Product;
import com.example.demo.repositroy.ProductRepository;
import com.example.demo.repositroy.ProductRepositoryImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class ProductController {
    private final ProductRepository productRepository;

    @Autowired
    public ProductController(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    @GetMapping("/products")
    public List<Product> getAllProducts(){
        return (List<Product>)productRepository.findAll();
    }
}
