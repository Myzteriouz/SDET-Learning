package com.builderpattern.pom;

/**
 * A POJO representing a User Account, constructed using the Builder Pattern.
 * This is extremely useful for complex forms where some fields are optional.
 */
public class UserAccount {
    private final String firstName;
    private final String lastName;
    private final String email;
    private final String password;
    private final String phone; // Optional field
    private final String address; // Optional field

    // Private constructor so it can only be created via the Builder
    private UserAccount(UserAccountBuilder builder) {
        this.firstName = builder.firstName;
        this.lastName = builder.lastName;
        this.email = builder.email;
        this.password = builder.password;
        this.phone = builder.phone;
        this.address = builder.address;
    }

    // Getters for the POM to access the data
    public String getFirstName() { return firstName; }
    public String getLastName() { return lastName; }
    public String getEmail() { return email; }
    public String getPassword() { return password; }
    public String getPhone() { return phone; }
    public String getAddress() { return address; }

    /**
     * The Static Inner Builder Class
     */
    public static class UserAccountBuilder {
        // Mandatory fields
        private final String firstName;
        private final String lastName;
        private final String email;
        private final String password;

        // Optional fields (initialized to null or default values)
        private String phone;
        private String address;

        // Constructor for the Builder requires all mandatory fields
        public UserAccountBuilder(String firstName, String lastName, String email, String password) {
            this.firstName = firstName;
            this.lastName = lastName;
            this.email = email;
            this.password = password;
        }

        // Setter methods for optional fields that return the Builder instance (Fluent Interface)
        public UserAccountBuilder withPhone(String phone) {
            this.phone = phone;
            return this;
        }

        public UserAccountBuilder withAddress(String address) {
            this.address = address;
            return this;
        }

        // The build method that creates the final UserAccount object
        public UserAccount build() {
            return new UserAccount(this);
        }
    }
}
