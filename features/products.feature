Feature: Product Store Administration Interface

Background:
    Given the following products
        | name       | description     | price  | available | category   |
        | Laptop     | High performance| 899.99 | True      | ELECTRONICS|
        | Smartphone | Dual SIM 5G     | 450.00 | False     | ELECTRONICS|
        | Mouse      | Wireless mouse  | 25.50  | True      | TOOLS       |
        | Monitor    | 4K Display      | 299.99 | True      | ELECTRONICS|

Scenario: Read a Product
    When I visit the "Home Page"
    And I set the "Name" to "Laptop"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" element
    And I press the "Clear" button
    And I paste the "Id" element
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Laptop" in the "Name" field

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "Laptop"
    And I press the "Search" button
    Then I should see the message "Success"
    When I set the "Description" to "Updated Description Text"
    And I press the "Update" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I set the "Name" to "Laptop"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Updated Description Text" in the "Description" field

Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Name" to "Mouse"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" element
    And I press the "Delete" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I paste the "Id" element
    And I press the "Retrieve" button
    Then I should see the message "404 Not Found"

Scenario: List All Products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Laptop" in the results
    And I should see "Smartphone" in the results
    And I should see "Mouse" in the results

Scenario: Search by Category
    When I visit the "Home Page"
    And I select "Tools" from the "Category" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Mouse" in the results
    And I should NOT see "Laptop" in the results

Scenario: Search by Availability
    When I visit the "Home Page"
    And I select "True" from the "Available" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Laptop" in the results
    And I should NOT see "Smartphone" in the results

Scenario: Search by Name
    When I visit the "Home Page"
    And I set the "Name" to "Monitor"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Monitor" in the results
    And I should NOT see "Mouse" in the results