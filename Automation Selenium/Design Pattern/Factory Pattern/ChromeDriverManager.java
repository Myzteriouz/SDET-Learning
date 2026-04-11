package com.factorypattern.framework;

import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

/**
 * Concrete Product implementation for Chrome.
 * Extends the abstract DriverManager and provides the specific logic needed to launch Google Chrome.
 */
public class ChromeDriverManager extends DriverManager {

    @Override
    protected void createDriver() {
        // ADVANCED CONCEPT: Browser Options & Desired Capabilities
        // Instead of just launching a raw driver, we use ChromeOptions to configure the execution environment.
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--start-maximized");          // Maximize window
        options.addArguments("--disable-notifications");    // Block push notifications
        options.addArguments("--disable-infobars");         // Disable "Chrome is being controlled by automated software"
        
        // Note: Selenium 4.6+ comes with Selenium Manager, so we no longer strictly need WebDriverManager.
        // It will automatically download the correct chromedriver.exe for the installed browser version.
        
        // Set the instantiated driver into the ThreadLocal variable inherited from the abstract parent class.
        driver.set(new ChromeDriver(options));
    }
}
