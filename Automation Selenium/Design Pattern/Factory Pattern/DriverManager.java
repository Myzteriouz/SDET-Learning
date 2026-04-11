package com.factorypattern.framework;

import org.openqa.selenium.WebDriver;

/**
 * Abstract class defining the contract for browser initialization and teardown.
 * This is the 'Product' interface in the Factory Method pattern.
 */
public abstract class DriverManager {
    
    // ADVANCED CONCEPT: ThreadLocal
    // We wrap WebDriver in a ThreadLocal object to guarantee thread safety.
    // When running tests in parallel (e.g., via TestNG), each thread gets its own isolated instance of WebDriver.
    // Without this, concurrent tests would share a single browser instance, leading to flaky tests (race conditions).
    protected ThreadLocal<WebDriver> driver = new ThreadLocal<>();

    /**
     * Abstract method that concrete classes (like ChromeDriverManager) must implement 
     * to instantiate their specific driver.
     */
    protected abstract void createDriver();

    /**
     * Quits the driver and cleans up the ThreadLocal variable.
     * Crucial to prevent memory leaks in CI/CD environments.
     */
    public void quitDriver() {
        if (driver.get() != null) {
            driver.get().quit();
            driver.remove(); // Remove the value from the current thread to avoid memory leaks
        }
    }

    /**
     * Retrieves the WebDriver instance for the current thread.
     * If the thread doesn't have an instance yet, it calls createDriver() to instantiate one.
     */
    public WebDriver getDriver() {
        if (driver.get() == null) {
            createDriver();
        }
        return driver.get();
    }
}
