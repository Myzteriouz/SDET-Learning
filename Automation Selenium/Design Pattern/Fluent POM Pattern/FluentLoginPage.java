package com.fluentpompattern.pom;

import org.openqa.selenium.WebDriver;

public class FluentLoginPage {
    private WebDriver driver;
    
    public FluentLoginPage(WebDriver driver) {
        this.driver = driver;
    }
    
    /**
     * INTRA-PAGE ACTION
     * By returning 'this', we can chain methods together in the test class.
     */
    public FluentLoginPage enterUsername(String user) {
        System.out.println("[LoginPage] Typing username: " + user);
        // driver.findElement(usernameLoc).sendKeys(user);
        return this;
    }
    
    /**
     * INTRA-PAGE ACTION
     */
    public FluentLoginPage enterPassword(String pass) {
        System.out.println("[LoginPage] Typing password: " + pass);
        // driver.findElement(passwordLoc).sendKeys(pass);
        return this;
    }
    
    /**
     * ADVANCED CONCEPT: Page Transitions (INTER-PAGE ACTION).
     * When an action causes the application to navigate to a new page,
     * the method returns an instance of the NEXT Page Object.
     */
    public HomePage clickLogin() {
        System.out.println("[LoginPage] Clicking login button. Transitioning to Home Page...");
        // driver.findElement(loginBtnLoc).click();
        return new HomePage(driver);
    }
}
