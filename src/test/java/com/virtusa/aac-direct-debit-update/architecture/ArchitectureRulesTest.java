package com.virtusa.aac-direct-debit-update.architecture;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.library.Architectures;
import org.junit.jupiter.api.Test;

public class ArchitectureRulesTest {

    @Test
    void layerDependenciesAreRespected() {
        JavaClasses importedClasses = new ClassFileImporter().importPackages("com.virtusa.aac-direct-debit-update");

        Architectures.layeredArchitecture()
            .layer("Controller").definedBy("..controller..")
            .layer("Service").definedBy("..service..")
            .layer("Client").definedBy("..client..")

            .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
            .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
            .whereLayer("Client").mayOnlyBeAccessedByLayers("Service")
            .check(importedClasses);
    }
}
