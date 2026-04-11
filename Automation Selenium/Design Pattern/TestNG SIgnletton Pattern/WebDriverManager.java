package com.framework.core;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

/**
 * Singleton class to manage WebDriver instances safely across multiple threads.
 */
public class WebDriverManager {

    // Thread-safe singleton instance
    private static volatile WebDriverManager instance;
    
    // ThreadLocal completely isolates WebDriver instances per thread
    private ThreadLocal<WebDriver> driver = new ThreadLocal<>();

    private WebDriverManager() {}

    // Double-Checked Locking for getting the Singleton instance
    public static WebDriverManager getInstance() {
        if (instance == null) {
            synchronized (WebDriverManager.class) {
                if (instance == null) {
                    instance = new WebDriverManager();
                }
            }
        }
        return instance;
    }

    // Gets or initializes the driver for the CURRENT thread
    public WebDriver getDriver() {
        if (driver.get() == null) {
            WebDriver webDriver = new ChromeDriver();
            webDriver.manage().window().maximize();
            driver.set(webDriver);
        }
        return driver.get();
    }

    // Quits the driver and cleans up the thread memory
    public void quitDriver() {
        if (driver.get() != null) {
            driver.get().quit();
            driver.remove(); // CRITICAL for parallel execution memory management
        }
    }
}