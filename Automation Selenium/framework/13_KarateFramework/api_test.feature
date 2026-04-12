Feature: Advanced API Testing with Karate

  Background:
    # ADVANCED CONCEPT: Global configurations and Base URLs
    * url 'https://reqres.in/api'
    * header Accept = 'application/json'
    
    # ADVANCED CONCEPT: Java Interoperability
    # Karate allows you to call Java methods directly from the Feature file!
    # Useful for generating dynamic data (like random emails) or hashing passwords.
    * def DataGenerator = Java.type('com.framework.karate.utils.DataGenerator')
    * def randomName = DataGenerator.getRandomName()

  Scenario: Create a new user and perform deep JSON assertion
    Given path '/users'
    And request { "name": "#(randomName)", "job": "leader" }
    When method post
    Then status 201
    
    # ADVANCED CONCEPT: Fuzzy Matching
    # In RestAssured, asserting dynamic fields (like auto-generated IDs or timestamps) requires extraction and Regex.
    # Karate has built-in 'Fuzzy Matchers'.
    # '#string' ensures the name is text. '#notnull' ensures an ID was created. '#ignore' ignores the timestamp.
    And match response == 
    """
    {
      "name": "#string",
      "job": "leader",
      "id": "#notnull",
      "createdAt": "#ignore"
    }
    """
    
    # Variable Extraction for Chaining
    * def newUserId = response.id
    * print 'Generated User ID is: ', newUserId

  Scenario: Chain the extracted ID to a GET request
    # This scenario relies on the ID generated in the previous step (or fetched via a setup call)
    Given path '/users', 2  # Hardcoded for example, but could be #(newUserId)
    When method get
    Then status 200
    
    # Deep nested assertion using JsonPath directly in the match
    And match response.data.first_name == 'Janet'
    
    # Array assertion: Ensure the response contains exactly what we expect
    # And match response.data[*].id contains [1, 2, 3]
