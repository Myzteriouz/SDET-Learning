package com.framework.agentic;

import org.testng.annotations.Test;

public class AgenticAITest {

    @Test
    public void testAutonomousCheckout() {
        
        // Initialize the Agent with an LLM API Key
        AutonomousAgent aiAgent = new AutonomousAgent("sk-mock-openai-key-2026");
        
        System.out.println("--- Starting Agentic/AI-Driven Test Execution ---");
        
        // Notice there are NO Locators! No Page Objects! No XPaths!
        // We pass Context and Intent (Prompt Engineering for QA)
        
        aiAgent.executeIntent("Find the first item that costs less than $50 and add it to the cart.");
        
        aiAgent.executeIntent("Proceed to checkout, fill in dummy credit card details, and submit the order.");
        
        aiAgent.executeIntent("Verify that the order success confirmation message is visible.");
        
        System.out.println("--- Test Complete. The framework self-healed and found the elements dynamically. ---");
    }
}
