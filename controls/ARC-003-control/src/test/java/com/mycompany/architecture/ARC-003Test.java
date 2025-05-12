
package com.mycompany.architecture;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.ArchRule;
import org.junit.jupiter.api.Test;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;


public class ARC003Test {

    @Test
    void domain_should_not_depend_on_dto_or_controller_packages() {
        JavaClasses classes = new ClassFileImporter().importPackages("com.mycompany");
        ArchRule rule = noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat().resideInAnyPackage("..dto..", "..controller..")
            .because("Domain layer must not depend on controller or DTO packages.");
        rule.check(classes);
    }
}
