package com.framework.keyworddriven.engine;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * ActionKeywords Class
 * Contains atomic methods that represent every possible action a user can take on the UI.
 * These methods correspond directly to "Keywords" defined in an Excel sheet.
 */
public class ActionKeywords {
    
    private WebDriver driver;
    
    public ActionKeywords(WebDriver driver) {
        this.driver = driver;
    }

    // Keyword: openBrowser
    public void openBrowser(String browserType) {
        System.out.println("[Keyword] Opening browser: " + browserType);
        // driver = new ChromeDriver();
    }

    // Keyword: navigate
    public void navigate(String url) {
        System.out.println("[Keyword] Navigating to: " + url);
        // driver.get(url);
    }

    // Keyword: click
    public void click(String locatorType, String locatorValue) {
        System.out.println("[Keyword] Clicking element -> " + locatorType + "=" + locatorValue);
        // driver.findElement(getBy(locatorType, locatorValue)).click();
    }

    // Keyword: input
    public void input(String locatorType, String locatorValue, String testData) {
        System.out.println("[Keyword] Typing '" + testData + "' into -> " + locatorType + "=" + locatorValue);
        // driver.findElement(getBy(locatorType, locatorValue)).sendKeys(testData);
    }

    // Keyword: closeBrowser
    public void closeBrowser() {
        System.out.println("[Keyword] Closing browser.");
        // driver.quit();
    }
    
    // Helper to convert strings to Selenium By objects
    private By getBy(String type, String value) {
        if (type.equalsIgnoreCase("id")) return By.id(value);
        if (type.equalsIgnoreCase("xpath")) return By.xpath(value);
        return By.id(value);
    }
}
