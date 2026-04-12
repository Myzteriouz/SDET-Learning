*** Settings ***
Documentation     An example of a modern, keyword-driven Robot Framework suite.
...               This suite validates the User Authentication flow.
Library           SeleniumLibrary    # The core library for browser automation
Resource          ../resources/keywords.robot    # Import custom reusable keywords
Test Setup        Open Browser To Login Page    # Runs before every test
Test Teardown     Close Browser    # Runs after every test

*** Variables ***
# Configuration variables can be overridden at runtime via CI/CD (e.g., --variable BROWSER:firefox)
${BROWSER}        chrome
${BASE_URL}       https://example.com/login
${VALID_USER}     admin
${VALID_PASS}     supersecret

*** Test Cases ***
Valid User Should Be Able To Login
    [Documentation]    Verifies that a user with valid credentials can access the dashboard.
    [Tags]             Smoke    Regression
    
    # High-level Keywords (Read like plain English)
    Input Username    ${VALID_USER}
    Input Password    ${VALID_PASS}
    Submit Credentials
    Welcome Page Should Be Visible

Invalid User Should Be Denied Access
    [Documentation]    Verifies that wrong credentials trigger an error message.
    [Tags]             Regression    Negative
    
    # Passing arguments directly to keywords
    Input Username    invalid_user
    Input Password    wrong_password
    Submit Credentials
    Error Message Should Be Displayed    "Invalid credentials provided."

*** Keywords ***
# ADVANCED CONCEPT: Custom Keywords
# We abstract the raw Selenium locators away from the Test Cases section.
Open Browser To Login Page
    Open Browser    ${BASE_URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Implicit Wait    5 seconds

Input Username
    [Arguments]    ${username}
    Input Text     id:username_field    ${username}

Input Password
    [Arguments]    ${password}
    Input Text     id:password_field    ${password}

Submit Credentials
    Click Button   xpath://button[@type='submit']

Welcome Page Should Be Visible
    Wait Until Element Is Visible    id:dashboard_header
    Title Should Be    User Dashboard
