package com.framework.core;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

/**
 * Singleton class to manage WebDriver instances safely across multiple threads.
 */
public class WebDriverManager {

    /**
     * 1. The Singleton Instance
     * 'volatile' is critical here. It guarantees that if multiple threads try to initialize 
     * this Singleton at the exact same moment, any changes to the 'instance' variable are 
     * immediately visible to all other threads in main memory (bypassing CPU local caching).
     */
    private static volatile WebDriverManager instance;
    
    /**
     * 2. The ThreadLocal Container
     * This is the secret to parallel execution. ThreadLocal acts like a Map where the 
     * key is the Current Thread ID and the value is the WebDriver. 
     * Thread A gets Browser A. Thread B gets Browser B. They cannot overwrite each other.
     */
    private ThreadLocal<WebDriver> driver = new ThreadLocal<>();

    // Private constructor prevents any other class from doing 'new WebDriverManager()'
    private WebDriverManager() {}

    /**
     * 3. Global Access Point with Double-Checked Locking
     * 
     * @return The single, globally shared WebDriverManager instance.
     */
    public static WebDriverManager getInstance() {
        // First check: avoids the massive performance hit of 'synchronized' if the instance already exists.
        if (instance == null) {
            // Lock the class so only one thread can step inside this block at a time.
            synchronized (WebDriverManager.class) {
                // Second check: ensures a waiting thread doesn't re-initialize the instance
                // if the thread before it already did so while it was waiting for the lock.
                if (instance == null) {
                    instance = new WebDriverManager();
                }
            }
        }
        return instance;
    }

    /**
     * Retrieves the WebDriver for the SPECIFIC thread that calls this method.
     * If this thread doesn't have a browser yet, it opens one and stores it.
     */
    public WebDriver getDriver() {
        if (driver.get() == null) {
            // Initialize the browser and set it strictly for the current thread
            WebDriver webDriver = new ChromeDriver();
            webDriver.manage().window().maximize();
            driver.set(webDriver);
        }
        // Return the thread's isolated browser instance
        return driver.get();
    }

    /**
     * Safely closes the browser and prevents memory leaks in thread pools.
     */
    public void quitDriver() {
        if (driver.get() != null) {
            // Close the browser window
            driver.get().quit();
            // 4. Memory Management: Completely clear the ThreadLocal context for this thread.
            // Because CI/CD tools and TestNG reuse threads, failing to call this causes 
            // old, "dead" browser references to leak into future tests executed on this thread.
            driver.remove();
        }
    }
}