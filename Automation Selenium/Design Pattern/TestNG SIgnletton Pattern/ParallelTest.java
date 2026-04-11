package com.framework.tests;

import org.testng.Assert;
import org.testng.annotations.Test;

public class ParallelTest extends BaseTest {

    @Test
    public void testGoogleSearch() throws InterruptedException {
        System.out.println("Executing testGoogleSearch on Thread: " + Thread.currentThread().getId());
        driver.get("https://www.google.com");
        Assert.assertTrue(driver.getTitle().contains("Google"));
        Thread.sleep(2000); // Pause for visual observation
    }

    @Test
    public void testBingSearch() throws InterruptedException {
        System.out.println("Executing testBingSearch on Thread: " + Thread.currentThread().getId());
        driver.get("https://www.bing.com");
        Assert.assertTrue(driver.getTitle().contains("Bing"));
        Thread.sleep(2000); // Pause for visual observation
    }
}