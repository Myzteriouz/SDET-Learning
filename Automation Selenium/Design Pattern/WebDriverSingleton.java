package automation.selenium;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

/**
 * This class demonstrates an Advanced Singleton Design Pattern tailored for 
 * Selenium WebDriver in real-world scenarios, particularly parallel execution.
 * 
 */
public class WebDriverSingleton {

    // 1. Thread-safe Singleton Instance using 'volatile'
    // 'volatile' ensures that multiple threads handle the 'instance' variable correctly 
    // when it is being initialized to the WebDriverSingleton instance, preventing caching issues.
    private static volatile WebDriverSingleton instance = null;

    // 2. ThreadLocal WebDriver for Parallel Execution
    // In real-world automation, we run tests in parallel to save execution time. 
    // If we use a standard global WebDriver, threads will overwrite each other's sessions.
    // ThreadLocal ensures that EVERY THREAD gets its OWN isolated instance of WebDriver.
    private ThreadLocal<WebDriver> driver = new ThreadLocal<>();

    private WebDriverSingleton() {
        // We no longer initialize the driver globally here, because initialization 
        // should happen per-thread, not once for the whole execution.
    }

    // 3. Double-Checked Locking for Thread-Safe Singleton Access
    public static WebDriverSingleton getInstance() {
        if (instance == null) {
            // Synchronized block ensures only one thread can execute this at a time
            // preventing a race condition where two threads might create two Singleton instances.
            synchronized (WebDriverSingleton.class) {
                // Double check if another thread hasn't already created the instance while we were waiting
                if (instance == null) {
                    instance = new WebDriverSingleton();
                }
            }
        }
        return instance;
    }

    /**
     * Retrieves the WebDriver for the current thread.
     * Initializes it if it doesn't exist for this specific thread.
     */
    public WebDriver getDriver() {
        if (driver.get() == null) {
            // In a real framework, you might pass browser type from a config file here.
            WebDriver webDriver = new ChromeDriver();
            webDriver.manage().window().maximize();
            // Store the initialized driver in the ThreadLocal variable
            driver.set(webDriver);
        }
        return driver.get();
    }

    /**
     * Safely quits the driver for the CURRENT THREAD and cleans up the ThreadLocal map.
     * This is typically called at the end of each test method (e.g., in @AfterMethod).
     */
    public void quitDriver() {
        if (driver.get() != null) {
            driver.get().quit();
            // 4. IMPORTANT: Remove the thread's copy to prevent memory leaks, 
            // especially when using Thread Pools (like in TestNG or CI servers).
            driver.remove();
        }
    }
}