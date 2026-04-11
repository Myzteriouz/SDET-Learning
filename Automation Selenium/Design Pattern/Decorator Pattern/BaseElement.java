package com.decoratorpattern.pom;

import org.openqa.selenium.WebElement;

/**
 * Concrete Component.
 * The basic wrapper around Selenium's raw WebElement that actually performs the real actions.
 */
public class BaseElement implements Element {
    private WebElement webElement;
    
    public BaseElement(WebElement webElement) {
        this.webElement = webElement;
    }

    @Override
    public void click() { 
        webElement.click(); 
    }

    @Override
    public void sendKeys(String text) { 
        webElement.sendKeys(text); 
    }

    @Override
    public String getText() { 
        return webElement.getText(); 
    }
    
    @Override
    public WebElement getWrappedElement() { 
        return webElement; 
    }
}
