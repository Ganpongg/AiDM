# Epics & User Stories Backlog

> _AI-generated via LiteLLM (backlog.md) — **unverified** until approved._

## 1. Planning Assumptions

| ID | Assumption / Gap |
|----|-----------------|
| A-01 | Sprint duration: 2 weeks. Velocity assumed 30–35 story points per sprint (pilot team ~4 devs + 1 QA). |
| A-02 | Per-service SLA defaults to 1 business day (OQ-02 open; update routing rules when resolved). |
| A-03 | Maker-checker applies to all approval decisions plus exception-checklist submissions (OQ-03 open). |
| A-04 | PII-visible roles: SUPERVISOR, MANAGER, ADMIN only; STAFF sees masked ID/phone (OQ-04 open). |
| A-05 | Deployment target: OpenShift (bank private cloud); Docker Compose for DEV (OQ-05 open). |
| A-06 | UI language: Thai primary, English field labels (OQ-06 non-blocking). |
| A-07 | Feature flags via `feature_flags` DB table; no external flag service for MVP. |
| A-08 | Greenfield — no legacy data migration required. |
| A-09 | Sprint 1–2 demonstrable increment: staff can create a ticket and complete a guided checklist (FR-001, FR-002, FR-003). |
| A-10 | IAM falls back to local Spring Security store for MVP; real adapter swapped pre-enterprise rollout. |

---

## 2. Epic Sequence and Dependency Map

```
EPIC-01 (Foundation & RBAC)
  └─► EPIC-02 (Service Intake & Checklist)   ← Sprint 1–2 increment
        └─► EPIC-03 (Approval Workflow)
              └─► EPIC-04 (Document Tracking)
              └─► EPIC-05 (Queue & Assignment)
                    └─► EPIC-06 (Request Tracking & Dashboard)
                          └─► EPIC-07 (Admin Configuration)
                          └─► EPIC-08 (Quality, Security & Pilot Readiness)
```

**Critical path:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-06 → EPIC-08 (pilot go-live gate).

---

## 3. Epics and User Stories

### EPIC-01 — Foundation, RBAC & Audit Infrastructure
**Outcome:** Secure, deployable skeleton with role enforcement and immutable audit trail enabling all subsequent epics.
**Priority:** Must Have | **Sprints:** 1–2

| Story | Title | As a / I want / So that | Pri | Pts | Depends | Technical Notes |
|-------|-------|------------------------|-----|-----|---------|-----------------|
| US-001 | Project scaffold & CI/CD | Dev / scaffold Spring Boot 3.x modular monolith with Flyway, HikariCP, Testcontainers, bank CI pipeline / so that all modules build and deploy consistently | Must | 5 | — | AD-01; Docker Compose DEV; OpenShift SIT manifest |
| US-002 | Core schema migration | Dev / apply Flyway V1 migration for all core tables / so that data model is version-controlled from day 1 | Must | 3 | US-001 | Arch §6 tables; indexes on `service_ticket(branch_id,status)`, `sla_due_at`, `audit_event(ticket_id,occurred_at)` |
| US-003 | RBAC — role model & JWT auth | Staff / authenticate with credentials and receive a JWT / so that only authorised users access BOW | Must | 5 | US-001 | Spring Security; local store (A-10); JWT ≤8 h expiry; `@PreAuthorize` on service layer (AD-05) |
| US-004 | RBAC — role-based screen access | Compliance Reviewer / access only audit and read-only screens / so that no write actions are available to my role | Must | 3 | US-003 | All 6 roles × all modules; security test suite (Arch §12) |
| US-005 | Immutable audit event writer | System / append an audit event on every state-changing action / so that the audit trail is complete and tamper-proof | Must | 5 | US-002, US-003 | `bow_audit_writer` DB role INSERT-only (AD-06); `before_state`/`after_state` JSONB; correlation ID via MDC (OBS-001) |
| US-006 | PII masking by role | Staff / see customer ID and phone masked in UI and API response / so that PII is not over-exposed | Must | 3 | US-003, US-004 | Role-filtered DTO projections (AD-07); A-04 masking rules |

