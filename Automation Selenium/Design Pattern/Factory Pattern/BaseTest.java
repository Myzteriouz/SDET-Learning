package com.factorypattern.framework;

import org.openqa.selenium.WebDriver;
// Note: Requires TestNG library in pom.xml to run
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Parameters;

/**
 * Base test class that handles setup and teardown utilizing the Factory Pattern.
 * All test classes in the framework should inherit from this class.
 */
public class BaseTest {

    protected DriverManager driverManager;
    protected WebDriver driver;

    /**
     * Runs before every test method (e.g., @Test).
     * @param browserName Passed from the testng.xml file (e.g., <parameter name="browser" value="chrome"/>)
     */
    @BeforeMethod(alwaysRun = true) // alwaysRun ensures this executes even if specific test groups are called
    @Parameters("browser") 
    public void setup(String browserName) {
        
        // 1. Convert string to Enum for type safety
        BrowserType type = BrowserType.valueOf(browserName.toUpperCase());
        
        // 2. Factory Pattern Usage: The test asks the Factory for a manager, completely ignoring HOW it's built.
        driverManager = DriverManagerFactory.getManager(type);
        
        // 3. ThreadLocal Usage: Get the WebDriver instance (Thread-safe)
        driver = driverManager.getDriver();
        
        // Navigate to base URL
        driver.get("https://example.com");
    }

    /**
     * Runs after every test method, regardless of pass or fail.
     */
    @AfterMethod(alwaysRun = true)
    public void tearDown() {
        // Safely quit and clean up ThreadLocal memory
        if (driverManager != null) {
            driverManager.quitDriver();
        }
    }
}
