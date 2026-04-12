package com.framework.screenplay.tasks;

import com.framework.screenplay.core.Actor;
import com.framework.screenplay.core.Task;
import org.openqa.selenium.By;

/**
 * Concrete Task for Logging In.
 * Encapsulates the specific steps to achieve the business goal of authenticating.
 */
public class LoginTask implements Task {
    
    private String username;
    private String password;
    
    // UI Targets (Usually stored in a separate Target class)
    private By userField = By.id("username");
    private By passField = By.id("password");
    private By loginBtn = By.id("submit");

    public LoginTask(String username, String password) {
        this.username = username;
        this.password = password;
    }

    // Factory method for readable syntax
    public static LoginTask withCredentials(String user, String pass) {
        return new LoginTask(user, pass);
    }

    @Override
    public void performAs(Actor actor) {
        System.out.println("   -> Entering username: " + username);
        // actor.getDriver().findElement(userField).sendKeys(username);
        
        System.out.println("   -> Entering password: [MASKED]");
        // actor.getDriver().findElement(passField).sendKeys(password);
        
        System.out.println("   -> Clicking Login");
        // actor.getDriver().findElement(loginBtn).click();
    }
}
