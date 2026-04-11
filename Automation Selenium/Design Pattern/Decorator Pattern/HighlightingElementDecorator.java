package com.decoratorpattern.pom;

import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

/**
 * Concrete Decorator.
 * Adds new behavior (Javascript Highlighting and Logging) BEFORE executing the standard actions.
 */
public class HighlightingElementDecorator extends ElementDecorator {
    private WebDriver driver;

    public HighlightingElementDecorator(Element customElement, WebDriver driver) {
        super(customElement); // Passes the element up to the base decorator
        this.driver = driver;
    }

    /**
     * ADVANCED CONCEPT: Dynamic Behavior Injection
     * This method adds a yellow background and red border to the element.
     * Extremely useful when recording automated tests for debugging or demo purposes.
     */
    private void highlight() {
        WebElement element = getWrappedElement();
        if (driver instanceof JavascriptExecutor) {
            JavascriptExecutor js = (JavascriptExecutor) driver;
            js.executeScript("arguments[0].setAttribute('style', 'border: 3px solid red; background: yellow;');", element);
            // Short sleep strictly to make the highlight visible to the human eye during a demo
            try { Thread.sleep(300); } catch (InterruptedException e) {} 
        }
    }

    @Override
    public void click() {
        System.out.println("LOG: [HighlightingElementDecorator] Highlighting element before click...");
        highlight(); // Inject new behavior
        super.click(); // Proceed with normal click
    }

    @Override
    public void sendKeys(String text) {
        System.out.println("LOG: [HighlightingElementDecorator] Highlighting element before typing: " + text);
        highlight(); // Inject new behavior
        super.sendKeys(text); // Proceed with normal typing
    }
}
