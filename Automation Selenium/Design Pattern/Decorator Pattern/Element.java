package com.decoratorpattern.pom;

import org.openqa.selenium.WebElement;

/**
 * The Component Interface.
 * Defines the standard operations we want to perform on a web element.
 */
public interface Element {
    void click();
    void sendKeys(String text);
    String getText();
    
    // Required so decorators can access the raw Selenium element (e.g. for JavascriptExecutor)
    WebElement getWrappedElement();
}
