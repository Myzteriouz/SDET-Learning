package com.facadepattern.pom;

import org.openqa.selenium.WebDriver;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

public class FacadeTest {
    private WebDriver driver;
    private OrderFacade orderFacade;

    @BeforeMethod
    public void setup() {
        // Driver initialization mocked for example
        // driver = new ChromeDriver();
        
        // We initialize the Facade once
        orderFacade = new OrderFacade(driver);
    }

    @Test
    public void testEndToEndOrder() {
        // Look how clean the test is!
        // The test doesn't care about page navigations, clicking specific buttons, or finding inputs.
        // It purely focuses on the high-level business logic.
        
        orderFacade.placeOrder("testuser", "secure123", "Gaming Laptop");
        
        // Assertions would go here (e.g., verifying order success message)
    }
}
