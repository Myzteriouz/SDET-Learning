package com.framework.screenplay.tests;

import com.framework.screenplay.core.Actor;
import com.framework.screenplay.tasks.LoginTask;
import org.openqa.selenium.WebDriver;
import org.testng.annotations.Test;

public class ScreenplayTest {

    @Test
    public void testUserLoginUsingScreenplay() {
        WebDriver mockedDriver = null;
        
        // 1. Instantiate the Actor
        Actor john = Actor.named("John the Admin");
        
        // 2. Give them the Ability
        john.canBrowseTheWebWith(mockedDriver);
        
        System.out.println("--- Starting Screenplay Pattern Test ---");
        
        // 3. The Actor performs high-level business Tasks
        // This is the epitome of readable, BDD-aligned code!
        john.attemptsTo(
            LoginTask.withCredentials("admin_user", "supersecret123")
            // AddItemTask.toCart("Laptop"),
            // CheckoutTask.withCreditCard("Visa")
        );
        
        // 4. Then we would use Questions to assert state
        // e.g., john.shouldSee(TheCart.totalIs("$1500"));
    }
}
