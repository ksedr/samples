package kamilsedrowicz.example.spring;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.util.HashMap;

@SpringBootApplication
public class AdApplication {

    static HashMap<Long, Ad> adsBoard;

    public static void main(String[] args) {
        adsBoard = new HashMap<>();

        SpringApplication.run(AdApplication.class, args);

        Ad ad = new Ad("java developer", "looking for java developer");
        adsBoard.put(ad.getId(), ad);
    }
}
