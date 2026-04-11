package com.decoratorpattern.pom;

import org.openqa.selenium.WebElement;

/**
 * The Base Decorator.
 * It implements the Element interface and holds a reference to an underlying Element object.
 * By default, it just passes all method calls down to the wrapped element.
 */
public abstract class ElementDecorator implements Element {
    protected Element customElement;

    public ElementDecorator(Element customElement) {
        this.customElement = customElement;
    }

    @Override
    public void click() { 
        customElement.click(); 
    }

    @Override
    public void sendKeys(String text) { 
        customElement.sendKeys(text); 
    }

    @Override
    public String getText() { 
        return customElement.getText(); 
    }
    
    @Override
    public WebElement getWrappedElement() { 
        return customElement.getWrappedElement(); 
    }
}
