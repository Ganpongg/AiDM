# Product Requirements Document

> _AI-generated via LiteLLM (prd.md) — **unverified** until approved._

## 1. Document Summary and Product Vision

**Product:** Branch Operations Workbench (BOW)
**Version:** 1.0 — MVP PRD
**Status:** Draft for Review
**Source Evidence:** Project Brief §1–21 (frozen snapshot, authoritative); discovery answers (behavior, rollout-migration); guided planning selections (compliance: none, feature_scope: standard, success_metric: time-to-value).

**Vision:** Provide bank branch staff with a unified digital workbench to capture, track, approve, and hand off customer service requests — replacing paper checklists, multi-system switching, and informal tracking with a guided, auditable workflow.

**Delivery Target:** 3-month MVP; pilot in 3–5 branches for 8–12 weeks.

---

## 2. Problem Statement and Opportunity

Source: Brief §3, §2.

| Pain Point | Impact |
|---|---|
| Inconsistent request capture across branches | Variable customer experience |
| Multi-system switching for each service | Slow handling, repeated data entry |
| Paper checklists and manual follow-up | Errors, missing documents, rework |
| Limited supervisor real-time visibility | Delayed escalations, SLA breaches |
| No traceable approval/escalation history | Audit and compliance risk |

**Opportunity:** Digitizing the service-request lifecycle for 7 non-cash service types in pilot branches creates measurable time-to-value within the 3-month window and establishes a reusable platform for branch modernization.

---

## 3. Primary Users, Stakeholders, and User Needs

Source: Brief §8, §14.

| Role | Primary Need |
|---|---|
| Branch Frontline Staff | Create tickets, follow guided checklists, attach documents, update status |
| Branch Supervisor | Approve/reject exceptions, monitor queue, track SLA |
| Branch Manager | View workload, SLA, and daily performance dashboard |
| Operations Support | Access and update escalated/pending tickets |
| Compliance/Audit Reviewer | Read-only access to audit trail and approval evidence |
| System Administrator | Configure service types, templates, users, branch settings |

---

## 4. Goals, Success Metrics, and Non-Goals

### Goals (Source: Brief §5, §15)

| ID | Goal |
|---|---|
| G-1 | Reduce average service handling time |
| G-2 | Increase SLA completion rate in pilot branches |
| G-3 | Eliminate paper-based checklist and manual follow-up tracking |
| G-4 | Provide supervisors real-time queue and approval visibility |
| G-5 | Ensure full audit traceability for every service request |

### Success Metrics

| Metric | Target | Linked Goal |
|---|---|---|
| M-1: Avg. handling time | ≥20% reduction vs. pre-pilot baseline | G-1 |
| M-2: SLA completion rate | ≥80% of tickets within SLA for 4 consecutive pilot weeks | G-2 |
| M-3: Missing-document cases | ≥30% reduction vs. baseline | G-3 |
| M-4: Staff adoption rate | ≥85% of pilot staff using BOW as primary tool by week 4 | G-3 |
| M-5: Supervisor approval turnaround | ≤4 hours median (Assumption: no SLA defined in Brief) | G-4 |
| M-6: Audit record completeness | 100% of closed tickets have complete audit trail | G-5 |

**Go/No-Go for Expansion:** M-2 met for 4 consecutive weeks (source: discovery answer, rollout-migration).

### Non-Goals (Source: Brief §6 Out of Scope)

- Cash transaction processing or core banking ledger posting
- Loan approval decisioning
- Full CRM or document management system replacement
- Customer-facing mobile self-service
- AI-based sales recommendations
- Enterprise-wide rollout in MVP

---

## 5. User Personas and User Journeys

### Personas

**P-1 — Frontline Staff (Nong):** Handles 15–30 customers/day; needs fast ticket creation and clear checklist guidance; low tolerance for complex UI.

**P-2 — Branch Supervisor (Khun Somchai):** Approves exceptions, monitors queue; needs real-time visibility without leaving the floor.

**P-3 — Branch Manager (Khun Malee):** Reviews daily performance; needs summary dashboard, not individual ticket detail.

### Core Journey: Service Request Lifecycle (Source: Brief §9)

```
Customer Arrives → Staff Creates Ticket (P-1) → System Loads Checklist
→ Staff Completes Steps & Attaches Docs → Approval Required?
  ├─ No  → Staff Closes Ticket → Audit Event Recorded
  └─ Yes → Supervisor Reviews (P-2)
             ├─ Approved → Staff Closes Ticket
             └─ Rejected → Ticket returns to Staff as editable → Staff corrects & resubmits
```

