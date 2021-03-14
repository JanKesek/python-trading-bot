package com.example.demo.models;

import lombok.*;

import javax.persistence.*;

@Data
@Entity
@Table(name = "product")
@Access(value = AccessType.PROPERTY)
public class Product {
    @Id
    public Long id;
    private String name;
    private String code;
    private String title;
    private String description;
    private String location;
    private Double price;
}