**Acceptance Criteria (representative — US-005):**
- **Given** a staff user updates ticket status, **When** the update is committed, **Then** an `audit_event` row is inserted with correct `user_id`, `action_type`, `before_state`, `after_state`, and `occurred_at`; no UPDATE or DELETE is possible via any API or app role.

---

### EPIC-02 — Service Intake & Guided Checklist
**Outcome:** Staff can create a ticket and complete a guided, service-specific checklist — Sprint 1–2 demonstrable increment.
**Priority:** Must Have | **Sprints:** 1–2

| Story | Title | As a / I want / So that | Pri | Pts | Depends | Technical Notes |
|-------|-------|------------------------|-----|-----|---------|-----------------|
| US-010 | Create service ticket (happy path) | Branch Staff / create a ticket by selecting branch, service type, priority, and entering customer reference / so that the request is captured with a unique ID | Must | 5 | US-002, US-003 | `POST /api/tickets`; mandatory fields enforced server-side; FR-001 |
| US-011 | Customer lookup via CBS mock | Branch Staff / search for a customer by reference and auto-populate contact fields / so that I avoid manual re-entry | Must | 3 | US-010 | `CoreBankingAdapter` mock (AD-04); graceful fallback if unavailable (NFR-008) |
| US-012 | Ticket creation — validation errors | Branch Staff / see clear field-level errors when mandatory fields are missing / so that I can correct and resubmit without losing data | Must | 2 | US-010 | FR-001 edge case; client + server validation |
| US-013 | Load guided checklist on ticket creation | Branch Staff / see the correct service-type checklist automatically loaded / so that I follow the right steps without searching | Must | 5 | US-010, US-002 | `GET /api/tickets/{id}/checklist`; template loads ≤2 s (NFR-001); FR-002 |
| US-014 | Complete checklist item | Branch Staff / mark each checklist item complete / so that progress is tracked and mandatory items gate ticket closure | Must | 3 | US-013 | `PATCH /api/tickets/{id}/checklist-items/{itemId}`; mandatory items block completion; FR-002 |
| US-015 | Capture exception reason | Branch Staff / enter a mandatory exception reason when I cannot complete a checklist item / so that the deviation is recorded in the audit trail | Must | 3 | US-014, US-005 | FR-003; exception reason required text; audit event written; happy-path US-014 first |
| US-016 | Checklist completion — missing mandatory items | Branch Staff / be blocked from closing a ticket with unchecked mandatory items unless an exception reason is provided / so that compliance is enforced | Must | 2 | US-015 | FR-002/003 edge case |

**Acceptance Criteria (US-013):**
- **Given** a staff user creates a ticket for service type "Debit Card Replacement", **When** the ticket is saved, **Then** the correct checklist template version loads within 2 seconds and all mandatory items are marked as required.

**Acceptance Criteria (US-015):**
- **Given** a mandatory checklist item is unchecked, **When** staff submits an exception reason, **Then** the reason is saved, an audit event is recorded, and the item is marked as exception-captured.

---

### EPIC-03 — Approval Workflow & Maker-Checker
**Outcome:** Supervisors can approve, reject, or request information; rejected tickets return to staff for correction and resubmission; maker-checker enforced.
**Priority:** Must Have | **Sprints:** 3–4

| Story | Title | As a / I want / So that | Pri | Pts | Depends | Technical Notes |
|-------|-------|------------------------|-----|-----|---------|-----------------|
| US-020 | Route ticket to approval queue | System / route a ticket to the supervisor approval queue when the service type or exception requires it / so that no controlled action bypasses review | Must | 5 | US-013, US-003 | `POST /api/tickets/{id}/submit-approval`; routing rule per `service_type.approval_required`; in-app notification; FR-007 |
| US-021 | Supervisor approves ticket | Branch Supervisor / approve a pending ticket with a mandatory comment / so that the decision is recorded with my identity and timestamp | Must | 3 | US-020 | `POST /api/approvals/{id}/decide`; action=APPROVED; FR-008 |
| US-022 | Supervisor rejects ticket | Branch Supervisor / reject a ticket with a mandatory comment / so that staff know exactly what to correct | Must | 3 | US-020 | action=REJECTED; ticket status → RETURNED; FR-008/009 |
| US-023 | Supervisor requests more information | Branch Supervisor / request more information on a ticket / so that I can defer decision until staff provide clarification | Must | 2 | US-020 | action=RFI; FR-008 |
| US-024 | Staff corrects and resubmits rejected ticket | Branch Staff / edit a returned ticket and resubmit for approval / so that the request can proceed without creating a duplicate | Must | 3 | US-022 | Status RETURNED → editable; resubmission creates new `approval_request`; rejection comment visible; FR-009 |
| US-025 | Maker-checker enforcement | System / block an approver from approving their own ticket / so that self-approval fraud is prevented | Must | 3 | US-021, US-022 | Server-side: `ticket.created_by ≠ approver`; FR-010; security test required |
| US-026 | Approval — edge cases (self-approval attempt) | Branch Staff / receive a clear error if I attempt to approve my own ticket / so that I understand the constraint | Must | 1 | US-025 | FR-010 edge case |

