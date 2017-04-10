package kamilsedrowicz.example.spring;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import java.util.Date;

/**
 * Represents a job offer.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public class Ad {
    private long id;
    private String title;
    private String description;

    public Ad() {
    }

    public Ad(String title, String description) {
        this.id = (new Date()).getTime();
        this.title = title;
        this.description = description;
    }

    public long getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    @Override
    public String toString() {
        return "Ad{" +
                "id=" + id +
                ", title='" + title + '\'' +
                ", description='" + description + '\'' +
                '}';
    }
}