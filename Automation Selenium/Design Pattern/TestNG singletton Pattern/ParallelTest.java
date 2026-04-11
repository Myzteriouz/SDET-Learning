package com.framework.tests;

import org.testng.Assert;
import org.testng.annotations.Test;

public class ParallelTest extends BaseTest {

    /**
     * TestNG will assign this method to an available thread from the thread pool 
     * (e.g., Thread-10). It inherits the driver setup natively from BaseTest.
     */
    @Test
    public void testGoogleSearch() throws InterruptedException {
        long threadId = Thread.currentThread().getId();
        System.out.println("Executing testGoogleSearch on Thread: " + threadId);
        
        // The 'driver' here is specific to Thread-10. It will not interfere with BingSearch.
        driver.get("https://www.google.com");
        Assert.assertTrue(driver.getTitle().contains("Google"));
        
        Thread.sleep(2000); // Artificial delay to easily observe the browsers running side-by-side
    }

    /**
     * TestNG will simultaneously assign this method to another available thread 
     * (e.g., Thread-11). It gets its own completely isolated browser window.
     */
    @Test
    public void testBingSearch() throws InterruptedException {
        long threadId = Thread.currentThread().getId();
        System.out.println("Executing testBingSearch on Thread: " + threadId);
        
        driver.get("https://www.bing.com");
        Assert.assertTrue(driver.getTitle().contains("Bing"));
        
        Thread.sleep(2000); // Artificial delay to easily observe the browsers running side-by-side
    }
}