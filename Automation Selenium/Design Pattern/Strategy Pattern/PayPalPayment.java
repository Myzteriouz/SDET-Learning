package com.strategypattern.pom;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * Concrete Strategy: Implements the UI steps for PayPal payment.
 */
public class PayPalPayment implements PaymentStrategy {
    private WebDriver driver;
    private String email;
    private String password;

    // Locators specific to the PayPal login modal
    private By ppEmailInput = By.id("paypalEmail");
    private By ppPasswordInput = By.id("paypalPass");
    private By ppLoginBtn = By.id("paypalLogin");

    public PayPalPayment(WebDriver driver, String email, String password) {
        this.driver = driver;
        this.email = email;
        this.password = password;
    }

    @Override
    public void pay(double amount) {
        System.out.println("Processing PayPal payment of $" + amount);
        // Automate the specific UI steps for PayPal payment
        driver.findElement(By.id("selectPayPal")).click();
        
        // Wait for modal, then enter details
        driver.findElement(ppEmailInput).sendKeys(email);
        driver.findElement(ppPasswordInput).sendKeys(password);
        driver.findElement(ppLoginBtn).click();
    }
}
