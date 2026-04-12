Feature: User Authentication

  As a registered user
  I want to be able to log in
  So that I can access my dashboard

  # ADVANCED CONCEPT: Scenario Outline allows Data-Driven testing natively within BDD
  Scenario Outline: Verify login with different credential combinations
    Given I navigate to the login page
    When I enter the username "<username>"
    And I enter the password "<password>"
    And I click the login button
    Then I should see the dashboard page

    Examples:
      | username | password |
      | admin    | pass123  |
      | testuser | secure1  |
