package com.strategypattern.pom;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

public class CheckoutTest {
    private WebDriver driver;
    private CheckoutPage checkoutPage;

    @BeforeMethod
    public void setup() {
        // Setup simplified
        driver = new ChromeDriver();
        checkoutPage = new CheckoutPage(driver);
        driver.get("https://example-store.com/checkout");
    }

    @Test
    public void testCheckoutWithCreditCard() {
        // Instantiate the specific strategy
        PaymentStrategy ccPayment = new CreditCardPayment(driver, "Alice Smith", "1234-5678-9012-3456");
        
        // Inject the strategy into the context (POM)
        checkoutPage.completeCheckout(ccPayment, 150.00);
    }

    @Test
    public void testCheckoutWithPayPal() {
        // Instantiate a different strategy without changing the CheckoutPage code
        PaymentStrategy paypalPayment = new PayPalPayment(driver, "alice@example.com", "superSecure1!");
        
        // Inject the strategy
        checkoutPage.completeCheckout(paypalPayment, 150.00);
    }

    @AfterMethod
    public void teardown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
