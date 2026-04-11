package com.decoratorpattern.pom;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

public class DecoratorTest {
    private WebDriver driver;

    @BeforeMethod
    public void setup() {
        driver = new ChromeDriver();
        driver.get("https://example.com");
    }

    @Test
    public void testDecoratorPattern() {
        // 1. Find the raw Selenium WebElement (e.g., a link or button)
        WebElement rawElement = driver.findElement(By.tagName("a"));
        
        // 2. Wrap it in our standard Component (BaseElement)
        Element baseElement = new BaseElement(rawElement);
        
        // 3. Decorate it dynamically! We wrap the baseElement with our Highlighting Decorator.
        Element enhancedElement = new HighlightingElementDecorator(baseElement, driver);
        
        // Now, when we call actions, it will first highlight, then execute the action.
        System.out.println("Fetching text... (won't highlight)");
        String text = enhancedElement.getText(); 
        
        System.out.println("Clicking element... (WILL highlight)");
        enhancedElement.click(); 
        
        // Notice we didn't have to modify the Page Object or Selenium's core classes
        // to add this awesome visual capability!
    }

    @AfterMethod
    public void teardown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
