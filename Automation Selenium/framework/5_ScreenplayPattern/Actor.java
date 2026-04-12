package com.framework.screenplay.core;

import org.openqa.selenium.WebDriver;

/**
 * The 'Who' in Screenplay.
 * An Actor represents the user interacting with the system.
 * They have 'Abilities' (like browsing the web) and perform 'Tasks'.
 */
public class Actor {
    private String name;
    private WebDriver driver; // Ability to browse the web

    public Actor(String name) {
        this.name = name;
    }

    public static Actor named(String name) {
        return new Actor(name);
    }

    public Actor canBrowseTheWebWith(WebDriver driver) {
        this.driver = driver;
        return this;
    }

    public WebDriver getDriver() {
        return this.driver;
    }

    // The core of Screenplay: The actor attempts to do something.
    public void attemptsTo(Task... tasks) {
        for (Task task : tasks) {
            System.out.println("🎭 " + name + " attempts to: " + task.getClass().getSimpleName());
            task.performAs(this);
        }
    }
}
