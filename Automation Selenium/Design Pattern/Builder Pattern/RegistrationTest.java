package com.builderpattern.pom;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

public class RegistrationTest {
    private WebDriver driver;
    private RegistrationPage registrationPage;

    @BeforeMethod
    public void setup() {
        // Setup simplified for example purposes
        driver = new ChromeDriver();
        registrationPage = new RegistrationPage(driver);
        driver.get("https://example-registration.com");
    }

    @Test
    public void testRegistrationWithAllFields() {
        // Using the Builder Pattern to create a complex object with optional fields (Fluent API)
        UserAccount fullUser = new UserAccount.UserAccountBuilder("John", "Doe", "john@email.com", "SecurePass123")
                .withPhone("555-1234")
                .withAddress("123 Main St, Tech City")
                .build();

        // The test code reads beautifully like an English sentence
        registrationPage.registerUser(fullUser);
    }

    @Test
    public void testRegistrationWithMandatoryFieldsOnly() {
        // Using the Builder Pattern to create an object with ONLY mandatory fields
        UserAccount basicUser = new UserAccount.UserAccountBuilder("Jane", "Smith", "jane@email.com", "Pass456!")
                .build();

        registrationPage.registerUser(basicUser);
    }

    @AfterMethod
    public void teardown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
