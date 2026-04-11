package com.fluentpompattern.pom;

import org.openqa.selenium.WebDriver;

public class HomePage {
    private WebDriver driver;
    
    public HomePage(WebDriver driver) {
        this.driver = driver;
    }
    
    public HomePage verifyWelcomeMessage() {
        System.out.println("[HomePage] Asserting welcome message is displayed.");
        return this;
    }
    
    // Returns void because it's the end of the workflow, or could return LoginPage
    public void clickLogout() {
        System.out.println("[HomePage] Logging out.");
    }
}