**Acceptance Criteria (US-025):**
- **Given** a staff user created ticket T-001, **When** the same user attempts to approve T-001, **Then** the server returns HTTP 403 with error code `SELF_APPROVAL_FORBIDDEN` and no approval record is created.

**Acceptance Criteria (US-024):**
- **Given** ticket T-001 is in RETURNED status with a rejection comment, **When** staff edits and resubmits, **Then** a new `approval_request` is created, the previous rejection comment remains visible, and an audit event records the resubmission.

---

### EPIC-04 — Document Tracking
**Outcome:** Staff can attach, mark, and track required documents per ticket.
**Priority:** Should Have | **Sprints:** 3–4

| Story | Title | As a / I want / So that | Pri | Pts | Depends | Technical Notes |
|-------|-------|------------------------|-----|-----|---------|-----------------|
| US-030 | Attach document to ticket | Branch Staff / attach a document file to a ticket and specify document type / so that required evidence is captured digitally | Should | 3 | US-010, US-002 | `POST /api/tickets/{id}/documents`; stored in BOW (mock DMS); FR-004 |
| US-031 | Mark document received or missing | Branch Staff / mark each required document as received or missing with a note / so that document completeness is visible at a glance | Should | 2 | US-030 | Status: RECEIVED/MISSING; FR-004 |
| US-032 | Document completeness status | Branch Supervisor / see document completeness status on a ticket / so that I can make an informed approval decision | Should | 2 | US-031 | Read-only view; FR-004 |

**Acceptance Criteria (US-031):**
- **Given** a ticket requires a national ID copy, **When** staff marks it MISSING with a note, **Then** the document status is saved, visible on the ticket detail, and an audit event is recorded.

---

### EPIC-05 — Queue & Assignment
**Outcome:** Staff and supervisors can view, filter, assign, and reassign tickets across the branch queue.
**Priority:** Should Have | **Sprints:** 3–4

| Story | Title | As a / I want / So that | Pri | Pts | Depends | Technical Notes |
|-------|-------|------------------------|-----|-----|---------|-----------------|
| US-040 | Queue view with status filters | Branch Staff / view all tickets filtered by status, service type, and owner / so that I can prioritise my work | Should | 5 | US-010, US-003 | `GET /api/tickets`; filters apply ≤1 s (NFR-002); waiting/handling time displayed; FR-005 |
| US-041 | Assign ticket to staff | Branch Supervisor / assign a ticket to an available staff member / so that workload is distributed | Should | 3 | US-040 | `PATCH /api/tickets/{id}/assignment`; logged in audit trail; FR-006 |
| US-042 | Reassign ticket | Branch Supervisor / reassign a ticket to a different staff member / so that coverage gaps are handled | Should | 2 | US-041 | FR-006 edge case; audit event written |
| US-043 | Update ticket priority | Branch Supervisor / change the priority of a ticket / so that urgent cases are handled first | Should | 2 | US-040 | FR-006; priority change logged |

**Acceptance Criteria (US-040):**
- **Given** a supervisor applies filter status=PENDING_APPROVAL, **When** the filter is submitted, **Then** only tickets in PENDING_APPROVAL status are returned within 1 second, with waiting time and handling time displayed.

---

### EPIC-06 — Request Tracking, Dashboard & Reporting
**Outcome:** Managers and supervisors have real-time visibility into queue health, SLA status, and pilot KPIs.
**Priority:** Should Have | **Sprints:** 5–6

