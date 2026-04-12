package com.framework.bdd.steps;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;

/**
 * Step Definitions Class.
 * Acts as the 'glue' code mapping the plain-English Gherkin steps to actual Java/Selenium code.
 */
public class LoginSteps {

    // Dependency Injection (like PicoContainer) would normally inject the WebDriver/PageObjects here.

    @Given("I navigate to the login page")
    public void navigateToLogin() {
        System.out.println("[Step] Driver navigating to Login URL...");
        // driver.get("https://example.com/login");
    }

    @When("I enter the username {string}")
    public void enterUsername(String username) {
        System.out.println("[Step] Typing username: " + username);
        // loginPage.enterUsername(username);
    }

    @When("I enter the password {string}")
    public void enterPassword(String password) {
        System.out.println("[Step] Typing password: " + password);
        // loginPage.enterPassword(password);
    }

    @When("I click the login button")
    public void clickLogin() {
        System.out.println("[Step] Clicking Login Button.");
        // loginPage.clickLoginBtn();
    }

    @Then("I should see the dashboard page")
    public void verifyDashboard() {
        System.out.println("[Step] Asserting Dashboard is visible.");
        // Assert.assertTrue(dashboardPage.isDisplayed());
    }
}
