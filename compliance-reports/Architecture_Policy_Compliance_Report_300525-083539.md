# Architecture Policy Evaluation Report

**Diagram**: `DirectDebitMandateUpdateArchitectureComponentDiagram.puml`
**Date**: 2025-05-30 08:35:38

## Summary of Compliance

| Policy ID      | Compliance Status |
|----------------|-------------------|
| ARC-POLICY-101      | ✅ Yes    |
| ARC-POLICY-102      | ❌ No    |
| ARC-POLICY-103      | ❌ No    |
| ARC-POLICY-104      | ✅ Yes    |
| ARC-POLICY-105      | ✅ Yes    |
| ARC-POLICY-106      | ✅ Yes    |
| ARC-POLICY-108      | ✅ Yes    |

## Detailed Policy Evaluations

### Non-Compliant Policies

#### ARC-POLICY-102 - ❌ NON-COMPLIANT

**Evaluation Details:**
Compliance: No

Deviations:
- 1: The UML diagram shows a relationship from `ClientApp` to `ThoughtMachine`, which is an external system. This violates the policy because the policy states that external systems like `ClientApp` must not access non-API-Gateway components directly. The relationship from `ClientApp` to `ThoughtMachine` bypasses the `ApiGateway`, which is not allowed according to the policy logic.

Suggestions:
- 1: To fix this deviation, ensure that all interactions from `ClientApp` to any internal or external systems go through the `ApiGateway`. Specifically, remove the direct relationship between `ClientApp` and `ThoughtMachine` and route the interaction through the `ApiGateway`. This may involve updating the architecture to ensure that the `ApiGateway` can handle requests intended for `ThoughtMachine`.

Conclusion: The UML diagram does not comply with the policy due to the direct access from an external system to a non-API-Gateway component.

---

#### ARC-POLICY-103 - ❌ NON-COMPLIANT

**Evaluation Details:**
Compliance: No

Deviations:
- 1: The UML diagram shows a relationship where the "MandateUpdateService" container connects directly to the "ThoughtMachine" external system. This violates the policy which explicitly states that only the "VaultCoreClient" adapter is allowed to connect to the "ThoughtMachine" external system. The policy logic checks that the source of any connection to "ThoughtMachine" must be "VaultCoreClient", and any other source results in a denial message.

Suggestions:
- 1: To fix this deviation, modify the architecture so that the "MandateUpdateService" does not directly connect to "ThoughtMachine". Instead, ensure that all interactions with "ThoughtMachine" are routed through the "VaultCoreClient" adapter. This can be achieved by having "MandateUpdateService" call "VaultCoreClient" for any operations that require interaction with "ThoughtMachine", thereby adhering to the policy requirement.

---

### Compliant Policies

#### ARC-POLICY-101 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

Conclusion: The UML diagram complies with the provided OPA policy. All microservices (WebAPI, ServiceLayer, VaultCoreClient) are defined within a system boundary labeled "ecs", which satisfies the policy requirement that containers must be deployed in ECS Fargate.

---

#### ARC-POLICY-104 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

Conclusion: The UML diagram complies with the provided OPA policy. The container "VaultCoreClient" makes an external call to "ThoughtMachine" and is correctly annotated with the stereotype "uses_secret," which satisfies the policy requirement. There are no deviations from the policy logic, and no further action is needed.

---

#### ARC-POLICY-105 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy requires the architecture to include a data store related to audit or logging, specifically using PostgreSQL or RDS technology, or having a stereotype of "data_store". The UML diagram includes an "Audit Log" container with the technology "Amazon RDS PostgreSQL" and the stereotype "data_store", which satisfies the policy requirement. Therefore, there are no deviations from the policy, and no suggestions for changes are necessary.

---

#### ARC-POLICY-106 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the policy ARC-POLICY-106. The policy requires that at least one container must have 'secrets' in the name or be labeled with the stereotype <<secrets_store>>. The UML diagram includes a container named "AWS Secrets Manager" with the stereotype <<secrets_store>>, which satisfies the policy requirement. Therefore, there are no deviations, and the architecture is compliant.

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

