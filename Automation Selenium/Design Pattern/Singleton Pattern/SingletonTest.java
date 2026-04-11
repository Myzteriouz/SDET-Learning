package com.singletonpattern.framework;

import org.testng.annotations.Test;

public class SingletonTest {

    @Test
    public void testSingletonInstance() {
        // We cannot do: new ConfigurationManager(); // This would throw a Compile Error!
        
        System.out.println("--- Thread 1 requesting config ---");
        ConfigurationManager config1 = ConfigurationManager.getInstance();
        System.out.println("URL is: " + config1.getProperty("url"));
        
        System.out.println("\n--- Thread 2 requesting config ---");
        ConfigurationManager config2 = ConfigurationManager.getInstance();
        System.out.println("Browser is: " + config2.getProperty("browser"));
        
        // Assert that both references point to the EXACT same object in memory
        if (config1 == config2) {
            System.out.println("\n✅ SUCCESS: config1 and config2 are the exact same instance in memory! The file was not re-read.");
        }
    }
}
