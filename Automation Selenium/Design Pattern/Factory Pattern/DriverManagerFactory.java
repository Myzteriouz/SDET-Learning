package com.factorypattern.framework;

/**
 * The Factory Class.
 * This class is responsible for instantiating the correct concrete DriverManager 
 * based on the requested BrowserType (e.g., Chrome, Firefox).
 */
public class DriverManagerFactory {

    /**
     * Factory Method to get the appropriate Manager instance.
     * 
     * @param type The requested BrowserType enum.
     * @return An instance of a specific DriverManager (e.g., ChromeDriverManager).
     */
    public static DriverManager getManager(BrowserType type) {
        
        DriverManager driverManager;

        // Switch statement creates the correct subclass of DriverManager.
        // It hides the complexity of instantiation from the test scripts.
        switch (type) {
            case CHROME:
                driverManager = new ChromeDriverManager();
                break;
            case FIREFOX:
                // driverManager = new FirefoxDriverManager(); // Assuming Firefox is implemented similarly
                throw new UnsupportedOperationException("Firefox is not yet fully implemented in this example.");
            default:
                // Fails fast if an unsupported browser type is requested.
                throw new IllegalArgumentException("Unsupported browser type: " + type);
        }
        
        return driverManager;
    }
}
