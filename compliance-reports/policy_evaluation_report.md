# Architecture Policy Evaluation Report

**Diagram**: `DirectDebitMandateUpdateArchitectureComponentDiagram.puml`
**Date**: 2025-05-29 13:36:42

## Summary of Compliance

| Policy ID      | Compliance Status |
|----------------|-------------------|
| ARC-POLICY-101      | ✅ Yes    |
| ARC-POLICY-102      | ✅ Yes    |
| ARC-POLICY-103      | ❌ No    |
| ARC-POLICY-104      | ✅ Yes    |
| ARC-POLICY-105      | ✅ Yes    |
| ARC-POLICY-106      | ✅ Yes    |
| ARC-POLICY-108      | ✅ Yes    |

## Detailed Policy Evaluations

### Non-Compliant Policies

#### ARC-POLICY-103 - ❌ NON-COMPLIANT

**Evaluation Details:**
Compliance: No

Deviations:
- 1: The UML diagram indicates that the "MandateUpdateService" container has a relationship with the "ThoughtMachine" external system. This violates the policy, which explicitly states that only the "VaultCoreClient" adapter is allowed to connect to the "ThoughtMachine" external system. The policy logic checks for any source other than "VaultCoreClient" attempting to connect to "ThoughtMachine" and flags it as non-compliant.

Suggestions:
- 1: To fix this deviation, ensure that the "MandateUpdateService" container does not directly connect to the "ThoughtMachine" external system. Instead, route any interactions with "ThoughtMachine" through the "VaultCoreClient" adapter. This can be achieved by modifying the architecture so that "MandateUpdateService" communicates with "VaultCoreClient" for any operations involving "ThoughtMachine". Update the UML diagram to reflect this change, ensuring compliance with the policy.

---

### Compliant Policies

#### ARC-POLICY-101 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. All microservices ("WebAPI", "ServiceLayer", and "VaultCoreClient") are defined within a system boundary labeled "ecs", which aligns with the policy requirement that microservices must be deployed in ECS Fargate. Therefore, there are no deviations from the policy, and no suggestions for changes are necessary.

---

#### ARC-POLICY-102 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram adheres to the provided OPA policy. The policy checks that external systems do not connect directly to non-API-Gateway components. In the UML diagram, the external system "ClientApp" connects to "ApiGateway," which is a valid API Gateway alias according to the policy. No direct connections from external systems to non-API-Gateway components are present in the relationships provided in the policy input JSON. Therefore, the architecture is compliant with the policy ARC-POLICY-102.

---

#### ARC-POLICY-104 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy checks if any container making external calls is not marked as using secrets. In the provided input JSON, the `VaultCoreClient` container, which makes an external call to `ThoughtMachine`, is correctly annotated with the stereotype `uses_secret`. Therefore, there are no deviations from the policy, and the architecture is compliant.

---

#### ARC-POLICY-105 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram includes an "Audit Log" component with the technology "Amazon RDS PostgreSQL" and the stereotype "data_store," which satisfies the policy requirement for a data store related to audit or logging. Therefore, the architecture complies with the policy ARC-POLICY-105, and no deviations are found.

---

#### ARC-POLICY-106 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided policy. The policy requires that at least one container must have 'secrets' in the name or be labeled <<secrets_store>>. The UML diagram includes a container named "AWS Secrets Manager" with the stereotype <<secrets_store>>, which satisfies the policy requirement. Therefore, there are no deviations, and the architecture is compliant with the policy ARC-POLICY-106.

---

#### ARC-POLICY-108 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the policy ARC-POLICY-108. The policy requires at least one container to be labeled as <<observability>> or include 'cloudwatch' in the name. The UML diagram includes a container named "Amazon CloudWatch" with the stereotype <<observability>>, satisfying the policy requirement. Therefore, there are no deviations, and the architecture is compliant.

---

