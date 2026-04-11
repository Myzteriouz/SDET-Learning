package com.strategypattern.pom;

import org.openqa.selenium.WebDriver;

/**
 * The Context Class in the Strategy Pattern (also a POM class).
 * The CheckoutPage doesn't know HOW the payment is processed.
 * It just takes a PaymentStrategy and executes it.
 */
public class CheckoutPage {
    private WebDriver driver;
    
    public CheckoutPage(WebDriver driver) {
        this.driver = driver;
    }

    /**
     * ADVANCED CONCEPT: Inversion of Control (IoC) / Strategy injection.
     * The CheckoutPage delegates the payment logic to the provided Strategy object.
     * This avoids massive if/else or switch statements in the POM (e.g., if paymentType == "CC" else if paymentType == "PayPal").
     *
     * @param paymentMethod The strategy to use (CreditCardPayment or PayPalPayment)
     * @param amount The total order amount
     */
    public void completeCheckout(PaymentStrategy paymentMethod, double amount) {
        // ... perform pre-payment steps (e.g., verify cart total) ...
        
        // Execute the strategy
        paymentMethod.pay(amount);
        
        // ... perform post-payment steps (e.g., verify success message) ...
    }
}
