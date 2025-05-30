# Architecture Policy Evaluation Report

**Diagram**: `DirectDebitMandateUpdateArchitectureComponentDiagram.puml`
**Date**: 2025-05-30 13:18:04

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
- 1: The UML diagram shows a relationship where the "MandateUpdateService" container connects directly to the "ThoughtMachine" external system. This violates the policy rule which states that only the "VaultCoreClient" adapter is allowed to connect to the "ThoughtMachine" external system. According to the policy logic, any container other than "VaultCoreClient" accessing "ThoughtMachine" directly should be denied.

Suggestions:
- 1: Modify the architecture so that the "MandateUpdateService" does not directly connect to "ThoughtMachine". Instead, ensure that all interactions with "ThoughtMachine" are routed through the "VaultCoreClient" adapter. This can be achieved by having "MandateUpdateService" call "VaultCoreClient" for any operations that require access to "ThoughtMachine", thereby adhering to the policy requirement.

---

### Compliant Policies

#### ARC-POLICY-101 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram adheres to the provided OPA policy. All microservices (WebAPI, ServiceLayer, and VaultCoreClient) are defined within a system boundary labeled "ecs," which complies with the policy requirement that microservices must be deployed within a system boundary labeled 'Fargate' or 'ECS'. Therefore, there are no deviations from the policy, and the architecture is compliant.

---

#### ARC-POLICY-102 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy checks whether any external system connects directly to a non-API-Gateway component. In the UML diagram, the external system "ClientApp" connects to "ApiGateway," which is an allowed connection according to the policy. There are no direct connections from external systems to non-API-Gateway components, thus adhering to the policy requirements.

---

#### ARC-POLICY-104 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The `VaultCoreClient` container, which makes an external call to the `ThoughtMachine` system, is correctly annotated with the stereotype `<<uses_secret>>`, satisfying the policy requirement that containers making external calls must be marked as using secrets. Therefore, there are no deviations from the policy, and the architecture is compliant.

---

#### ARC-POLICY-105 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram includes an "Audit Log" container with the technology "Amazon RDS PostgreSQL" and the stereotype "data_store," which satisfies the policy requirement for a data store related to audit or logging. Therefore, the architecture complies with the policy ARC-POLICY-105, as it includes the necessary audit log or persistent data store for compliance.

---

#### ARC-POLICY-106 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy requires that at least one container must have 'secrets' in the name or be labeled <<secrets_store>>. The UML diagram includes a container named "AWS Secrets Manager" with the stereotype <<secrets_store>>, which satisfies the policy requirement. Therefore, there are no deviations from the policy, and no suggestions for changes are necessary.

---

#### ARC-POLICY-108 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the policy ARC-POLICY-108. The policy requires at least one container to be labeled as <<observability>> or include 'cloudwatch' in the name. The UML diagram includes a container named "Amazon CloudWatch" with the stereotype <<observability>>, satisfying the policy requirement.

---

