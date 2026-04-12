package com.framework.api;

/**
 * POJO (Plain Old Java Object) representing a User Payload for API Testing.
 * Used for Serialization (Java -> JSON) and Deserialization (JSON -> Java).
 */
public class UserPayload {
    private String name;
    private String job;

    // Constructors, Getters, and Setters are standard.
    // Modern frameworks use Lombok (@Data) to auto-generate these at compile time.
    
    public UserPayload(String name, String job) {
        this.name = name;
        this.job = job;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getJob() { return job; }
    public void setJob(String job) { this.job = job; }
}
