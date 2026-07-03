Feature: Authentication
  Scenario: Successful login via API
    Given I have valid credentials
    When I POST to /api/v1/auth/login/
    Then I should get a JWT token

  Scenario: Failed login via API
    Given I have invalid credentials
    When I POST to /api/v1/auth/login/
    Then I should get 401 status
