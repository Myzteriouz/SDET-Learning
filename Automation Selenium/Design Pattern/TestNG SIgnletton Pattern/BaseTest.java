package com.framework.tests;

import com.framework.core.WebDriverManager;
import org.openqa.selenium.WebDriver;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;

public class BaseTest {
    protected WebDriver driver;

    @BeforeMethod
    public void setUp() {
        // Fetches the isolated WebDriver for whatever thread TestNG assigns to this test
        driver = WebDriverManager.getInstance().getDriver();
    }

    @AfterMethod
    public void tearDown() {
        // Safely closes the browser and removes the ThreadLocal context
        WebDriverManager.getInstance().quitDriver();
    }
}