Source for rejection flow: discovery answer (behavior).

---

## 6. Release Scope and Priorities

### MVP (Pilot Release — 3 months)

**Service Types Supported** (Source: Brief §7): Customer information update, debit card replacement, account statement request, bank certificate request, dormant account reactivation, customer complaint/service issue, general branch inquiry.

**Priority Tiers** (Assumption: no MoSCoW ranking in Brief; tiers assigned by delivery risk and G-1/G-2 alignment):

| Tier | Capability |
|---|---|
| P1 — Must Have | Service intake & ticket creation, guided checklist, approval workflow (incl. rejection-resubmit), audit trail, RBAC |
| P2 — Should Have | Document tracking, queue/assignment view, branch dashboard, request tracking & follow-up |
| P3 — Nice to Have | Supervisor workload summary, operations support escalation view, admin configuration UI |

### Post-MVP (Future Roadmap — Source: Brief §17)

Appointment booking, customer self-check-in, mobile workbench, AI guidance, automated document validation, SLA alerting, cross-branch analytics.

---

## 7. Functional Requirements

| ID | Requirement | Priority | Acceptance Notes | Linked Goal/Need |
|---|---|---|---|---|
| FR-001 | Staff can create a service ticket by selecting branch, service type, priority, and entering customer reference and contact info | P1 | Ticket persists with unique ID; all mandatory fields enforced before save | G-1, G-3, P-1 |
| FR-002 | System loads a service-type-specific guided checklist on ticket creation | P1 | Correct template loads within 2 s; mandatory items block completion if unchecked | G-1, G-3, P-1 |
| FR-003 | Staff can capture exception reasons when a mandatory checklist item cannot be completed | P1 | Exception reason is required text field; recorded in audit trail | G-5, P-1 |
| FR-004 | Staff can attach documents, mark them received/missing, and add notes per document | P2 | Attachment stored with ticket; document completeness status visible | G-3, P-1 |
| FR-005 | Queue view shows tickets by status (waiting, in-progress, pending, completed) with filters by status, service type, and owner | P2 | Filters apply within 1 s; waiting time and handling time displayed | G-4, P-1, P-2 |
| FR-006 | Tickets can be assigned and reassigned to available staff; priority can be updated | P2 | Reassignment logged in audit trail | G-4, P-2 |
| FR-007 | System routes ticket to supervisor approval queue when service type or exception requires it | P1 | Routing rule configurable per service type; supervisor notified (in-app) | G-4, G-5, P-2 |
| FR-008 | Supervisor can approve, reject, or request more information on a pending ticket, with mandatory comment | P1 | Decision recorded with timestamp and user ID; comment required for reject/RFI | G-4, G-5, P-2 |
| FR-009 | On rejection, ticket returns to originating staff as editable; staff can correct and resubmit | P1 | Status set to "Returned"; rejection comment visible to staff; resubmission creates new approval event | G-5, P-1, P-2 |
| FR-010 | Maker-checker separation enforced: approver cannot be the same user who created the ticket | P1 | System blocks self-approval; enforced server-side | G-5, Brief §10.5 |
| FR-011 | Staff and supervisors can view all open, pending, and escalated requests with status and SLA indicator | P2 | SLA breach visually flagged; escalated tickets visible to operations support role | G-2, G-4 |
| FR-012 | Branch dashboard displays: active ticket count, avg. wait/handling time, tickets by service type, pending approvals, overdue items, staff workload | P2 | Dashboard refreshes ≤60 s; accessible to supervisor and manager roles | G-4, M-2, P-3 |
| FR-013 | Every user action (create, update, status change, document attach, approval decision, closure) is recorded in an immutable audit trail | P1 | Audit events include user ID, timestamp, action type, before/after values; not editable by any role | G-5, M-6 |
| FR-014 | System administrator can create/edit service types, checklist templates, and branch user accounts | P3 | Changes to templates version-stamped; existing open tickets retain original template version | G-3, Brief §14 |
| FR-015 | Staff can reopen a closed ticket with a mandatory reason; reopening logged in audit trail | P2 | Only staff and supervisor roles can reopen; compliance reviewer cannot | G-5, Brief §10.6 |

---

## 8. Non-Functional Requirements

