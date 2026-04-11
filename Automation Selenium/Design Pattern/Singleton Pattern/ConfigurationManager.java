package com.singletonpattern.framework;

import java.util.Properties;

/**
 * Singleton Pattern implementation for a Configuration/Properties Manager.
 * Ensures that configuration files (like config.properties) are only loaded ONCE
 * into memory during the entire test execution, saving I/O resources.
 */
public class ConfigurationManager {
    
    // 1. Static variable to hold the single instance
    private static ConfigurationManager instance;
    
    private Properties properties;

    // 2. Private constructor prevents instantiation from outside
    private ConfigurationManager() {
        properties = new Properties();
        // Mocking the loading of a file from disk
        System.out.println("LOG: [ConfigurationManager] Reading config.properties from disk... (This should ONLY happen once!)");
        properties.setProperty("browser", "chrome");
        properties.setProperty("timeout", "30");
        properties.setProperty("url", "https://example.com");
    }

    // 3. Public static method to get the instance
    // ADVANCED CONCEPT: Synchronized block for Thread Safety
    // If two parallel test threads call getInstance() at the exact same millisecond,
    // they might create two instances. Double-checked locking prevents this.
    public static ConfigurationManager getInstance() {
        if (instance == null) {
            synchronized (ConfigurationManager.class) {
                if (instance == null) {
                    instance = new ConfigurationManager();
                }
            }
        }
        return instance;
    }

    // Getter for properties
    public String getProperty(String key) {
        return properties.getProperty(key);
    }
}
