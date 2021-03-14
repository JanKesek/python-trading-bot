package com.example.demo.models;

import lombok.*;
import org.springframework.data.annotation.Id;

@Data
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProductCategory {
    @Id
    private String id;
    private String name;
    private String title;
    private String description;
    private String imgUrl;
}
