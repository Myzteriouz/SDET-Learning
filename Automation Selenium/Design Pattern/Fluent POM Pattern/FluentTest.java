package com.fluentpompattern.pom;

import org.openqa.selenium.WebDriver;
import org.testng.annotations.Test;

public class FluentTest {

    @Test
    public void testFluentLogin() {
        WebDriver driver = null; // Mocked for example purposes
        
        // Start on the Login Page
        FluentLoginPage loginPage = new FluentLoginPage(driver);
        
        System.out.println("--- Starting Fluent UI Flow ---");
        
        // 🌟 Look at this beautiful Method Chaining!
        loginPage
            .enterUsername("admin")
            .enterPassword("supersecret")
            .clickLogin()            // This dynamically returns the HomePage object!
            .verifyWelcomeMessage()  // Now we are seamlessly calling HomePage methods
            .clickLogout();
    }
}