| ID | Requirement | Measurable Target | Linked Goal |
|---|---|---|---|
| NFR-001 | Page/screen load time | ≤2 seconds at P95 under pilot load (≤50 concurrent users) | G-1 |
| NFR-002 | Ticket save and status update response | ≤1 second at P95 | G-1 |
| NFR-003 | System availability during branch hours | ≥99.5% uptime Mon–Sat 07:00–20:00 local time | G-2 |
| NFR-004 | Role-based access control | Each role accesses only permitted screens and data; enforced server-side; verified by penetration test before pilot | G-5 |
| NFR-005 | Sensitive customer data masking | PII fields (ID number, phone, account ref) masked in UI except for authorized roles; masking rules documented | G-5, Brief §11 |
| NFR-006 | PDPA / data protection compliance | No customer PII stored beyond retention policy; Assumption: retention period = 7 years per banking norm (TBD: confirm with compliance) | G-5 |
| NFR-007 | Audit trail immutability | Audit records write-only; no update/delete API exposed; verified by security review | G-5 |
| NFR-008 | Graceful integration failure | If mock/real integration is unavailable, system degrades gracefully with user-visible error; ticket workflow continues offline-capable for non-integration steps | G-2 |
| NFR-009 | Usability | New staff can complete core ticket workflow with ≤30 min onboarding; validated by pilot UAT | G-1, M-4 |
| NFR-010 | Scalability | Architecture supports expansion to 50 branches and 500 concurrent users without redesign | Brief §11 |

---

## 9. Data, Integrations, and External Interfaces

### Core Data Objects (Source: Brief §12)

Branch, Branch User, Customer Reference, Service Ticket, Service Type, Checklist Template, Checklist Item, Document Attachment, Approval Request, Approval Decision, Comment, Audit Event, SLA Status, Follow-up Task.

### Integrations (Source: Brief §13)

| Integration | MVP Approach | Notes |
|---|---|---|
| Core banking customer profile lookup | Mock adapter / API-ready stub | Read-only; no financial posting |
| Identity & Access Management (IAM) | API-ready adapter; fallback to local auth | TBD: IAM system name |
| Document Management System | Mock; attachment stored in BOW for MVP | Future DMS integration post-MVP |
| SMS/Email notification service | Mock; in-app notification only for MVP | Customer-facing notifications post-MVP |
| Branch queue management system | Mock adapter | |
| Enterprise reporting platform | CSV export for MVP; API post-pilot | |
| CRM / customer case system | Out of scope MVP | |
| Jira / delivery tracking | Out of scope MVP | |

**Constraint:** BOW must not execute financial transactions or post to core banking ledger (Source: Brief §4, §6).

---

## 10. UX and Accessibility Requirements

| ID | Requirement |
|---|---|
| UX-001 | Web-based responsive UI; optimized for desktop branch workstations (1280×800 minimum) |
| UX-002 | Guided checklist presented as a step-by-step task list with clear completion indicators |
| UX-003 | Ticket status and SLA breach communicated via color coding and text labels (not color alone — accessibility) |
| UX-004 | Rejection reason and returned-ticket state surfaced prominently on staff workbench |
| UX-005 | All interactive elements keyboard-navigable; WCAG 2.1 AA compliance targeted (Assumption: no explicit standard mandated in Brief) |
| UX-006 | UI language: Assumption: Thai primary with English field labels; TBD: confirm with pilot branch stakeholders |

---

## 11. Analytics and Observability Requirements

| ID | Requirement |
|---|---|
| OBS-001 | Application logs capture all API requests, errors, and integration failures with correlation IDs |
| OBS-002 | Dashboard metrics (FR-012) sourced from live ticket data; refresh interval ≤60 seconds |
| OBS-003 | SLA breach events trigger in-app flag and are queryable for M-2 reporting |
| OBS-004 | Pilot KPI report (M-1 through M-6) exportable as CSV by branch manager and system admin |
| OBS-005 | Error rate and latency monitored; alert threshold: error rate >1% over 5-minute window |

---

## 12. Dependencies and Constraints

| Item | Detail |
|---|---|
| Timeline | 3-month MVP; non-negotiable per Brief §1 |
| Pilot scope | 3–5 branches; expansion gated on M-2 go/no-go criterion |
| Integration availability | Mock services acceptable for MVP; real APIs may not be available (Brief §13) |
| No financial execution | BOW must not post to core banking in any release phase of MVP |
| Feature flags | Assumption: feature-flag mechanism needed for phased pilot rollout; TBD: confirm tooling |
| Training | Assumption: ≤30 min onboarding per NFR-009; formal training plan TBD |
| Infrastructure | Assumption: cloud-hosted or on-premise bank datacenter; TBD: confirm deployment environment |

