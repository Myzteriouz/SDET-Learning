package com.builderpattern.pom;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * Page Object Model (POM) class representing a Registration Page.
 * It consumes the UserAccount object created by the Builder to fill the form.
 */
public class RegistrationPage {
    private WebDriver driver;

    // Locators
    private By firstNameInput = By.id("firstName");
    private By lastNameInput = By.id("lastName");
    private By emailInput = By.id("email");
    private By passwordInput = By.id("password");
    private By phoneInput = By.id("phone");
    private By addressInput = By.id("address");
    private By submitButton = By.id("submitBtn");

    public RegistrationPage(WebDriver driver) {
        this.driver = driver;
    }

    /**
     * ADVANCED CONCEPT: Passing a Data Object (POJO) to a POM method.
     * Instead of passing 6 parameters like register(fn, ln, email, pass, phone, address),
     * we pass the single UserAccount object. This keeps the POM clean and scalable.
     */
    public void registerUser(UserAccount user) {
        driver.findElement(firstNameInput).sendKeys(user.getFirstName());
        driver.findElement(lastNameInput).sendKeys(user.getLastName());
        driver.findElement(emailInput).sendKeys(user.getEmail());
        driver.findElement(passwordInput).sendKeys(user.getPassword());

        // Handle optional fields: Only interact with the UI if the data was provided by the Builder
        if (user.getPhone() != null) {
            driver.findElement(phoneInput).sendKeys(user.getPhone());
        }
        
        if (user.getAddress() != null) {
            driver.findElement(addressInput).sendKeys(user.getAddress());
        }

        driver.findElement(submitButton).click();
    }
}
