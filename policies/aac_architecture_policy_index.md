
# ✅ Architecture Guardrail Policies (AAC Series)

This document defines a set of **Architecture as Code (AaC)** policies for validating PlantUML architecture diagrams and aligning them to agreed governance and cloud-native design patterns.

---

| **ID**      | **Policy Description**                                                                                      | **Intent / Reasoning**                                                        |
| ----------- | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **ARC-POLICY-101-control** | All microservices must be annotated as `<<fargate>>` or reside in a `System_Boundary` named for Fargate     | Enforces serverless/containerized runtime alignment with AWS strategy         |
| **ARC-POLICY-102-control** | All external clients (e.g., CRM, portals) must interact through a defined `<<api_gateway>>` container       | Prevents direct backend access; supports throttling, auth, monitoring         |
| **ARC-POLICY-103-control** | Thought Machine Vault Core must only be accessed via a named adapter container                              | Prevents tight coupling to external APIs and promotes testability/abstraction |
| **ARC-POLICY-104-control** | All containers that make external calls must be annotated `<<uses_secret>>`                                 | Ensures credentials are injected and tracked                                  |
| **ARC-POLICY-105-control** | No containers may hardcode credentials (validated via source or annotation in `.puml`)                      | Prevents insecure practices                                                   |
| **ARC-POLICY-106-control** | A `Secrets Manager` or `Parameter Store` dependency must be declared explicitly in the architecture         | Makes secret source auditable and enforces runtime access policy              |
| **ARC-POLICY-107-control** | All stateful services must store logs or data in defined data store containers                              | Ensures auditability, log retention, and persistence boundaries               |
| **ARC-POLICY-108-control** | PlantUML diagrams must include a `<<observability>>` container or mention CloudWatch                        | Guarantees operational readiness                                              |
| **ARC-POLICY-109-control** | A `System_Boundary` must contain at least one controller and service pair (`<<controller>>`, `<<service>>`) | Enforces layered domain logic inside services                                 |
| **ARC-POLICY-110-control** | Each architecture diagram must include a `legend` and `skinparam` block                                     | Ensures diagram is understandable, themed, and clean for compliance readers   |

---

Each policy has a corresponding Rego file, test input, and CI enforcement path inside the `/policies` directory.

Policies are traceable to Architecture Decision Records (ADRs) where applicable.
