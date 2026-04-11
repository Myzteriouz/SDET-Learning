package com.strategypattern.pom;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * Concrete Strategy: Implements the UI steps for Credit Card payment.
 */
public class CreditCardPayment implements PaymentStrategy {
    private WebDriver driver;
    private String nameOnCard;
    private String cardNumber;

    // Locators specific to the Credit Card form
    private By ccNameInput = By.id("ccName");
    private By ccNumberInput = By.id("ccNum");
    private By ccSubmit = By.id("submitCC");

    public CreditCardPayment(WebDriver driver, String nameOnCard, String cardNumber) {
        this.driver = driver;
        this.nameOnCard = nameOnCard;
        this.cardNumber = cardNumber;
    }

    @Override
    public void pay(double amount) {
        System.out.println("Processing Credit Card payment of $" + amount);
        // Automate the specific UI steps for CC payment
        driver.findElement(By.id("selectCreditCard")).click();
        driver.findElement(ccNameInput).sendKeys(nameOnCard);
        driver.findElement(ccNumberInput).sendKeys(cardNumber);
        driver.findElement(ccSubmit).click();
    }
}
