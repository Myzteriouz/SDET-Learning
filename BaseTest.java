package com.framework.tests;

import com.framework.core.WebDriverManager;
import org.openqa.selenium.WebDriver;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;

public class BaseTest {
    // This driver variable will hold the reference to the thread-specific WebDriver.
    // Since tests run in parallel, TestNG creates a separate instance of the test 
    // class for each thread, keeping this variable safe for parallel method execution.
    protected WebDriver driver;

    /**
     * @BeforeMethod is CRITICAL for parallel execution here.
     * If we used @BeforeClass, TestNG would only run this once for all tests in the class,
     * meaning all parallel threads would try to share the exact same browser instance.
     * 
     * By using @BeforeMethod, TestNG executes this block right before EVERY @Test method,
     * ensuring each thread explicitly requests its own unique WebDriver from our Singleton.
     */
    @BeforeMethod
    public void setUp() {
        // 1. TestNG spawns a thread for a @Test method (e.g., Thread 14).
        // 2. This thread calls WebDriverManager.getInstance().
        // 3. getDriver() checks if THIS specific thread already has a browser.
        // 4. If not, it creates a new ChromeDriver, stores it in ThreadLocal, and returns it.
        driver = WebDriverManager.getInstance().getDriver();
        System.out.println("Browser setup complete for Thread: " + Thread.currentThread().getId());
    }

    /**
     * @AfterMethod runs immediately after a @Test method completes, regardless of pass/fail.
     * This ensures that we don't leave zombie browsers open if an assertion fails.
     */
    @AfterMethod
    public void tearDown() {
        // 1. Quits the specific browser assigned to this exact thread.
        // 2. Calls driver.remove() on the ThreadLocal map inside the Singleton.
        // This prevents Memory Leaks because TestNG reuses threads (Thread Pool).
        // If we didn't remove it, the next test using this thread would find a "dead" browser.
        WebDriverManager.getInstance().quitDriver();
        System.out.println("Browser closed and cleaned up for Thread: " + Thread.currentThread().getId());
    }
}