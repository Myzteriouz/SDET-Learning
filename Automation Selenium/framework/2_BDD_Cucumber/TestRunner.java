package com.framework.bdd.runner;

import io.cucumber.testng.AbstractTestNGCucumberTests;
import io.cucumber.testng.CucumberOptions;

/**
 * The Cucumber Test Runner.
 * Configures where to find the feature files, step definitions, and how to generate reports.
 */
@CucumberOptions(
        features = "src/test/resources/features",      // Path to Gherkin files
        glue = "com.framework.bdd.steps",              // Path to Step Definitions
        tags = "@Regression and not @WIP",             // ADVANCED: Tag management for CI/CD pipelines
        plugin = {
            "pretty",                                  // Console output
            "html:target/cucumber-reports/report.html",// Standard HTML report
            "json:target/cucumber-reports/Cucumber.json"// JSON for CI/CD integrations (e.g. Jenkins plugins)
        },
        monochrome = true // Makes console output readable
)
public class TestRunner extends AbstractTestNGCucumberTests {
    // Extending AbstractTestNGCucumberTests integrates Cucumber natively with TestNG's execution lifecycle.
    // This allows us to run parallel BDD scenarios using TestNG's parallel execution capabilities.
}
