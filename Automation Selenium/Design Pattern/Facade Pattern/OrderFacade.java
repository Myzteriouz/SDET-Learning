package com.facadepattern.pom;

import org.openqa.selenium.WebDriver;

// Mocked Page Object for example
class LoginPage {
    private WebDriver driver;
    public LoginPage(WebDriver driver) { this.driver = driver; }
    
    public void login(String user, String pass) {
        System.out.println("[LoginPage] Logging in with user: " + user);
    }
}

// Mocked Page Object for example
class SearchPage {
    private WebDriver driver;
    public SearchPage(WebDriver driver) { this.driver = driver; }
    
    public void searchItem(String item) {
        System.out.println("[SearchPage] Searching for: " + item);
    }
    
    public void addToCart() {
        System.out.println("[SearchPage] Adding top result to cart.");
    }
}

// Mocked Page Object for example
class CartPage {
    private WebDriver driver;
    public CartPage(WebDriver driver) { this.driver = driver; }
    
    public void checkout() {
        System.out.println("[CartPage] Proceeding to checkout and processing order.");
    }
}

/**
 * The Facade Class.
 * Provides a simple, high-level interface to a complex subsystem of Page Objects.
 */
public class OrderFacade {
    private LoginPage loginPage;
    private SearchPage searchPage;
    private CartPage cartPage;

    public OrderFacade(WebDriver driver) {
        this.loginPage = new LoginPage(driver);
        this.searchPage = new SearchPage(driver);
        this.cartPage = new CartPage(driver);
    }

    /**
     * ADVANCED CONCEPT: Macro-Action / Workflow Encapsulation.
     * Instead of writing 15 lines of code in the test script to complete a purchase,
     * the test calls one simple method. This keeps tests highly readable and completely
     * isolates them from POM structural changes.
     */
    public void placeOrder(String username, String password, String itemName) {
        System.out.println("--- Starting Order Facade Workflow ---");
        
        loginPage.login(username, password);
        searchPage.searchItem(itemName);
        searchPage.addToCart();
        cartPage.checkout();
        
        System.out.println("--- Order Facade Workflow Complete ---");
    }
}