---

## 13. Risks and Mitigations

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R-01 | Core banking API unavailable for pilot | High | Medium | Use mock adapters; design API-ready stubs from day 1 |
| R-02 | Staff resistance to new workflow | Medium | High | Simple UI (NFR-009); involve pilot branch leads in UAT; measure M-4 weekly |
| R-03 | Scope creep — additional service types requested | High | Medium | Freeze service type list at Brief §7; change control required for additions |
| R-04 | PII data handling non-compliance | Low | High | Data masking (NFR-005), PDPA controls (NFR-006), security review before pilot |
| R-05 | Process variation across pilot branches | Medium | Medium | Configurable checklist templates (FR-014); document branch-specific exceptions |
| R-06 | SLA targets undefined per service type | Medium | Medium | Define per-service SLA in sprint 1 with operations team; placeholder = 1 business day |

---

## 14. Open Questions

| ID | Question | Owner | Blocking? |
|---|---|---|---|
| OQ-01 | Which specific branches join the pilot? | Branch Ops Lead | Yes — needed for UAT planning |
| OQ-02 | Per-service-type SLA targets (minutes/hours)? | Operations | Yes — needed for FR-011, OBS-003 |
| OQ-03 | Which approvals require maker-checker beyond exception cases? | Compliance | Yes — needed for FR-010 routing rules |
| OQ-04 | Customer data fields permitted for display to staff? | Compliance / Legal | Yes — needed for FR-001, NFR-005 |
| OQ-05 | Deployment environment (cloud vs. on-premise)? | IT Infrastructure | Yes — needed for NFR-003, NFR-010 |
| OQ-06 | UI language(s) for pilot? | Product / Branch Ops | No — default assumption Thai+English |
| OQ-07 | Customer SMS/email notification in pilot scope? | Product | No — assumed out of scope MVP |
| OQ-08 | Data retention period confirmation with compliance? | Legal / Compliance | No — assumed 7 years |
| OQ-09 | Feature flag tooling available? | Engineering | No — needed before sprint 1 |

---

## 15. Requirements Traceability

| Requirement | Type | Priority | Linked Goals | Source Evidence |
|---|---|---|---|---|
| FR-001 | Functional | P1 | G-1, G-3 | Brief §10.1 |
| FR-002 | Functional | P1 | G-1, G-3 | Brief §10.3 |
| FR-003 | Functional | P1 | G-5 | Brief §10.3 |
| FR-004 | Functional | P2 | G-3 | Brief §10.4 |
| FR-005 | Functional | P2 | G-4 | Brief §10.2 |
| FR-006 | Functional | P2 | G-4 | Brief §10.2 |
| FR-007 | Functional | P1 | G-4, G-5 | Brief §10.5 |
| FR-008 | Functional | P1 | G-4, G-5 | Brief §10.5 |
| FR-009 | Functional | P1 | G-5 | Discovery answer: behavior |
| FR-010 | Functional | P1 | G-5 | Brief §10.5 |
| FR-011 | Functional | P2 | G-2, G-4 | Brief §10.6 |
| FR-012 | Functional | P2 | G-4 | Brief §10.7 |
| FR-013 | Functional | P1 | G-5 | Brief §10.8 |
| FR-014 | Functional | P3 | G-3 | Brief §14 |
| FR-015 | Functional | P2 | G-5 | Brief §10.6 |
| NFR-001 | Non-Functional | P1 | G-1 | Brief §11 Performance |
| NFR-002 | Non-Functional | P1 | G-1 | Brief §11 Performance |
| NFR-003 | Non-Functional | P1 | G-2 | Brief §11 Availability |
| NFR-004 | Non-Functional | P1 | G-5 | Brief §11 Security |
| NFR-005 | Non-Functional | P1 | G-5 | Brief §11 Security |
| NFR-006 | Non-Functional | P1 | G-5 | Brief §11 Compliance |
| NFR-007 | Non-Functional | P1 | G-5 | Brief §10.8 |
| NFR-008 | Non-Functional | P2 | G-2 | Brief §11 Availability |
| NFR-009 | Non-Functional | P2 | G-1 | Brief §11 Usability |
| NFR-010 | Non-Functional | P3 | G-2 | Brief §11 Scalability |
| M-2 Go/No-Go | Rollout Gate | — | G-2 | Discovery answer: rollout-migration |
