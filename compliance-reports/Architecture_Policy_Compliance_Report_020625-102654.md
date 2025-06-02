# Architecture Policy Evaluation Report

**Diagram**: `DirectDebitMandateUpdateArchitectureComponentDiagram.puml`
**Date**: 2025-06-02 10:26:52

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
- 1: The UML diagram indicates that the `MandateUpdateService` container has a relationship with the `ThoughtMachine` external system. This violates the policy rule which states that only the `VaultCoreClient` adapter is allowed to connect to the `ThoughtMachine` external system. The policy logic explicitly checks for any source other than `VaultCoreClient` attempting to access `ThoughtMachine` and flags it as non-compliant.

Suggestions:
- 1: To fix this deviation, ensure that the `MandateUpdateService` does not directly connect to the `ThoughtMachine` external system. Instead, route all interactions with `ThoughtMachine` through the `VaultCoreClient`. This can be achieved by modifying the architecture so that `MandateUpdateService` communicates with `VaultCoreClient`, which then handles all interactions with `ThoughtMachine`. Update the UML diagram to reflect this change by removing the direct relationship between `MandateUpdateService` and `ThoughtMachine` and adding a relationship between `MandateUpdateService` and `VaultCoreClient` for mandate update operations.

---

### Compliant Policies

#### ARC-POLICY-101 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

Conclusion:
The UML diagram complies with the provided OPA policy. All microservices (WebAPI, ServiceLayer, VaultCoreClient) are defined within a system boundary labeled "ecs," which satisfies the policy requirement that containers must be deployed in ECS Fargate. Therefore, there are no deviations from the policy, and no suggestions for changes are necessary.

---

#### ARC-POLICY-102 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy checks that external systems do not connect directly to non-API-Gateway components. In the UML diagram, the external system "ClientApp" connects to "ApiGateway," which is a valid API Gateway alias according to the policy. Therefore, there are no violations or deviations from the policy logic.

---

#### ARC-POLICY-104 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The `VaultCoreClient` container, which makes an external call to `ThoughtMachine`, is correctly annotated with the stereotype `<<uses_secret>>`, satisfying the policy requirement that containers making external calls must be marked as using secrets. Therefore, there are no deviations from the policy.

---

#### ARC-POLICY-105 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy requires the architecture to include a data store related to audit or logging, specifically mentioning technologies like PostgreSQL or RDS, or having a stereotype of "data_store". The UML diagram includes an "Audit Log" container with the technology "Amazon RDS PostgreSQL" and the stereotype "data_store", which satisfies the policy requirements. Therefore, there are no deviations from the policy, and no suggestions for changes are necessary.

---

#### ARC-POLICY-106 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy requires that at least one container must have 'secrets' in the name or be labeled <<secrets_store>>. The UML diagram includes a container named "AWS Secrets Manager" with the stereotype "secrets_store", which satisfies the policy requirement. Therefore, there are no deviations from the policy, and no suggestions for fixes are necessary.

---

#### ARC-POLICY-108 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy requires at least one container to be labeled as <<observability>> or to include 'cloudwatch' in the name. The UML diagram includes the "Amazon CloudWatch" container, which is labeled with the stereotype <<observability>> and also contains 'cloudwatch' in its name. Therefore, the architecture meets the policy requirements, and no deviations are present.

---

