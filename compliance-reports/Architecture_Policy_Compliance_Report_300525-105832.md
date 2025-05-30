# Architecture Policy Evaluation Report

**Diagram**: `DirectDebitMandateUpdateArchitectureComponentDiagram.puml`
**Date**: 2025-05-30 10:58:31

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
- 1: The UML diagram shows a relationship where the `MandateUpdateService` container connects directly to the `ThoughtMachine` external system. This violates the policy which states that only the `VaultCoreClient` adapter is allowed to connect to the `ThoughtMachine` external system. The policy logic specifically checks that the source of any connection to `ThoughtMachine` must be `VaultCoreClient`, and any other source results in a denial message.

Suggestions:
- 1: To fix this deviation, modify the UML diagram so that the `MandateUpdateService` does not directly connect to `ThoughtMachine`. Instead, ensure that the `MandateUpdateService` communicates with `VaultCoreClient`, which then handles the connection to `ThoughtMachine`. This can be achieved by removing the direct relationship between `MandateUpdateService` and `ThoughtMachine` and ensuring all interactions with `ThoughtMachine` are routed through `VaultCoreClient`.

---

### Compliant Policies

#### ARC-POLICY-101 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

Conclusion: The UML diagram complies with the provided OPA policy. All microservices (WebAPI, ServiceLayer, and VaultCoreClient) are defined within a system boundary labeled "ecs," which matches the policy requirement for deployment in ECS Fargate.

---

#### ARC-POLICY-102 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

Conclusion:
The UML diagram adheres to the provided OPA policy. The relationships defined in the policy input JSON match the expected connections in the UML diagram, ensuring that external systems only connect to the API Gateway, which is compliant with the policy logic. There are no direct connections from external systems to non-API-Gateway components, thus satisfying the policy requirements.

---

#### ARC-POLICY-104 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy checks whether any container making external calls is annotated with the stereotype <<uses_secret>>. The container "VaultCoreClient" in the UML diagram makes an external call to "ThoughtMachine" and is correctly annotated with <<uses_secret>>, satisfying the policy requirements. Therefore, there are no deviations from the policy, and no suggestions for changes are necessary.

---

#### ARC-POLICY-105 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy requires the architecture to include a data store related to audit or logging, specifically mentioning technologies such as PostgreSQL or RDS, or having a stereotype of "data_store". The UML diagram includes an "Audit Log" container using "Amazon RDS PostgreSQL" with the stereotype "data_store", which satisfies the policy requirements. Therefore, there are no deviations from the policy, and no suggestions for changes are necessary.

---

#### ARC-POLICY-106 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the policy ARC-POLICY-106. The policy requires that at least one container must have 'secrets' in the name or be labeled <<secrets_store>>. The UML diagram includes a container named "AWS Secrets Manager" with the stereotype <<secrets_store>>, which satisfies the policy requirement. Therefore, there are no deviations, and no suggestions for fixes are necessary.

---

#### ARC-POLICY-108 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy requires at least one container to be labeled as <<observability>> or include 'cloudwatch' in the name. The UML diagram includes a container named "Amazon CloudWatch" with the stereotype <<observability>>, which satisfies the policy requirement. Therefore, there are no deviations from the policy, and no suggestions for changes are necessary.

---