| Story | Title | As a / I want / So that | Pri | Pts | Depends | Technical Notes |
|-------|-------|------------------------|-----|-----|---------|-----------------|
| US-050 | Open/pending/escalated request view | Branch Staff / view all my open, pending, and escalated requests with SLA indicator / so that I never miss a follow-up | Should | 3 | US-040, US-020 | FR-011; SLA breach visually flagged; OPS_SUPPORT sees escalated tickets |
| US-051 | SLA breach flagging | System / flag a ticket as SLA-breached when `sla_due_at` passes / so that supervisors can act immediately | Should | 3 | US-002, US-050 | Background job every 5 min; `sla_breached=true`; OBS-003; FR-011 |
| US-052 | Branch dashboard | Branch Manager / view active ticket count, avg wait/handling time, tickets by service type, pending approvals, and overdue items / so that I can manage branch performance | Should | 5 | US-050, US-051 | `GET /api/dashboard/summary`; materialized view refresh ≤60 s; FR-012; OBS-002 |
| US-053 | Staff workload summary | Branch Supervisor / see per-staff ticket counts on the dashboard / so that I can rebalance workload | Should | 2 | US-052 | FR-012 sub-feature |
| US-054 | KPI CSV export | Branch Manager / export M-1–M-6 KPI data as CSV / so that I can report pilot performance to leadership | Should | 3 | US-052 | `GET /api/reports/kpi.csv`; roles: MANAGER, ADMIN; OBS-004 |
| US-055 | Reopen closed ticket | Branch Staff / reopen a closed ticket with a mandatory reason / so that additional customer needs are handled without creating duplicates | Should | 2 | US-010, US-005 | `POST /api/tickets/{id}/reopen`; COMPLIANCE role cannot reopen; FR-015 |

**Acceptance Criteria (US-052):**
- **Given** a branch manager views the dashboard, **When** the page loads, **Then** active ticket count, avg wait time, tickets by service type, pending approvals, and overdue items are displayed with data no older than 60 seconds.

**Acceptance Criteria (US-051):**
- **Given** a ticket's `sla_due_at` has passed, **When** the SLA background job runs, **Then** `sla_breached` is set to true and the ticket is visually flagged in the queue view within the next job cycle (≤5 min).

---

### EPIC-07 — Admin Configuration
**Outcome:** System administrators can manage service types, checklist templates, and branch users without code changes.
**Priority:** Could Have | **Sprints:** 5–6

| Story | Title | As a / I want / So that | Pri | Pts | Depends | Technical Notes |
|-------|-------|------------------------|-----|-----|---------|-----------------|
| US-060 | Manage service types | System Admin / create and edit service types with SLA and approval-required flag / so that new services can be onboarded without deployment | Could | 3 | US-002, US-003 | FR-014; changes version-stamped |
| US-061 | Manage checklist templates | System Admin / create and version checklist templates per service type / so that open tickets retain their original template version | Could | 5 | US-060 | FR-014; `effective_from` versioning; open tickets pinned to `template_version` |
| US-062 | Manage branch users | System Admin / create and deactivate branch user accounts with role assignment / so that access is controlled without IT tickets | Could | 3 | US-003 | FR-014; role: ADMIN only |

**Acceptance Criteria (US-061):**
- **Given** an admin publishes a new checklist template version for "Account Statement Request", **When** an existing open ticket was created under the previous version, **Then** the open ticket still displays the original template version and new tickets use the new version.

---

### EPIC-08 — Quality, Security & Pilot Readiness
**Outcome:** System passes penetration test, performance test, and UAT; pilot branches can go live.
**Priority:** Must Have (gate) | **Sprints:** 5–6 + pre-pilot

