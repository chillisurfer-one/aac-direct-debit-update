
package com.mycompany.architecture;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.ArchRule;
import org.junit.jupiter.api.Test;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.classes;

public class ARC007Test {

    @Test
    void all_classes_should_be_in_mycompany_directdebitupdate_package() {
        JavaClasses classes = new ClassFileImporter().importPackages("com.mycompany");

        ArchRule rule = classes()
            .should().resideInAPackage("..com.mycompany.directdebitupdate..")
            .because("All classes should be part of the com.mycompany.directdebitupdate package hierarchy.");
        rule.check(classes);
    }
}
