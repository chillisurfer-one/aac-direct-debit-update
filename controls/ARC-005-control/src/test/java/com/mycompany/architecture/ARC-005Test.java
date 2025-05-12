
package com.mycompany.architecture;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.ArchRule;
import org.junit.jupiter.api.Test;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;


import org.springframework.beans.factory.annotation.Autowired;

public class ARC005Test {

    @Test
    void no_field_injection_should_be_used() {
        JavaClasses classes = new ClassFileImporter().importPackages("com.mycompany");
        ArchRule rule = noFields()
            .should().beAnnotatedWith(Autowired.class)
            .because("Use constructor injection instead of field injection.");
        rule.check(classes);
    }
}