| Story | Title | As a / I want / So that | Pri | Pts | Depends | Technical Notes |
|-------|-------|------------------------|-----|-----|---------|-----------------|
| US-070 | Performance test — P95 latency | QA / run Gatling load test at 50 concurrent users / so that NFR-001 (≤2 s) and NFR-002 (≤1 s) are verified before pilot | Must | 3 | All EPIC-02–06 | Arch §12; Gatling in SIT environment |
| US-071 | Penetration test — RBAC & audit | Security Team / conduct pen test on RBAC, audit immutability, and transport security / so that NFR-004/007 are verified before PROD | Must | 3 | US-003, US-005, US-006 | Pre-PROD gate; bank security team; TLS 1.2+ |
| US-072 | UAT — pilot branch staff onboarding | Pilot Branch Staff / complete the core ticket workflow with ≤30 min onboarding / so that NFR-009 is validated | Must | 3 | All EPIC-02–03 | Guided test scripts; M-4 baseline capture |
| US-073 | Observability & alerting setup | Ops / configure error-rate alert (>1%/5 min) and health endpoints / so that production issues are detected immediately | Must | 2 | US-001 | OBS-005; `/actuator/health`; Prometheus/Grafana or bank equivalent |
| US-074 | Feature flag configuration | Dev / enable/disable features via `feature_flags` table without redeployment / so that phased pilot rollout is controlled | Must | 2 | US-002 | A-07; Arch §13 rollback strategy |

---

## 4. Cross-Cutting Enablers

| Enabler | Stories | Notes |
|---------|---------|-------|
| Correlation ID propagation | All API stories | `X-Correlation-ID` header; MDC in Logback JSON (OBS-001) |
| Graceful integration degradation | US-011, US-020 | Resilience4j circuit-breaker on all adapters (NFR-008, AD-04) |
| Flyway migration discipline | All DB stories | Rollback script required per migration before merge (Arch §13) |
| Blue/green rollback | US-001, US-074 | OpenShift route weight shift; feature flags as secondary control |
| PDPA retention job | US-002, US-005 | Scheduled purge after 7-year retention; `archived_at` soft-delete (NFR-006) |

---

## 5. Suggested Release and Sprint Plan

| Sprint | Stories | Increment / Goal |
|--------|---------|-----------------|
| S1 | US-001, US-002, US-003, US-004, US-005, US-006 | EPIC-01 complete; secure deployable skeleton |
| S2 | US-010, US-011, US-012, US-013, US-014, US-015, US-016 | **Demo:** Staff creates ticket + completes guided checklist (FR-001/002/003) |
| S3 | US-020, US-021, US-022, US-023, US-024, US-025, US-026 | Approval workflow + maker-checker live |
| S4 | US-030, US-031, US-032, US-040, US-041, US-042, US-043 | Document tracking + queue/assignment |
| S5 | US-050, US-051, US-052, US-053, US-054, US-055, US-060 | Tracking, dashboard, KPI export, admin (partial) |
| S6 | US-061, US-062, US-070, US-071, US-072, US-073, US-074 | Admin complete; pen test; perf test; UAT → **Pilot Go-Live** |

**M-2 Go/No-Go gate:** ≥80% SLA completion for 4 consecutive pilot weeks before branch expansion (PRD §4).

---

## 6. Definition of Ready

A story is ready for sprint planning when:
1. Acceptance criteria written in Given/When/Then format.
2. All upstream dependencies (story IDs) are Done or in the same sprint.
3. Open questions blocking the story are resolved (OQ-02, OQ-03, OQ-04 flagged per story).
4. UI mockup or API contract available (or explicitly waived).
5. Estimate agreed by team (Planning Poker or equivalent).
6. Technical notes reviewed by at least one developer.

---

## 7. Definition of Done

Every story must satisfy all of the following before acceptance:
1. Code peer-reviewed and merged to main branch.
2. Unit test coverage ≥80% for new/changed code (JUnit 5 / Mockito).
3. Integration tests pass in SIT (Spring Boot Test + Testcontainers).
4. RBAC enforcement verified: correct roles can access, incorrect roles receive 403.
5. Audit trail verified: all state-changing actions produce correct `audit_event` rows.
6. PII masking verified for applicable stories.
7. No critical/high findings from static analysis (SonarQube or equivalent).
8. SIT environment deployment successful; smoke test passed.
9. SIT sign-off from QA lead.
10. Acceptance criteria scenarios demonstrated and signed off by Product Owner.

---

## 8. Requirements Coverage Matrix

