# ♟️ Strategy Pattern in UI Automation (SDET Guide)

## 📌 What is the Strategy Pattern?
The Strategy Pattern is a behavioral design pattern that lets you define a family of algorithms (strategies), put each of them into a separate class, and make their objects interchangeable at runtime.

### 💡 The Problem it Solves in Automation:
**The "God Class" and "If-Else Hell".**
Imagine a `CheckoutPage` POM class. Customers can pay via Credit Card, PayPal, Crypto, or Bank Transfer.
Without the Strategy pattern, your `pay()` method would look like this:
```java
public void pay(String type) {
    if (type.equals("CC")) {
        // 10 lines of Credit Card UI locators and actions
    } else if (type.equals("PayPal")) {
        // 10 lines of PayPal UI locators and actions
    } else if (type.equals("Crypto")) { ... }
}
```
This violates the **Open/Closed Principle** (SOLID). Every time the dev team adds Apple Pay, you have to modify the `CheckoutPage` class, risking breaking existing flows.

### 🛠️ How Our Framework Uses It:
1. **`PaymentStrategy` (Interface):** Defines a single `pay(amount)` method.
2. **Concrete Strategies (`CreditCardPayment`, `PayPalPayment`):** These classes contain the *specific UI locators and interactions* required for their payment type.
3. **`CheckoutPage` (Context):** It simply accepts a `PaymentStrategy` object and calls `.pay()`. It delegates the work.

If the devs add "Apple Pay" tomorrow, we simply create an `ApplePayPayment` class. We **do not** touch the `CheckoutPage` class.

### 🌟 Advantages for SDETs
*   **Separation of Concerns:** UI Locators for the PayPal modal are stored in the PayPal strategy class, not polluting the main Checkout page.
*   **Runtime Interchangeability:** The test script decides which path to take dynamically, injecting the behavior into the POM.

---

## 🧠 Memory Trick for Interviews
### The "GPS Navigation App" 🗺️
*   **Context:** You enter your destination into Google Maps (The `CheckoutPage`).
*   **Strategies:** You can choose to get there by **Walking**, **Driving**, or **Biking**.
*   **Execution:** The app calculates the route (`.pay()`), but the *algorithm* (roads vs. sidewalks) is completely different depending on the strategy you selected. Google Maps doesn't care *how* you travel, it just executes the selected strategy.
*   **Key Phrase:** *"It encapsulates varying algorithms or UI workflows into separate classes, replacing messy if-else logic and adhering to the Open/Closed Principle."*