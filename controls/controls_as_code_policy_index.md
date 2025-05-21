
# ✅ Controls as Code (CaC) – Policy Index

This document captures the full list of **Controls as Code** implemented (or planned) to enforce secure, modular, and compliant software delivery for the **Direct Debit Mandate Update Microservice**.

---

## 🔐 Security Controls (`SEC-`)

| ID      | Policy                                                              | Purpose                                      |
| ------- | ------------------------------------------------------------------- | -------------------------------------------- |
| SEC-001 | **All REST endpoints must require authentication**                  | Prevent unauthorized access                  |
| SEC-002 | **No @PermitAll or unsecured /api/** paths in Spring Security**     | Avoid accidental exposure                    |
| SEC-003 | **Secrets must not be hardcoded in code or config**                 | Ensure AWS Secrets Manager is used           |
| SEC-004 | **OAuth2 clients must not bypass token validation**                 | Enforce proper token handling for Vault Core |
| SEC-005 | **Mandatory logging of all failed login or API attempts**           | Support audit trail requirements             |
| SEC-006 | **Cross-Origin Resource Sharing (CORS) must be restricted**         | Prevent CORS abuse in production             |

---

## 🧱 Architecture Controls (`ARC-`)

| ID      | Policy                                                                           | Purpose                                                            |
| ------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| ARC-001 | **DTOs must be used for all controller inputs/outputs**                          | Prevent leaking JPA entities                                       |
| ARC-002 | **Repositories must not be injected into controllers**                           | Enforce service layer abstraction                                  |
| ARC-003 | **Domain entities must not depend on controller or DTO packages**                | Enforce clean hexagonal layering                                   |
| ARC-004 | **All exceptions must be handled via @ControllerAdvice**                         | Avoid scattered error handling                                     |
| ARC-005 | **Use constructor injection, not field injection**                               | Improve testability and immutability                               |
| ARC-006 | **Each REST controller must be annotated with @RequestMapping("/api/v1/...")**   | Enforce versioning                                                 |
| ARC-007 | **All classes must belong to allowed package namespaces**                        | Enforce modular design (e.g., com.mycompany.directdebitupdate.*)   |

---

## 🏗 Infrastructure Controls (`INFRA-`)

| ID        | Policy                                                                  | Purpose                              |
| --------- | ----------------------------------------------------------------------- | ------------------------------------ |
| INFRA-001 | **Fargate tasks must use latest approved image tag (e.g., :stable)**    | Avoid drift or old images            |
| INFRA-002 | **API Gateway must use HTTPS-only endpoints**                           | Prevent insecure communication       |
| INFRA-003 | **Audit logs must be stored in encrypted RDS**                          | Enforce data at rest protection      |
| INFRA-004 | **Secrets Manager must store DB and API credentials**                   | Prevent plaintext secrets in configs |
| INFRA-005 | **CloudWatch must capture logs and custom metrics**                     | Enable observability and tracing     |
| INFRA-006 | **Terraform plans must pass tfsec checks with no HIGH/Critical issues** | Enforce IaC compliance               |

---

Each control will be mapped to its implementation and enforcement test in `/controls/{security|architecture|infra}/` folders.  
Waiver exceptions and expirations will be tracked in `/adr/waivers/`.