| Requirement | Priority | Covered By | Status |
|-------------|----------|-----------|--------|
| FR-001 | P1 | US-010, US-012 | ✅ |
| FR-002 | P1 | US-013, US-014, US-016 | ✅ |
| FR-003 | P1 | US-015, US-016 | ✅ |
| FR-004 | P2 | US-030, US-031, US-032 | ✅ |
| FR-005 | P2 | US-040 | ✅ |
| FR-006 | P2 | US-041, US-042, US-043 | ✅ |
| FR-007 | P1 | US-020 | ✅ |
| FR-008 | P1 | US-021, US-022, US-023 | ✅ |
| FR-009 | P1 | US-024 | ✅ |
| FR-010 | P1 | US-025, US-026 | ✅ |
| FR-011 | P2 | US-050, US-051 | ✅ |
| FR-012 | P2 | US-052, US-053 | ✅ |
| FR-013 | P1 | US-005 (cross-cutting) | ✅ |
| FR-014 | P3 | US-060, US-061, US-062 | ✅ |
| FR-015 | P2 | US-055 | ✅ |
| NFR-001 | P1 | US-070 (perf test) | ✅ |
| NFR-002 | P1 | US-040, US-070 | ✅ |
| NFR-003 | P1 | US-001, US-073 | ✅ |
| NFR-004 | P1 | US-003, US-004, US-071 | ✅ |
| NFR-005 | P1 | US-006, US-071 | ✅ |
| NFR-006 | P1 | US-002, US-005 (PDPA job) | ✅ |
| NFR-007 | P1 | US-005, US-071 | ✅ |
| NFR-008 | P2 | US-011, US-020 (circuit-breaker) | ✅ |
| NFR-009 | P2 | US-072 (UAT) | ✅ |
| NFR-010 | P3 | US-001 (stateless design) | ✅ |
| OBS-001 | — | US-001, US-005 | ✅ |
| OBS-002 | — | US-052 | ✅ |
| OBS-003 | — | US-051 | ✅ |
| OBS-004 | — | US-054 | ✅ |
| OBS-005 | — | US-073 | ✅ |
| M-2 Go/No-Go | Gate | US-051, US-052, US-054 | ✅ |
| UX-001–006 | — | US-013, US-016, US-024 (UI notes) | ⚠️ Partial — full UX review in UAT (US-072) |

**Uncovered / Flagged:**
- OQ-02 (per-service SLA values): US-051 uses 1-day default (A-02); update when resolved.
- OQ-03 (maker-checker scope): US-025 uses A-03; expand routing rules when compliance confirms.
- OQ-04 (PII display rules): US-006 uses A-04; update masking config when legal confirms.

---

## 9. Delivery Risks

| ID | Risk | Likelihood | Impact | Linked PRD Risk | Mitigation |
|----|------|-----------|--------|-----------------|------------|
| DR-01 | CBS mock not replaced before pilot — customer lookup always mocked | High | Medium | R-01 | US-011 uses adapter pattern (AD-04); real swap is config-only; track CBS API readiness weekly |
| DR-02 | OQ-02/03/04 unresolved by Sprint 3 — blocks approval routing and PII config | Medium | High | R-05 | Escalate to Product Owner by end of Sprint 2; use assumptions A-02/03/04 as interim; flag in sprint review |
| DR-03 | Staff resistance reduces M-4 adoption below 85% | Medium | High | R-02 | UAT in Sprint 6 (US-072); involve pilot branch leads from Sprint 3 demos; measure weekly |
| DR-04 | Pen test findings require rework post-Sprint 6 | Medium | High | R-04 | Security stories (US-003–006) built-in from Sprint 1; pre-pen-test security review in Sprint 5 |
| DR-05 | Scope creep — additional service types requested before pilot | High | Medium | R-03 | Service type list frozen at PRD §6; US-060/061 admin UI enables additions post-pilot via change control |
| DR-06 | IAM integration unavailable — local auth store used in PROD | Medium | Medium | TD-02 | A-10 fallback designed in; flag as must-replace before enterprise rollout |
| DR-07 | Sprint velocity lower than assumed (A-01) — S5/S6 stories slip | Medium | Medium | — | P3 stories (US-060–062) are Could Have; descope to post-pilot if velocity drops; P1/P2 stories protected |
