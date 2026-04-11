package com.strategypattern.pom;

/**
 * The Strategy Interface.
 * Defines the contract that all payment strategies must follow.
 */
public interface PaymentStrategy {
    
    /**
     * Executes the payment workflow on the UI.
     * @param amount The amount to be paid.
     */
    void pay(double amount);
}
