# Software Requirements Specification — Library Management Reporting & Operations

*Generated 2026-10-20 by the ReqNet agentic network from 20 source documents. Status: not fully approved — see §8.*

## Contents

- 1. Introduction
- 2. Priority Scale
- 3. Source Documents
- 4. Glossary
- 5. Requirements
- 6. Discarded Requirements (Blacklist)
- 7. Traceability Matrix
- 8. Quality Assurance Record

## 1. Introduction

This document consolidates the requirements for **Library Management Reporting & Operations** stated across a corpus of heterogeneous sources (emails, meeting minutes, interviews, surveys, draft specifications). 580 candidate statements were extracted; they were deduplicated, checked for conflicts and consolidated into **218 requirements** in 13 functional areas. Discarded candidates (18) are recorded with a justification in §6.

Each requirement has a unique identifier `REQ-<AREA>-<NNN>`, a short name, a descriptive paragraph, a type, a priority (§2) and the list of source documents it was derived from (§3, §7). Requirements are ordered by priority within each area. The key word *shall* denotes a mandatory capability.

| Area | Name | Requirements |
|---|---|---|
| AUTH | Authentication & Staff Login | 4 |
| ROLE | Authorization, Permissions & Admin Scope Control | 12 |
| UIXT | Web App UI, Help & Accessibility | 8 |
| DATAQ | Query Builder, Filters & Candidate Selection Engine | 21 |
| RPTMG | Report Templates, Scheduling, Queue & Outputs | 38 |
| ANALY | Analytical Reporting & Reporting Dimensions | 19 |
| LOCAP | Location & Consortium Multi-Location Reporting | 17 |
| OPMIS | OP Operations: Item Transfer, Revert & Transit Management | 14 |
| PURGE | Purge/Weeding & Deletion Utilities | 10 |
| ACCT | Finance & Transaction Reporting (Fines/Payments/Accounting) | 12 |
| CALCD | Collections, Circulation & Capacity/Inventory Analytics | 20 |
| STKID | Patron Analytics & Demographic/Inactivity Reporting | 17 |
| NFRQA | Non-Functional Constraints & Platform/Deployment/Compliance | 26 |

## 2. Priority Scale

| Priority | Meaning | Criteria |
|---|---|---|
| **P1** | Critical (Must have) | The system is not acceptable without it: explicitly marked high priority or mandatory in the sources, a hard technical/legal constraint, or demanded consistently by many stakeholders (e.g. a large share of survey respondents). |
| **P2** | High (Should have) | Important for daily work of a significant user group and requested in more than one source, but a temporary workaround exists. |
| **P3** | Medium (Could have) | Useful improvement requested by a single group or source; can be delivered in a later increment without blocking core use. |
| **P4** | Low (Nice to have) | Convenience, cosmetic or speculative wish with weak evidence of need; candidate for future releases. |

Distribution: P1: 41, P2: 95, P3: 80, P4: 2.

## 3. Source Documents

| ID | File | Type | Date | Title |
|---|---|---|---|---|
| DOC-01 | `conversations/conv_pines014_material_volume.eml` | email thread | 2009-04-06 | Volume reporting - how do we count what we have? |
| DOC-02 | `conversations/conv_pines015_capacity_interface.eml` | email thread | 2009-04-08 | Can we see all branches at once? |
| DOC-03 | `conversations/conv_pines016_shelf_space.eml` | email thread | 2009-04-13 | Shelf space vs. usage - help needed |
| DOC-04 | `conversations/conv_pines018_item_transfer.eml` | email thread | 2009-05-11 | Moving items between branches - utility needed |
| DOC-05 | `conversations/conv_pines019_020_missing_intransit.eml` | email thread | 2009-04-16 | Missing and damaged items - we need a report |
| DOC-06 | `conversations/conv_pines021_item_purging.eml` | email thread | 2009-04-21 | Weeding reports - item purging needs |
| DOC-07 | `conversations/conv_pines022_deletions.eml` | email thread | 2009-04-24 | Tracking deletions - who deleted what? |
| DOC-08 | `conversations/conv_pines023_patron_characteristics.eml` | email thread | 2009-04-29 | Patron reports by demographics - how? |
| DOC-09 | `conversations/conv_pines024_inactive_patrons.eml` | email thread | 2009-05-05 | Inactive patrons report needed |
| DOC-10 | `early_draft_srs_galecia.txt` | draft specification | 2009-01-27 | DRAFT SOFTWARE REQUIREMENTS SPECIFICATION |
| DOC-11 | `email_financial_reports.eml` | email thread | 2009-07-13 | Financial reporting requirements - discussion thread |
| DOC-12 | `email_report_features.eml` | email thread | 2009-07-27 | Report features and interface requirements |
| DOC-13 | `email_staff_login.eml` | email thread | 2009-04-09 | Staff login difficulties - need for streamlined access |
| DOC-14 | `evergreen_reference_2009.txt` | reference document | 2009-03-15 | EVERGREEN ILS - REPORTING MODULE OVERVIEW |
| DOC-15 | `interview_cataloging_2009-05-08.txt` | stakeholder interview | 2009-05-08 | PINES REPORTS WORKING GROUP - INTERVIEW RECORD |
| DOC-16 | `interview_sysadmin_2009-05-10.txt` | stakeholder interview | 2009-05-10 | PINES REPORTS WORKING GROUP - INTERVIEW RECORD |
| DOC-17 | `meeting_minutes/meeting_2009-03-15_minutes.txt` | meeting minutes | 2009-03-15 | PINES REPORTS WORKING GROUP - FIRST MEETING MINUTES |
| DOC-18 | `meeting_minutes/meeting_2009-07-20_minutes.txt` | meeting minutes | 2009-07-20 | PINES REPORTS WORKING GROUP - SECOND MEETING MINUTES |
| DOC-19 | `meeting_tech_subcommittee_2009-06-30.txt` | meeting notes | 2009-06-30 | PINES TECHNICAL SUBCOMMITTEE MEETING NOTES |
| DOC-20 | `survey_results_2009.txt` | survey results | 2009-04-20 | PINES STAFF REPORTS SURVEY - RESULTS SUMMARY |

## 4. Glossary

Preferred terms used consistently throughout this document.

| Term | Definition | Avoid |
|---|---|---|
| **authorized staff user** | A staff member or other authorized worker permitted to log in, operate the system, or use reports according to assigned permissions. | user, staff member, operator, employee user |
| **client application** | A browser-based or Windows-compatible software interface used to access the reporting system; this term does not mean a library patron. | client when referring to a patron, patron-facing client unless the software interface is intended |
| **consortium** | The broader group of participating library systems governed or operated together. | network, enterprise |
| **hold** | A patron request for an item or title, including its placement method, status, fulfillment, and pickup state. | request, reservation, hold request |
| **item** | An owned or circulating physical or electronic copy that can have a location, status, circulation history, value, or transfer history. | copy, material, volume |
| **item location** | The current physical or organizational location assigned to an item, which may differ from its owning library or transfer destination. | location, branch location, facility location |
| **library** | An organizational or physical library unit that owns, houses, or manages items and can be used as a reporting scope. | branch, facility |
| **library system** | An administrative collection of one or more libraries that share operational data, policies, and reporting. | local system, system, organization |
| **patron** | A library customer whose account, demographic information, holds, circulation activity, or financial activity may be represented in the system. | borrower, customer, client, community user |
| **purge** | An authorized operation that permanently deletes selected records or related records from the system. | removal, deletion when the broader audit or policy concept is intended |
| **query** | A set of selectable fields, filters, joins, grouping rules, and Boolean conditions used to retrieve or analyze records. | search, report definition, filter |
| **report** | A generated presentation or export of queried, aggregated, or predefined system data. | output, listing, analysis |
| **report template** | A saved report definition containing fields, criteria, formatting, permissions, and optionally scheduling or delivery settings. | canned report, report definition, saved query |
| **report user** | An authorized staff user who runs, designs, schedules, reviews, or administers reports. | report consumer, report operator |
| **reporting system** | The software product specified by this document, distinct from the enterprise Library Automation System and from a library system or consortium. | system, enterprise, client |
| **transaction** | A recorded operational or financial occurrence such as a checkout, check-in, renewal, hold placement, payment, or registration. | activity, event, operation |
| **uncataloged material** | Library material tracked for inventory or circulation without a complete bibliographic record. | non-cataloged material, uncataloged shipment, bulk material |
| **weeding** | The collection-management process of identifying items for review, withdrawal, discard, or purge; it does not itself imply deletion. | cleanup, purge |

## 5. Requirements

### 5.1 Authentication & Staff Login (AUTH)

_Staff login mechanisms (username/password, card-swipe, optional streamlined login), session handling, login audit, and role-at-login behavior._

#### REQ-AUTH-001 — Staff Login Options

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-13 (`email_staff_login.eml`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Priority rationale:** The draft specification marks card-swipe and username/password login as high priority, and the agreed email discussion and later meeting minutes reiterate the need for card-swipe login while preserving optional use and a fallback.

The system shall support staff authentication using individual username and password credentials or card-swipe login, such as an RFID employee badge. Card-swipe login shall be optional and shall not require card-reader hardware; username and password login shall remain available as a fallback, including for staff without cards and branches without readers. A successful card swipe shall log the identified staff member in immediately. Streamlined login options shall be available to reduce login time and the security risks associated with password sharing and terminals left logged in compared with manual login.

#### REQ-AUTH-002 — Individual Login Accountability

- **Priority:** P2  ·  **Type:** data
- **Derived from:** DOC-13 (`email_staff_login.eml`)
- **Priority rationale:** The source explicitly describes individual identification as important for audit purposes and states that card-swipe login must not bypass individual authentication.

The system shall record which staff member is logged in whenever a login occurs, for audit purposes. Every login method, including card-swipe login, shall identify the individual staff member. Card-swipe login shall not bypass individual authentication or accountability.

#### REQ-AUTH-003 — Automatic Session Protection

- **Priority:** P3  ·  **Type:** non-functional
- **Derived from:** DOC-13 (`email_staff_login.eml`)
- **Priority rationale:** A frontline security problem is explicitly raised in one email thread, but no threshold or additional source establishes a higher priority.

The system shall provide automatic session protection to reduce the risk of terminals being left logged in and staff sharing passwords. This protection shall include mechanisms such as automatic session locking or logout. The source does not specify a timeout, so the system shall not assume a particular inactivity threshold from this requirement.

#### REQ-AUTH-004 — Password Change Reporting

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** This is a single proposed missing report type in a reference document, with no higher-priority marker or evidence of broad stakeholder agreement.

The system shall provide a report listing staff accounts and the date of each account's last password change. The report shall allow IT and security personnel to review password-change dates across staff accounts. The source identifies this report as currently unavailable but provides no evidence that it blocks core login use.

### 5.2 Authorization, Permissions & Admin Scope Control (ROLE)

_Role-based and fine-grained access control for report and operational functions; admin capabilities for managing groups/roles, template edit restrictions, and scoped permissions._

#### REQ-ROLE-001 — Database Table And Field Permissions

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** The source explicitly marks control of table and field access as high priority, making it a stated security requirement.

The system shall allow administrators to control staff access to database tables and fields used in queries. Administrators shall be able to restrict which data structures and fields each authorized user can access. This shall limit query access to the data appropriate for a user's responsibilities.

#### REQ-ROLE-002 — Fine-Grained Report Permissions

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`), DOC-14 (`evergreen_reference_2009.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Fine-grained report permissions are marked high priority, appear across several sources, and were prioritized by 76% of survey respondents.

The system shall provide fine-grained permissions that control which users can create, clone, modify, run, schedule, and view reports. Permissions shall be configurable for specific reports and shall also control who may add canned reports. These controls shall allow administrators to grant report capabilities according to users' roles and responsibilities.

#### REQ-ROLE-003 — Report Folder Run Permissions

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Shared-folder report permissions are marked high priority in the draft and repeated in agreed sources, including survey results.

The system shall allow administrators to create shared folders for reports and assign permissions to specific staff for running reports stored in those folders. Administrators shall be able to allow or deny run access to particular reports through these folder permissions. This shall support controlled sharing of reports with the appropriate users.

#### REQ-ROLE-004 — Role-Based Access Control

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-13 (`email_staff_login.eml`), DOC-16 (`interview_sysadmin_2009-05-10.txt`), DOC-17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** Role-based access control is explicitly marked high priority and essential, and is supported across multiple stakeholder sources.

The system shall control access to authorized system and report functions through configurable roles and security groups. Administrators shall be able to assign roles or groups to authorized staff users, and permissions shall be determined from those assignments at login regardless of login method. Permissions shall provide access appropriate to each authorized staff user's responsibilities.

#### REQ-ROLE-005 — Scoped Ad Hoc Dataset Access

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`)
- **Priority rationale:** Control of ad hoc reporting on specific data sets is marked high priority, and a later agreed source also identifies shared folders as an access-control mechanism.

The system shall allow administrators to allow or deny staff the ability to run ad hoc reports on specific sets of data. Administrators shall be able to use shared folders to control access to those data sets. These controls shall limit ad hoc reporting to staff authorized for the relevant data.

#### REQ-ROLE-006 — Template Edit Restrictions

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`)
- **Priority rationale:** Template editing restrictions are marked high priority in the draft and reaffirmed in an agreed source; the sources identify dependable and accurate output as the purpose.

The system shall allow administrators to restrict which template filters and display fields staff can alter. Restrictions shall be configurable to prevent front-line staff from changing a template to display deleted items. These controls shall help preserve dependable and accurate report output.

#### REQ-ROLE-007 — Predefined Role Capability Profiles

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-13 (`email_staff_login.eml`), DOC-16 (`interview_sysadmin_2009-05-10.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** An agreed meeting provides a specific set of role access levels, and stakeholder sources also provide consistent administrative capabilities and concrete role examples.

The system shall support role profiles for Global Admin, Local Admin, Library Manager, Staff, and Patron. Global Admin shall have full system access, including software changes and configuration and statistical reporting for the entire system or consortium; Local Admin shall be able to configure local settings and run branch-level or system reports. Library Manager shall be able to run approved reports and make limited template modifications, while Staff shall run reports within assigned permissions and Patron access shall be indirect through OPAC displays. The system shall also support profiles such as front-desk staff with basic reports and limited filters, department heads with template creation and modification, and system administrators with full report and permission access.

#### REQ-ROLE-008 — Query Tool Access Control

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-12 (`email_report_features.eml`)
- **Priority rationale:** Administrator control of query-tool access was agreed and included in a consolidated summary, though it is supported by one source.

The system shall allow administrators to control which users can access the query tool. Administrators shall be able to grant or deny access according to users' roles and responsibilities. This control shall prevent users from accessing query functionality unless authorized.

#### REQ-ROLE-009 — Role And Group Administration

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`), DOC-13 (`email_staff_login.eml`), DOC-16 (`interview_sysadmin_2009-05-10.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** Multiple stakeholders and sources request role and group management and emphasize easy administration; role changes provide a practical way to manage permissions.

The system shall allow administrators to create, modify, and delete roles and security groups and to manage their membership. Administrators shall be able to change a user's permissions by changing the user's role assignment, with the user's permissions updated automatically to match that role. The system shall provide an easy-to-administer interface for managing report permissions and roles, avoiding the need to edit permissions individually for routine role changes.

#### REQ-ROLE-010 — Cross-Branch Capacity Access

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-02 (`conversations/conv_pines015_capacity_interface.eml`)
- **Priority rationale:** This is a specific operational need requested in one source, with no evidence of broader stakeholder agreement or an explicit high-priority marker.

The system shall allow branch managers and other authorized roles to view capacity information for all branches, not only their own branch. Access to this information shall be governed by the user's permissions. This shall support operational decisions such as reallocating items or resources across branches.

#### REQ-ROLE-011 — Mass Deletion Safeguards

- **Priority:** P3  ·  **Type:** non-functional
- **Derived from:** DOC-06 (`conversations/conv_pines021_item_purging.eml`)
- **Priority rationale:** An agreed source identifies a consequential safety concern and proposes concrete safeguards, but the requirement appears in only one source.

The system shall provide safeguards against accidental mass deletion of collections. Safeguards shall include configurable limits or warnings for large batches, read-only previews, mandatory confirmations, role-based restrictions, and audit logging. These controls shall help administrators and technical staff prevent unintended loss of collection data.

#### REQ-ROLE-012 — Transfer Role Authorization

- **Priority:** P3  ·  **Type:** constraint
- **Derived from:** DOC-04 (`conversations/conv_pines018_item_transfer.eml`)
- **Priority rationale:** A single source requests role-based limits on transfers; the need is concrete but has no explicit high-priority marker or broader evidence of agreement.

The system shall restrict the ability to initiate item transfers between branches to authorized roles. Authorized roles shall include managers, administrators, or transfer coordinators as configured by the organization. This shall prevent staff without an appropriate operational responsibility from initiating transfers.

### 5.3 Web App UI, Help & Accessibility (UIXT)

_Web-based report writer interfaces, query UI/UX, interactive help (hierarchical/cross-linked/online), hover tooltips, and accessibility/non-interference with OPAC._

#### REQ-UIXT-001 — Integrated Online Help

- **Priority:** P1  ·  **Type:** documentation
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`), DOC-16 (`interview_sysadmin_2009-05-10.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** C-145 is marked High Priority, C-497 identifies context-sensitive help as critical, and agreed requirements in C-530 and C-497 plus C-360, C-438, and C-145 show broad support across sources.

The system shall provide an online, HTML-based help system integrated with the reporting interface. Help shall be hierarchical, cross-linked, searchable, and easy to navigate, and shall describe and illustrate all system functions. The system shall provide context-sensitive help so users can understand the reporting functions relevant to their current task and reduce the need to contact IT for routine guidance.

#### REQ-UIXT-002 — Standards Compliant HTML

- **Priority:** P1  ·  **Type:** constraint
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-16 (`interview_sysadmin_2009-05-10.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** C-154 is marked High Priority, C-449 calls accessibility non-negotiable, and agreed requirements in C-504 and C-537 specify standards validation across multiple sources.

The system shall produce valid, standards-compliant HTML for the web interface, online help, and report output. The HTML shall validate against applicable W3C standards. It shall use semantic structure and provide alt attributes and ARIA labels where appropriate, supporting accessible use of the web-based components.

#### REQ-UIXT-003 — Staff Report Authoring

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`), DOC-17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)
- **Priority rationale:** Custom report authoring is requested for staff in two candidates and supports a significant user group, though no source marks it mandatory or high priority.

The system shall provide library staff with a web-based report writer for creating custom reports. It shall allow staff to create and edit report content, recognizing staff as the primary report creators. This capability shall let staff develop reports through the web application rather than requiring a separate authoring interface.

#### REQ-UIXT-004 — Approved Report Type Coverage

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** This is a proposed improvement from one source, with no priority marker or additional evidence establishing it as a core-use blocker.

The system shall provide every report type in the controlled report-gap register approved for the project. Before acceptance testing, the project shall identify the register by controlled artifact identifier and version and ensure it specifies each report type's required fields, filters, scope, and output rules. Acceptance testing shall verify each entry in that fixed baseline; report types not in the approved version are outside this requirement.

#### REQ-UIXT-005 — Large Location Usability

- **Priority:** P3  ·  **Type:** non-functional
- **Derived from:** DOC-02 (`conversations/conv_pines015_capacity_interface.eml`)
- **Priority rationale:** One source identifies a concrete scale concern of 286 locations, but the request is a proposed consideration rather than an agreed or explicitly high-priority requirement.

The system shall remain usable when displaying hundreds of locations, including a set of approximately 286 locations. It shall provide mechanisms such as grouping or filtering, or other suitable interface techniques, to prevent the display from becoming overcrowded. These mechanisms shall help users work with location information at the stated scale.

#### REQ-UIXT-006 — Quick Access Descriptions

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** The feature is identified as missing in one source, with no explicit priority marker or evidence of a workaround-free need.

The system shall provide a quick-access interface for users selecting reports and options. The interface shall display pop-up descriptions for reports and options to help users identify appropriate choices. This shall make common reporting choices easier to locate and understand.

#### REQ-UIXT-007 — Report Title Tooltips

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** The same usability improvement appears in two sources, but neither supplies a high-priority marker or evidence that it blocks core reporting use.

The system shall display a brief description when an authorized staff user hovers over the title of a report template in the report-selection interface. The description shall identify the template's purpose before the staff user selects it. Acceptance testing shall verify that a configured description appears for each template with a description and that templates without one do not display misleading text.

#### REQ-UIXT-008 — Usable Reports Interface

- **Priority:** P3  ·  **Type:** non-functional
- **Derived from:** DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** The need is grounded in a staff survey but appears in only one candidate and has no reported survey percentage or explicit priority marker.

The system shall provide an intuitive reports interface that helps staff find and run the reports they need. The interface shall make report choices and the steps to run a selected report understandable to users. This shall address reported difficulty locating needed reports and support staff in completing routine reporting tasks.

### 5.4 Query Builder, Filters & Candidate Selection Engine (DATAQ)

_Relational query capabilities for selecting/reporting entities: field selection, drag-and-drop, boolean logic (AND/OR), complex criteria, LIMIT/GROUP BY, regex/picklists upload files, null inclusion options, and displaying criteria/results._

#### REQ-DATAQ-001 — Combine Query Criteria

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-06 (`conversations/conv_pines021_item_purging.eml`), DOC-08 (`conversations/conv_pines023_patron_characteristics.eml`), DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`), DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** Boolean operators are explicitly marked high priority and are requested in several sources, including an agreed multi-participant request; customizable status, time, and activity criteria are also agreed.

The system shall let report users combine query clauses using AND and OR Boolean operators and group clauses. Supported item statuses shall include missing, discard or weed, and damaged, as defined by the Library Automation System status codes. A time-in-status criterion shall mean elapsed time since the item entered its current status, and activity criteria shall include elapsed time since last circulation. Acceptance testing shall verify combined criteria against records with known statuses, status-entry dates, and circulation dates.

#### REQ-DATAQ-002 — Display Query Criteria

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`)
- **Priority rationale:** Displaying criteria with results is marked high priority in a draft specification and appears again in an agreed request.

The system shall display the query selection criteria alongside the resulting records. The displayed criteria shall clearly identify the selections used to generate the report. This shall allow staff and auditors to understand how the result set was produced.

#### REQ-DATAQ-003 — Include Null And Blank Values

- **Priority:** P1  ·  **Type:** data
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** The requirement is stated as a must in agreed meeting notes and is repeated across a draft specification, reference document, and survey; a later agreed decision supersedes the earlier question about whether users should choose to exclude nulls.

The system shall include records with null or blank field values in query and report results rather than implicitly filtering them out. This behavior shall apply regardless of the selected filters or displayed fields. This shall make records with missing data visible in reporting.

#### REQ-DATAQ-004 — Select Picklist Values

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`)
- **Priority rationale:** Picklist selection is explicitly marked high priority in a draft specification and is also included in an agreed request.

The system shall allow staff to select query values from picklists of possible values. Picklist selection shall be available while designing a query. This shall help users supply valid filter values without having to enter them manually.

#### REQ-DATAQ-005 — Select Report Fields

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`), DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** Field selection is explicitly marked high priority in a draft specification, appears in an agreed request, and limited field availability is identified as a current limitation.

The system shall allow staff to choose fields to query and fields to display in a report. Report authors shall be able to select fields using drag-and-drop. The system shall expose a comprehensive set of database fields rather than a limited subset so users can build reports with the data they need.

#### REQ-DATAQ-006 — Usable Query Designer

- **Priority:** P1  ·  **Type:** non-functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`)
- **Priority rationale:** The need is explicitly marked high priority in a draft specification and is also included in an agreed request from library staff and directors.

The system shall provide an interface that allows authorized staff users to design queries across bibliographic, item, patron, transaction, and financial records without requiring specialist technical skills. The interface shall expose the supported fields and query criteria and provide validation feedback for incomplete or invalid criteria. Acceptance testing shall verify that a staff user can create and run a query for each supported record type using the displayed controls.

#### REQ-DATAQ-007 — Use Regular Expressions

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`), DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** Regular-expression support is explicitly marked high priority in a draft specification, identified as a current limitation, and included in an agreed request.

The system shall support regular-expression matching in query and report filters. Staff shall be able to select regular expressions from a dropdown when designing queries. This shall enable advanced matching while making available expressions discoverable to users.

#### REQ-DATAQ-008 — Complete Data Specifications

- **Priority:** P2  ·  **Type:** documentation
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** Complete data specifications are agreed and described as essential, with the requirement repeated in meeting minutes and later meeting notes.

The system developer shall provide complete data specifications for authority, bibliographic, order, item, hold, and other records maintained or accessed by the system. The specifications shall identify record and field names, data types, relationships, and which records and fields are available for querying. The documentation shall be delivered with the system and reviewed against the data structures available to report authors, developers, integrators, and data architects.

#### REQ-DATAQ-009 — Filter And Sort Reports

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Basic filtering and sorting are identified as needed, and a survey reports that some relevant fields are not currently available for filtering.

The system shall allow report authors and users to filter and sort report definitions and results. Filtering shall be available on relevant report fields, including fields that are not currently filterable. This shall let users create and refine reports using the data they need.

#### REQ-DATAQ-010 — Filter By Survey Name

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** The same need appears in a draft specification and meeting notes, with the latter defining the required name-to-ID resolution.

The system shall allow users to filter reports by survey name rather than requiring them to enter a survey ID. The system shall resolve the selected survey name to its corresponding ID internally. This shall make survey-based filtering usable without requiring users to know internal identifiers.

#### REQ-DATAQ-011 — Group Patron Results

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-08 (`conversations/conv_pines023_patron_characteristics.eml`)
- **Priority rationale:** The request is agreed and described as essential for program planning by a stakeholder, but comes from one source.

The system shall allow users to group report results by patron age range, ZIP code, county of residence, home branch, patron type, and preferred language. Grouping shall support aggregates such as checkout counts by age range. This shall help staff analyze patron activity for planning purposes.

#### REQ-DATAQ-012 — Identify Data Quality Issues

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`), DOC-15 (`interview_cataloging_2009-05-08.txt`)
- **Priority rationale:** Specific data-quality report needs are identified in a reference document and emphasized in a stakeholder interview.

The system shall provide reports that identify bibliographic records missing specified MARC fields. It shall also report items with invalid item types, items with excessively long call numbers, and bibliographic records with no item records. This shall help cataloging staff find records that need data-quality review.

#### REQ-DATAQ-013 — Identify Purge Candidates

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-06 (`conversations/conv_pines021_item_purging.eml`)
- **Priority rationale:** Cataloging staff agreed on customizable purge criteria, and the source provides concrete status, time, and activity examples.

The system shall allow cataloging staff to identify item records for purging using customizable criteria. Criteria shall include item status, such as missing or discard/weed, time spent in a status, and activity such as time since last circulation. Users shall be able to combine applicable criteria to identify the items that meet their purge policy.

#### REQ-DATAQ-014 — Normalized, Isolated Reporting Architecture

- **Priority:** P2  ·  **Type:** constraint
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`), DOC-16 (`interview_sysadmin_2009-05-10.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** Reporting isolation and historical-data handling are requested across multiple sources, and database impact is identified as a significant concern; a normalized architecture provides a clear, consistent constraint.

The system shall support reporting queries over normalized relational data and shall not require a denormalized copy of production data. Reporting workloads shall be isolated from production transactions using a read-only replica, normalized historical store, snapshots, or an equivalent architecture; reporting access shall not modify source records. The implementation shall document data synchronization and reconciliation, workload isolation, and the data-through timestamp, which each report shall identify. Denormalized reporting stores are not permitted by this requirement.

#### REQ-DATAQ-015 — Present MARC Fields Per Record

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** The need is repeated in a draft specification and a survey, with the survey identifying a concrete problem affecting cataloging and reporting staff.

The system shall allow users to select and extract specific MARC fields for reports. It shall present the selected MARC fields for each bibliographic record on a single row rather than spreading that record's fields across multiple rows. This shall make the extracted fields usable together in report results.

#### REQ-DATAQ-016 — Query Across Record Types

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`)
- **Priority rationale:** Access to all record types and the named open-template attributes are requested in multiple candidates, including an agreed request.

The system shall allow users to design and run queries against all record types available to the system. Open report templates shall expose attributes associated with circulation, items, patrons, bills, and bibliographic records for both filtering and display. This shall allow staff to build queries across the record domains needed for reporting.

#### REQ-DATAQ-017 — Select Records From Query Results

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-04 (`conversations/conv_pines018_item_transfer.eml`), DOC-15 (`interview_cataloging_2009-05-08.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Manual selection is requested in an email, a stakeholder interview, and survey results, where 39% requested the capability.

The system shall allow authorized staff users to select individual records or items from query results for a targeted action. The selection shall be limited to the results the staff user chooses, rather than automatically including the complete query result. Transfer workflows and other supported targeted actions shall use this reusable selection capability.

#### REQ-DATAQ-018 — Transfer Candidate Query and Preparation

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-04 (`conversations/conv_pines018_item_transfer.eml`), DOC-10 (`early_draft_srs_galecia.txt`), DOC-15 (`interview_cataloging_2009-05-08.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Candidate-material queries appear in a stakeholder interview and a survey, with 44% of respondents requesting the capability; a separate request also describes a concrete location and inactivity use case.

The system shall provide a query capability for identifying candidate items for transfer, including criteria such as item location and circulation inactivity. Authorized staff users shall be able to review the query results and prepare a transfer batch from selected candidates; selection of individual results shall use the reusable result-selection capability in REQ-DATAQ-017. This shall combine query-driven discovery with controlled preparation of transfer batches.

#### REQ-DATAQ-019 — Upload Identifier Filters

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** Identifier-file filtering is requested in a draft specification and listed as a missing feature in a reference document.

The system shall allow users to upload a text file of identifiers and use those identifiers as report filter criteria. Supported examples shall include barcodes and TCNs. This shall let users select report records by supplying a prepared identifier list.

#### REQ-DATAQ-020 — Filter Transaction Details

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** The specific transaction filters are requested in one draft specification, with no additional priority or agreement evidence.

The system shall allow users to filter reports by transaction date and time, workstation, and staff member. Users shall be able to apply these criteria when running a report. This shall support investigation and reporting of transactions by when, where, and by whom they occurred.

#### REQ-DATAQ-021 — Reuse Existing Query Tool

- **Priority:** P3  ·  **Type:** constraint
- **Derived from:** DOC-04 (`conversations/conv_pines018_item_transfer.eml`)
- **Priority rationale:** Reuse or integration is proposed by technical staff in one source, with no evidence that it is mandatory or agreed.

The system shall support reuse or integration of the existing report query tool for candidate selection. This shall allow staff to use established query capabilities when identifying candidate records. The implementation shall preserve the ability to apply the candidate-selection queries required by the system.

### 5.5 Report Templates, Scheduling, Queue & Outputs (RPTMG)

_Canned and template-based report creation/management, run controls (ad hoc, modifiable vs run-as-is), scheduling/recurrence, queue visibility/status/cancel, report prioritization, pagination/progress, and output formats/exports (CSV/HTML/Excel/email)._

#### REQ-RPTMG-001 — Board and External Reports

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Priority rationale:** A source marks board and external reports high priority, and the reports include statistics tied to formal state reporting; multiple sources request predefined board or executive reports.

The system shall provide the predefined reports for library boards and external reporting needs, including the Georgia Annual Report and the Application for State Aid. Before acceptance testing, the project shall identify the controlled, approved, versioned report catalog and applicable form versions, including required fields, calculations, reporting periods, and output rules. Acceptance testing shall verify each report against that fixed baseline; changes require an approved version update.

#### REQ-RPTMG-002 — Create, Edit, and Version Report Templates

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`), DOC-14 (`evergreen_reference_2009.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Template creation is marked high priority in one source, has 81% survey support, and is requested across multiple sources.

The system shall allow report administrators to create report templates, edit their saved configuration, and maintain versions when a template is changed. Report administrators shall be able to make templates available to report users subject to assigned permissions. This requirement covers the saved template lifecycle; cloning is covered by REQ-RPTMG-026, and run-specific changes are covered by REQ-RPTMG-006.

#### REQ-RPTMG-003 — Report and Capacity Data Export Formats

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-02 (`conversations/conv_pines015_capacity_interface.eml`), DOC-03 (`conversations/conv_pines016_shelf_space.eml`), DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** CSV, Excel, and HTML are explicitly described as required, and survey support for multiple formats is 61%; several sources request the capability.

The system shall allow report users to export report outputs and capacity data in CSV, Excel, and HTML formats. Capacity data, including capacity views, shall be exportable in CSV or Excel for use in spreadsheet applications. Report users shall be able to select an available format appropriate to their intended use.

#### REQ-RPTMG-004 — Report Job Prioritization

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`), DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** An agreed source calls prioritization crucial, and multiple sources request the ability to move important reports ahead in the queue.

The system shall allow authorized administrators to prioritize specific report jobs or report types in the processing queue. Prioritized reports shall move ahead of other queued reports, including resource-consuming ad hoc queries, so that important reports such as a director's board report can run sooner. The system shall display report priority and provide controls for changing it.

#### REQ-RPTMG-005 — Report Queue Visibility

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`), DOC-14 (`evergreen_reference_2009.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Queue visibility is requested across multiple sources, is marked high priority in one source, and received 68% survey support; status information is also reported to reduce help-desk calls.

The system shall allow users to see their submitted report's position in the processing queue and how many reports are ahead of it. The system shall display report status as waiting, running, completed, or failed, together with the report submission timestamp. This shall help users understand progress and reduce requests to IT for status information.

#### REQ-RPTMG-006 — Run Report Templates With Optional Run-Time Changes

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`)
- **Priority rationale:** C-193 explicitly marks this capability as high priority, and C-305 separately agrees that templates should be runnable as-is.

The system shall allow report users to run a report template as saved or change supported criteria for an individual run without changing the saved template. Access to templates and run-time changes shall follow assigned permissions. This requirement covers execution and run-specific changes; saved template creation, editing, and versioning are covered by REQ-RPTMG-002, and cloning is covered by REQ-RPTMG-026.

#### REQ-RPTMG-007 — Versioned Report Definition Catalog

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** The draft specification marks this item high priority and states that the system must support the Appendix A definitions.

The system shall support the report definitions in a controlled, versioned report catalog that identifies each report, its fields, filters, scope, and output rules, including the definitions formerly referenced as Appendix A and Appendix B. Before acceptance testing, the project shall include the catalog's controlled artifact identifier and approved version in the specification. Acceptance testing shall verify every definition in that fixed version; changes to the catalog require an approved version update.

#### REQ-RPTMG-008 — Canned Report Display Editing

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** Two sources request editable canned-report displays, including field selection and column presentation options.

The system shall allow users to edit display options for canned reports. Users shall be able to add or remove displayed fields, such as shelving location, and change the order and format of displayed columns. This shall allow report authors and administrators to tailor report presentation to users' needs.

#### REQ-RPTMG-009 — Circulation Report Catalog

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** Circulation reporting is detailed in the draft specification and was selected by 78% of survey respondents as a standard report type.

The system shall provide circulation reports for check-ins, check-outs, renewals, non-cataloged circulation, total circulation, and items overdue by a specified number of days. Reports shall support breakdowns by circulation modifier, Cat1, Cat2, Dewey, shelving location, MARC, and circulation location. Circulation-location reports shall support breakdowns by patron county and home library, and reports shall also support age-demographic breakdowns.

#### REQ-RPTMG-010 — Custom Local Reports

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** The survey indicates that 38% use custom reports and provides several concrete report examples, showing a meaningful user need.

The system shall support the creation and use of custom or local reports. Supported examples shall include collection development reports, program attendance tracking, and staff productivity reports, including time spent per transaction. This shall enable local library staff to report on needs beyond predefined report definitions.

#### REQ-RPTMG-011 — Email Report Delivery

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Email delivery is requested in two sources and received 45% support in the survey, indicating meaningful but not majority demand.

The system shall deliver generated reports by email to one or more recipients entered by a report user or selected from an address book. Before delivery, the report user shall be able to review and change the recipient list. The system shall report whether delivery succeeded or failed for each recipient so report users can verify the delivery outcome.

#### REQ-RPTMG-012 — Holds Report Catalog

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** The holds report set is detailed in one draft source, and a separate source specifically identifies the Holds Purchase Alert as missing.

The system shall provide reports for Holds Purchase Alerts, items sent for holds, items received for holds, unfilled holds, annual hold counts, and stale holds awaiting pickup. It shall provide IntraPINES loan reports for the consortium and library systems, with results broken down by those scopes. Each report shall identify its reporting scope and period so authorized staff users can interpret results consistently.

#### REQ-RPTMG-013 — PINES Library Templates

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Priority rationale:** Two meeting sources affirm the need for templates across PINES libraries, including a unanimously carried motion.

The system shall support identifying, creating, and delivering the report templates needed by PINES libraries. The templates shall be available for use across those libraries. This shall address the template needs agreed for the PINES library community.

#### REQ-RPTMG-014 — Recurring Report Scheduling

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** The survey reports that 52% prioritized the ability to schedule recurring reports, indicating substantial user demand.

The system shall allow users to schedule reports to run on a recurring basis. Report schedulers shall be able to use this capability for reports that need to run repeatedly. This shall reduce the need to initiate each recurring report manually.

#### REQ-RPTMG-015 — Report Cancellation

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Four sources request cancellation of scheduled or running reports, and a meeting source confirms the required cancellation checks are technically feasible.

The system shall allow users or administrators to cancel a scheduled report or a report that is currently running. During processing, the system shall check for cancellation signals and stop the report when cancellation is requested. This shall give users control over unwanted or no-longer-needed report jobs.

#### REQ-RPTMG-016 — Report Criteria Display

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** Two sources request showing criteria with results, including the date selection and report name.

The system shall display the selection criteria used to generate a report alongside its results. The displayed information shall include the selected date criteria and the report name, positioned at the top or bottom of the results. This shall help report consumers understand the scope and origin of the results.

#### REQ-RPTMG-017 — Reporting Interface Options

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** The draft specification says all three interfaces are needed, but provides no explicit high-priority marker or evidence from additional sources.

The system shall provide three reporting interfaces: predefined report templates, on-demand reports configured for a specific run, and open-template reporting. The interface shall identify the selected mode and provide the controls needed to run or configure it; open-template reporting shall support ad hoc reporting by advanced report users. Acceptance testing shall verify that a report user can run a predefined template, change run-time criteria for an on-demand report, and create or configure an open template.

#### REQ-RPTMG-018 — Save and Reuse Queries and Report Templates

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-04 (`conversations/conv_pines018_item_transfer.eml`), DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`), DOC-15 (`interview_cataloging_2009-05-08.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** C-058 describes repeated monthly use as crucial, while C-383 and C-061 also request saving, reuse, or sharing.

The system shall allow report users to save queries and report templates for repeated use, including recurring monthly work. Report users shall be able to share saved queries or templates with other authorized staff users when permitted by assigned roles. Changes shall be governed by the applicable template permissions; conversion between saved queries and report templates and version history are not required by this capability.

#### REQ-RPTMG-019 — Scheduled Report Frequencies

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** Scheduling options are requested in more than one source, and one source lists the full set of required frequencies.

The system shall allow report users to run a report as soon as possible or schedule it to run hourly, daily, weekly, monthly, or yearly. The selected frequency shall be available when configuring the report schedule, and hourly scheduling shall be supported alongside the other listed frequencies.

#### REQ-RPTMG-020 — Standard Report Categories

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** A survey identifies broad staff demand, including 78% for circulation, 65% for item, and 52% for patron reports.

The system shall provide standard report categories for circulation, items, patrons, finances, and holds, as well as custom and on-demand reports. Examples shall include circulation check-outs, check-ins, and renewals; item inventory, weeding, and missing-item reports; patron demographics and inactive accounts; and fines and payments. This shall give library staff access to commonly requested report types.

#### REQ-RPTMG-021 — Template Run Modification

- **Priority:** P2  ·  **Type:** constraint
- **Derived from:** DOC-12 (`email_report_features.eml`)
- **Priority rationale:** The requirement was agreed by staff and administrators, with consistency identified as the reason for preserving the original template.

The system shall allow staff to modify a report template for an individual run without changing the original template. Run-specific modifications shall not compromise the original template or its results. This shall let staff adapt a report while preserving a consistent reusable template.

#### REQ-RPTMG-022 — Batch Report Execution

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** Requested in two sources as a useful capability, with no high-priority marker or evidence that it blocks core use.

The system shall allow users to select multiple saved or canned reports and run them in one operation. When requested, the system shall present the results together in a single document. This shall reduce the effort of running and reviewing related reports individually.

#### REQ-RPTMG-023 — Bibliographic Record Reports

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** The report set is specified in one draft source without an explicit priority marker.

The system shall provide bibliographic record reports for total records, edited records, and records added by user and library. It shall also provide reports for bibliographic records with no attached volumes and records missing specified MARC fields. These reports shall help staff identify and review bibliographic record counts and data issues.

#### REQ-RPTMG-024 — Check-In Type Counts

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** Requested in one draft specification, with no evidence of a blocking need or high-priority marker.

The system shall provide individual and cumulative check-in counts by check-in type. Supported types shall include book-drop, terminal, user, and self-service check-ins. This shall allow staff to review check-in activity by its method or source.

#### REQ-RPTMG-025 — Check-Out Type Counts

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** Requested in one draft specification, with no evidence of a blocking need or high-priority marker.

The system shall provide individual and cumulative counts for staff check-outs, self check-outs, staff renewals, self check-out renewals, online renewals, and OPAC renewals. Staff shall be able to review activity separately by these transaction types. This shall support analysis of circulation activity across service methods.

#### REQ-RPTMG-026 — Clone Report Templates

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-12 (`email_report_features.eml`)
- **Priority rationale:** An agreed email source identifies cloning as a distinct useful capability, but there is no evidence it is essential to core use.

The system shall allow a report user with the required permission to clone an existing report template and save the clone as a separate template for further modification. Cloning shall not alter the original template. This requirement covers creation of a new template from an existing one; editing and versioning the saved template are covered by REQ-RPTMG-002, and run-specific changes are covered by REQ-RPTMG-006.

#### REQ-RPTMG-027 — Excel Export Deduplication

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** A single survey response identifies duplicate rows as a problem, with no broader priority evidence.

The system shall provide Excel exports without excessive duplicate rows or provide an option to deduplicate exported rows. Users shall be able to obtain a spreadsheet with redundant rows removed when needed. This shall address the stated difficulty of using exported data in Excel.

#### REQ-RPTMG-028 — Executive Report Interface

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Priority rationale:** An agreed meeting source identifies the interface and report list as a relevant need, but does not specify high-priority functionality.

The system shall provide an Executive Reports Interface containing a compiled list of reports needed for executive use. The interface shall make those reports accessible to executive stakeholders. This shall support executive access to the reports identified for their use.

#### REQ-RPTMG-029 — Hold Type Subtotals

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** A single draft specification requests these specific subtotals, with no explicit priority marker.

The system shall subtotal holds by hold type in reports. Supported types shall include active, frozen, and frozen-until holds. This shall allow staff to review hold totals separately by type.

#### REQ-RPTMG-030 — In-House Use Reports

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** A single draft specification requests these reports and provides no explicit priority marker.

The system shall provide reports for non-cataloged in-house use counts by month and cataloged in-house use counts. Staff shall be able to review these in-house use measures in report form. This shall support analysis of library materials used on site.

#### REQ-RPTMG-031 — On-Demand Reports

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** On-demand reporting is described in a draft source and is included as a standard report category in survey results, but survey support for custom/on-demand reports is 29%.

The system shall provide preset reports that users can run on demand for maintenance reporting and collections development. These reports shall use preselected criteria to support repeatable report runs. This shall let staff request relevant reports when needed rather than waiting for a scheduled run.

#### REQ-RPTMG-032 — Periodic Operational Reports

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** The cited evidence is primarily a single draft request and does not establish a mandatory, legal, technical, or consistently demanded need; the listed reports can be delivered in a later increment.

The system shall support periodic reports for bibliographic records with holds and without item records; items not checked out in a specified number of days; item-level holds; invalid item types; and missing items. It shall also support reports for in-transit items with outstanding holds or in transit beyond a specified number of days, last-copy items, items with long call numbers, and patrons with invalid home libraries. These reports shall help reporting staff identify records and items that require operational attention.

#### REQ-RPTMG-033 — Prewritten Report Templates

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** A single draft source requests delivered templates, with no explicit priority evidence.

The system shall include a set of prewritten report templates delivered with the product. Users shall be able to select these templates as starting points for reporting. This shall provide ready-to-use reports without requiring every report to be created from scratch.

#### REQ-RPTMG-034 — Recurring Report Editing

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** A single draft specification requests editing recurring reports, with no separate priority evidence.

The system shall allow users to edit recurring reports. Users shall be able to add or remove report selections and change email recipient addresses. This shall let users maintain recurring report configurations as their needs change.

#### REQ-RPTMG-035 — Relative Date Ranges

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** A single draft specification requests the listed date-range options without an explicit priority marker.

The system shall allow users to run canned reports using relative date ranges. Supported ranges shall include yesterday, last week, last month, and last year. This shall make recurring time-period selections easier to apply consistently.

#### REQ-RPTMG-036 — Report Recipient Address Book

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** Requested in two sources, but one describes it as desirable and no blocking need is indicated.

The system shall provide an address book in which report schedulers can store and select regularly used email addresses. Users shall be able to select recipients from the address book when configuring report delivery. This shall reduce repeated entry of recipient addresses.

#### REQ-RPTMG-037 — Scheduled Purging Utility

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-06 (`conversations/conv_pines021_item_purging.eml`)
- **Priority rationale:** The capability is requested in one email thread, with an annual end-of-year example and no stated priority marker.

The system shall allow users to schedule the purging utility to run automatically at specified times. Scheduling shall support a recurring time such as the end of each year. This shall enable collection managers to automate planned purging or cleanup operations.

#### REQ-RPTMG-038 — Sent Notice Reports

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** The capability is specified in one draft specification and has no explicit priority marker.

The system shall provide reports for pre-overdue notices, overdue notices, and holds notices that were sent. Reporting staff shall be able to use these reports to review notice activity. The reports shall cover all three notice categories identified in the specification.

### 5.6 Analytical Reporting & Reporting Dimensions (ANALY)

_Core reporting analytics: grouping/aggregation levels, pivot/crosstab outputs, comparative date ranges and side-by-side views, trends, shelf-space proxy/reporting by category attributes, and demographic/inactivity/activity metrics._

#### REQ-ANALY-001 — Anonymized Demographic Reporting

- **Priority:** P1  ·  **Type:** constraint
- **Derived from:** DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** The source explicitly requires anonymization and prohibits personally identifiable information in demographic reports, establishing a hard privacy constraint.

The system shall anonymize demographic statistics in reports and shall not expose personally identifiable information. This constraint shall apply whenever demographic reporting is provided. It shall allow privacy and compliance officers to use aggregated demographic results without revealing individual identities.

#### REQ-ANALY-002 — Transaction Cross Tabulation

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Cross-tabulation is agreed in one source and explicitly marked high priority in another; transaction grouping is also requested in a survey.

The system shall allow analysts and staff to group and cross-tabulate transaction reports by terminal, branch, library system, hour, patron age range, patron type, and patron location. Users shall be able to query all transaction types or filter by transaction type, including check-ins, checkouts, fines collected, and patron registrations. These dimensions shall support analysis of transaction activity at different operational and patron levels.

#### REQ-ANALY-003 — Collection Composition Reporting

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-03 (`conversations/conv_pines016_shelf_space.eml`)
- **Priority rationale:** The breakdown was repeatedly requested and agreed in the source thread, and its counts and circulation totals were identified as required report data.

The system shall report collection and circulation metrics by genre and material format for collection managers and report users. It shall compute item counts by genre and format to show each category's percentage of the collection, and checkout totals by genre and format to show each category's percentage of total circulations. For the Shelf Space Report, users shall be able to group and aggregate results by genre, format, library, or system.

#### REQ-ANALY-004 — Comparative Period Analysis

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-03 (`conversations/conv_pines016_shelf_space.eml`), DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** Date-range filtering and comparisons were requested by collection planners and managers, and comparative circulation columns are specified in a separate reporting source.

The system shall allow users to filter the Shelf Space Report by an arbitrary date range, including quarters such as Q1 and Q2. It shall support comparing report results across selected date ranges to reveal changes over time. Comparative output shall be able to include last month's circulation, the previous month's circulation, the corresponding month of the previous year, and percentage differences between the periods.

#### REQ-ANALY-005 — Current-Data Reporting

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Real-time reporting is proposed in one source and specifically agreed for current-state reports in another.

For reports designated as requiring current data, the system shall include source transactions committed no more than five minutes before report generation begins. Each report shall display the data-through timestamp. If a source is unavailable or the five-minute freshness target cannot be met, the system shall identify the affected data and its timestamp rather than presenting it as current. Acceptance testing shall compare report contents and timestamps with committed source transactions.

#### REQ-ANALY-006 — Historical Reporting Data

- **Priority:** P2  ·  **Type:** data
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Historical reporting is raised in multiple sources, including a missing-feature reference and a later meeting action; the survey also specifies retention periods and aggregates.

The system shall support reporting on historical data, including billing data as of a specified past date and snapshots of bill amounts on that date. Retention for identifiable transaction history shall follow the configurable periods in the Financial Data Retention Policy, including applicable audit requirements and legal holds. De-identified monthly and annual aggregates shall follow the separate indefinite-retention rule for aggregate transaction information. Reports shall identify the date or period represented by the historical data.

#### REQ-ANALY-007 — Independent Item Dates

- **Priority:** P2  ·  **Type:** data
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`), DOC-15 (`interview_cataloging_2009-05-08.txt`)
- **Priority rationale:** Separate edit and circulation dates are requested in the reference document and a stakeholder interview, with agreement on the need to exclude circulation from edit dates.

The system shall provide last edit date and last circulation date as separate reportable item fields. The last edit date shall reflect the most recent bibliographic or item-record edit and shall not be updated by circulation events. Collection managers and catalogers shall be able to review editing and circulation activity independently.

#### REQ-ANALY-008 — Operational Trend Reporting

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-02 (`conversations/conv_pines015_capacity_interface.eml`), DOC-05 (`conversations/conv_pines019_020_missing_intransit.eml`)
- **Priority rationale:** Trend reporting is agreed for branch planning in one source and separately requested for collection decisions in another.

The system shall present trends over selectable time ranges to support planning and collection-management decisions. Trend reports shall show whether branches are growing or shrinking and shall support trending missing and damaged items. Users shall be able to use these results to identify changes over time and inform collection decisions.

#### REQ-ANALY-009 — Pivot Table Output

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Pivot-table output is requested in three separate sources, including a reference document identifying it as a missing feature.

The system shall provide report data in pivot-table-style output. The output shall support cross-tabulation and aggregation of report data and shall be available in a pivot-table-compatible format. Report users shall be able to use this format to examine and rearrange analytical results.

#### REQ-ANALY-010 — Staff Workflow Analysis

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)
- **Priority rationale:** The same analysis need appears in a draft specification and meeting minutes, although neither source assigns an explicit priority.

The system shall provide reports that allow authorized staff users and managers to review staff workflow by selected library, staff member, task type, and reporting period. Reports shall display transaction counts by task type and period, and shall identify the criteria used to produce the results. Acceptance testing shall verify the counts against a reference set of recorded transactions for each selected task type and period.

#### REQ-ANALY-011 — Transaction and Circulation Metrics

- **Priority:** P2  ·  **Type:** data
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`)
- **Priority rationale:** The activity metrics were agreed and requested for directors and boards; circulation breakdowns are also identified as useful reporting data.

The system shall provide reports of transactions for directors, boards, and report users, including checkouts, check-ins, holds placed, and holds filled. Reports shall show total circulation with separate counts for checkouts, renewals, and uncataloged material circulations. Each report shall identify its reporting period and scope so results can be used to monitor library use and compare circulation measures.

#### REQ-ANALY-012 — Data Quality Reports

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Priority rationale:** The need is stated in meeting minutes as necessary, but appears in only one source and has no explicit priority marker.

The system shall provide reports identifying records with missing required values, invalid codes, or inconsistent relationships between records. Each result shall identify the affected record, the field or relationship that failed validation, and the validation rule. Acceptance testing shall use a reference set containing known examples of each supported issue and verify that the report identifies those examples and does not report valid reference records as failures.

#### REQ-ANALY-013 — Edited Record Counts

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** The report is identified as missing in one reference source, with no explicit priority marker or additional source agreement.

The system shall provide a report counting item and bibliographic record edits during a period selected by an authorized staff user. The report shall identify the selected record type and period and return the count for that combination. Acceptance testing shall compare the reported counts with a reference set of edits whose record types and timestamps are known.

#### REQ-ANALY-014 — Hold Placement Source Reporting

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** The detail is an agreed survey request from one source, with no explicit priority marker.

The system shall record and report the placement method for each hold, with supported methods including staff desk, public computer inside a library, and remote placement. Reports shall provide both individual hold records with their placement method and aggregate hold counts grouped by placement method and reporting period. This shall allow authorized staff users to analyze hold placement patterns without combining distinct methods.

#### REQ-ANALY-015 — Library Comparison Reports

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-03 (`conversations/conv_pines016_shelf_space.eml`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Priority rationale:** The side-by-side view is a specific proposed request from one source, with no explicit high-priority marker.

The system shall provide a common report view for comparing selected metrics across multiple libraries for the same reporting period. The view shall label each library, metric, and period and display results together so directors and library managers can identify differences without assembling separate reports. The measures and comparison period shall be selectable from the report's supported criteria.

#### REQ-ANALY-016 — Separate Check-In and Renewal Records and Reporting

- **Priority:** P3  ·  **Type:** data
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** The unmet timestamp detail is listed in one reference source and has no explicit priority marker.

The system shall record renewal transactions separately from check-in transactions and expose separate date and time values for each. Reports shall distinguish check-ins from renewals and provide separate counts and timestamps so circulation staff and analysts can verify each transaction type independently.

#### REQ-ANALY-017 — Strategic Planning Reports

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)
- **Priority rationale:** The need is described across several proposed statements, but no explicit priority or agreement marker is provided.

The system shall provide library administrators, managers, and directors with aggregated reports for strategic planning, evaluation, and service decisions. Report users shall be able to review measures grouped by reporting period and library, and by collection where the measure supports that dimension. Reports shall label measures, groupings, and periods and shall support presentation of the resulting summaries to a library board.

#### REQ-ANALY-018 — Transaction Scope Reports

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** The report scopes are specified in one draft source and have no explicit priority or additional source agreement.

The system shall generate transaction reports for holds placed, holds filled, and checkouts. Users shall be able to scope these reports by patron, individual library, selected group of libraries, library system, or county. These scopes shall support analysis at both individual and broader organizational levels.

#### REQ-ANALY-019 — Voter Survey Reporting

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** The report is listed as a missing type in one reference source, with no explicit priority marker.

The system shall provide a report that collects and presents voter survey responses. Community engagement users shall be able to review the responses in report form. The report shall support the presentation of survey results for analysis.

### 5.7 Location & Consortium Multi-Location Reporting (LOCAP)

_Branch/system/region scope, cross-branch visibility, drill-downs, grouping branches by region/system, local-vs-system average comparisons, and centralized consolidation for multi-library operations._

#### REQ-LOCAP-001 — Centralized Multi-Location Operations

- **Priority:** P1  ·  **Type:** constraint
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** Centralized operation is repeated across four documents, including agreed meeting records, and establishes the architecture for serving multiple locations.

The system shall consolidate management processes at a central location. It shall accept input from multiple library locations and provide services to those locations. The centralized operation shall provide a single source of truth for multi-location management.

#### REQ-LOCAP-002 — Branch Capacity Drilldown

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-02 (`conversations/conv_pines015_capacity_interface.eml`)
- **Priority rationale:** Drilldown is agreed in the working-group summary and complements the requested overview; users could otherwise seek branch detail separately.

The system shall allow users to drill down from the high-level capacity overview into an individual branch's detailed capacity view. The detailed view shall provide branch-level information corresponding to the overview. This shall allow users to move from system-wide review to inspection of a specific branch.

#### REQ-LOCAP-003 — Consolidated Data Completeness and Freshness

- **Priority:** P2  ·  **Type:** non-functional
- **Derived from:** DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** Meeting notes identify completeness and currency across locations as a specific challenge to consolidated operation, though no measurable threshold or explicit priority is provided.

For each consolidated report, the system shall identify the libraries included, the data-through timestamp for each library, and any source data unavailable to the report. Data shall be considered current only when it meets the five-minute freshness target for reports designated as requiring current data. Acceptance testing shall compare report contents with source records and verify that missing or delayed library data is identified rather than presented as complete and current.

#### REQ-LOCAP-004 — Consolidated Material Volume Report

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-01 (`conversations/conv_pines014_material_volume.eml`)
- **Priority rationale:** The request is agreed and addresses a recurring manual task for a monthly board report, but the evidence is limited to one document and a workaround exists.

The system shall provide a consolidated material volume report that aggregates counts into a single report. Users shall be able to obtain the report without manually gathering the data from multiple screens. The report shall support users preparing monthly board reports.

#### REQ-LOCAP-005 — Inactive Patron Branch Reporting

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-09 (`conversations/conv_pines024_inactive_patrons.eml`)
- **Priority rationale:** Requested by multiple library stakeholders and agreed; the reporting supports branch-level cleanup, with other manual coordination possible as a workaround.

The system shall aggregate inactive-patron counts by home library for viewing at the system level. Users shall be able to drill down from those counts to branch-level lists so they can assign cleanup tasks to specific branches. The system shall allow the inactive-patron list to be generated or configured at organizational levels such as System, Home Library, and County, as well as other levels as needed.

#### REQ-LOCAP-006 — Library Capacity Overview

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-02 (`conversations/conv_pines015_capacity_interface.eml`)
- **Priority rationale:** The overview is agreed and supported by several candidate statements from the working group and branch stakeholders, including a need to see all branches at once.

The system shall provide an overview showing capacity information for all libraries in a library system. For each library, the overview shall display the available capacity metrics, including current load and capacity percentage. Report users shall be able to review the libraries and their metrics together to support capacity and resource decisions.

#### REQ-LOCAP-007 — Library Grouping and Filtering

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-02 (`conversations/conv_pines015_capacity_interface.eml`)
- **Priority rationale:** Grouping and sorting or filtering were requested in agreed working-group material, with the source noting 286 locations and the resulting visual crowding.

The system shall allow report users to group libraries by library system or configured region and to sort and filter them by region, library type, and current load. The overview shall label the selected grouping and filters. These controls shall allow report users to navigate and compare libraries in a consortium-scale overview.

#### REQ-LOCAP-008 — Library Location Report Filter

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-01 (`conversations/conv_pines014_material_volume.eml`)
- **Priority rationale:** The filter is agreed in the source summary and supports a specific library-level reporting need, with manual extraction as a possible workaround.

The system shall allow users to filter the material volume report by library location. When a library is selected, the report shall count only items whose location matches that library. This shall allow users to report on items at a given library at a point in time.

#### REQ-LOCAP-009 — Local System Average Comparison

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-03 (`conversations/conv_pines016_shelf_space.eml`)
- **Priority rationale:** Branch managers explicitly requested the comparison, and the source states its value for understanding local performance against the system average.

The system shall display a local library's Shelf Space Report results alongside the system average. Branch managers shall be able to compare local results with the system-level value. The comparison shall support review of the local library's situation in the context of the wider system.

#### REQ-LOCAP-010 — Shelf Space Report Scope

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-03 (`conversations/conv_pines016_shelf_space.eml`)
- **Priority rationale:** The requirement is agreed and supported by requests from multiple stakeholders, including directors who review the data quarterly and need both views.

The system shall allow users to run the Shelf Space Report for an individual library or for the entire system. Users shall be able to select the desired scope when generating the report. The two scopes shall support local review by branch managers and system-wide review by administrators and directors.

#### REQ-LOCAP-011 — Bibliographic Additions By Library

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** This missing report was identified in one reference document for cataloging managers, with no evidence of broader demand or a blocking need.

The system shall provide a report counting bibliographic records added by each user, grouped by library. Users shall be able to use the report to review record additions across library locations. The report shall present the counts in a form suitable for cataloging managers.

#### REQ-LOCAP-012 — Circulation Counts By Patron County

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** The report is listed as missing in one reference document for regional managers, with no further evidence of urgency or agreement.

The system shall provide circulation count reports grouped by circulation location and broken down by patron county. Regional managers shall be able to review circulation counts across locations using this county breakdown. The report shall retain the circulation location and patron county as distinct grouping dimensions.

#### REQ-LOCAP-013 — Consortium Administration And Reporting

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)
- **Priority rationale:** The capability is identified for a specific administrator role in one set of meeting minutes, without a priority marker or additional supporting sources.

The system shall provide Global System Administrators with consortium-level capabilities to implement software changes and configurations. They shall be able to generate statistical reports for the consortium as a whole. The system shall make these capabilities available for administration and reporting across the full consortium.

#### REQ-LOCAP-014 — Library Capacity Distribution Analysis

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)
- **Priority rationale:** The need appears in one set of meeting minutes without a stated priority or evidence of broader agreement.

The system shall provide reports showing capacity measures and collection distribution for selected libraries. Authorized staff users shall be able to select libraries and a reporting period and compare each library's configured capacity limit with its observed collection measure. Reports shall identify the measure, limit, observed value, and difference so users can assess distribution and capacity against explicit values.

#### REQ-LOCAP-015 — Library Manager Reporting Interfaces

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)
- **Priority rationale:** The capability is described for Library Managers in one set of meeting minutes and has no explicit priority marker or corroborating source.

The system shall provide Library Managers with interfaces and reporting features for supervising a single organizational unit. It shall support their contribution to the design and implementation of reports. The interfaces shall serve managers in their role overseeing a local unit.

#### REQ-LOCAP-016 — Local Administrator Configuration

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)
- **Priority rationale:** The local configuration role is identified in one set of meeting minutes without an explicit priority or evidence of broader demand.

The system shall allow Local System Administrators at local branches to configure the system locally. This capability shall support local management staff in carrying out their assigned configuration role. Local configuration shall be available within the system's multi-location operation.

#### REQ-LOCAP-017 — Transaction Totals By Organizational Scope

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** The need is recorded as agreed survey input from library staff, but the source provides no response counts or explicit priority evidence.

The system shall provide reports of total transactions aggregated per patron, per library, per group of libraries, per system, and per county. Users shall be able to review totals at the scope appropriate to their reporting needs. The report shall preserve these aggregation levels as distinct options.

### 5.8 OP Operations: Item Transfer, Revert & Transit Management (OPMIS)

_Batch transfer mechanisms and utilities (picklists/manual selection/query-driven candidate lists), audit/logging, preview/confirm, transaction safety, transit in-transit detection/thresholds/overdue rules, scheduled/conditional auto-revert, and undo for transfers including in-transit report variants._

#### REQ-OPMIS-001 — In-Transit Item Reporting

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-05 (`conversations/conv_pines019_020_missing_intransit.eml`), DOC-10 (`early_draft_srs_galecia.txt`), DOC-15 (`interview_cataloging_2009-05-08.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Priority rationale:** The report is explicitly called critical and is agreed or requested across multiple sources; branch and delivery staff rely on it for coordination and follow-up.

The system shall provide an in-transit report combining transit-to and transit-from information, including items in transit to a destination library and items in transit by sending library. The report shall identify items without a recorded arrival whose departure date is more than a configurable number of days ago, with a default threshold of 7 days. Authorized staff users shall be able to view results by library or library system and sort them by due date. The report shall identify item, sending library, destination library, departure date, and arrival status to support delivery coordination and follow-up.

#### REQ-OPMIS-002 — Batch Item Transfers

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-04 (`conversations/conv_pines018_item_transfer.eml`), DOC-10 (`early_draft_srs_galecia.txt`), DOC-15 (`interview_cataloging_2009-05-08.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Batch location changes and transfer utilities are requested in multiple documents by cataloging, logistics, and library staff; manual record updates offer a workaround.

The system shall provide staff with a utility to transfer batches of selected items between branches and to special locations, including mobile units and outreach collections. The utility shall update each selected item's location to the destination location as part of the transfer. It shall support changing item records in batches, rather than requiring staff to update each location individually.

#### REQ-OPMIS-003 — Delayed Transfer Alerts

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-04 (`conversations/conv_pines018_item_transfer.eml`)
- **Priority rationale:** The alert is a useful operational capability requested in one source, but the evidence does not establish a critical or mandatory need.

The system shall notify configured recipients when a transfer has no recorded arrival after its configured delay threshold or when a transfer operation records a failure or invalid transfer status. Configuration shall specify the delay threshold, recipient roles or addresses, and notification channel; the system shall identify the affected item, sending and destination libraries, detected condition, and detection time. The system shall retry a failed notification and retain its delivery status until delivery succeeds or an authorized staff user is alerted to intervene. Acceptance testing shall verify each condition, configured recipient and channel, and failed-delivery handling.

#### REQ-OPMIS-004 — Missing and Damaged Item Reports

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-05 (`conversations/conv_pines019_020_missing_intransit.eml`), DOC-10 (`early_draft_srs_galecia.txt`), DOC-15 (`interview_cataloging_2009-05-08.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Priority rationale:** Branch-level reporting is agreed as crucial for accountability and requested for inventory audits; additional filters and incident details support trending and collection decisions.

The system shall provide reports of missing and damaged items by library, including counts grouped by library and item-level results. Authorized staff users shall be able to select date ranges and filter by status, including missing, lost, and long overdue, and review item condition notes. Reports shall support auditing and collection decisions, including identifying items with repeated incidents for replacement or relocation.

#### REQ-OPMIS-005 — Scheduled Transfer Reversion

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-04 (`conversations/conv_pines018_item_transfer.eml`), DOC-10 (`early_draft_srs_galecia.txt`), DOC-15 (`interview_cataloging_2009-05-08.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Timed reversion is requested across several sources, including a survey, and supports temporary transfers; staff may otherwise revert locations manually.

The system shall allow authorized staff to return transferred items to their original location automatically after a configurable period or on a specified event, such as an item's status changing to "returned" or "sold". For temporary transfers to an event or program, staff shall be able to specify an end date that triggers reversion. The system shall support scheduled processing of these time- and event-based rules, while leaving an item at its destination if it has been checked out there. Staff shall also be able to revert an item to its original location when needed.

#### REQ-OPMIS-006 — Transfer Audit History

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-04 (`conversations/conv_pines018_item_transfer.eml`)
- **Priority rationale:** Transfer logging and item-level history are requested by different stakeholders in the same source; audit and accountability are important, though some history may be tracked manually.

The system shall record transfer actions and item location changes for audit purposes, including who performed each transfer and when. It shall retain transfer history for each item, including transfer timestamps and the number of times the item has been transferred. Authorized users shall be able to review this history to support auditing and collection decisions.

#### REQ-OPMIS-007 — Item Status Conversion Report

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** The report is requested in one draft specification and supports a specific cataloging workflow.

The system shall provide a report to assist authorized staff users with batch conversion of item statuses. The report shall identify the items and their current statuses relevant to the intended status change, allowing staff to review the items before performing the batch conversion. This requirement covers the status-conversion report, not authorization or execution safeguards for the conversion operation.

#### REQ-OPMIS-008 — Printable Transfer Pull Lists

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-04 (`conversations/conv_pines018_item_transfer.eml`)
- **Priority rationale:** Pull lists are requested in two documents as a transfer mechanism, but staff can prepare retrieval lists by other means.

The system shall generate a printable pull list of items to be moved in a transfer batch. Staff shall be able to use the list to retrieve the items for physical transfer. This shall support the picking and logistics work that accompanies a transfer.

#### REQ-OPMIS-009 — Printable Transit Labels

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-04 (`conversations/conv_pines018_item_transfer.eml`)
- **Priority rationale:** This is a single-source operational convenience that can be supported by other labeling methods if not delivered.

The system shall generate printable transit labels for items in a transfer. Each label shall include a barcode associated with the item. Staff shall be able to print the labels for use while handling and routing transferred items.

#### REQ-OPMIS-010 — Separate Report Documentation

- **Priority:** P3  ·  **Type:** documentation
- **Derived from:** DOC-05 (`conversations/conv_pines019_020_missing_intransit.eml`)
- **Priority rationale:** The reports working group agreed to track the two reports separately in documentation; this is a specific documentation need rather than a system operation.

The system documentation shall record the Missing and Damaged Items report and the In-Transit Items report as separate entries. It shall preserve their distinction even though both reports relate to item movement or condition. This shall make each report requirement identifiable and trackable in the documentation.

#### REQ-OPMIS-011 — Transfer Preview Confirmation

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-04 (`conversations/conv_pines018_item_transfer.eml`)
- **Priority rationale:** A single source proposes a concrete safeguard that reduces transfer errors; staff can otherwise check batches manually.

Before executing a transfer batch, the system shall show staff a preview and request confirmation. The preview shall state the number of items to be moved and the source and destination locations. This shall give staff an opportunity to catch an incorrect selection or destination before changes are made.

#### REQ-OPMIS-012 — Transfer Undo

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-04 (`conversations/conv_pines018_item_transfer.eml`)
- **Priority rationale:** Undo is requested in one source as protection against mistakes, while manual correction provides a workaround.

The system shall allow authorized users to undo a recent transfer operation. Undo shall reverse the location changes made by that operation. This shall enable staff to recover from an accidental transfer without correcting each item individually.

#### REQ-OPMIS-013 — Uncataloged Shipment Processing

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-15 (`interview_cataloging_2009-05-08.txt`)
- **Priority rationale:** This efficiency need comes from one stakeholder interview and is useful for a specific shipment workflow, but is not described as blocking other transfers.

The system shall provide a bulk distribution and processing mode for uncataloged shipments. It shall enable staff to distribute these shipments quickly while minimizing the per-item labor required at branches. This capability shall support rapid processing before items are cataloged.

#### REQ-OPMIS-014 — Indirect Patron Access to Report Output

- **Priority:** P4  ·  **Type:** functional
- **Derived from:** DOC-17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)
- **Priority rationale:** This access model appears in one meeting-minutes source and is framed as a possible indirect use rather than a core operational need.

The system shall allow libraries to display selected report output on screens intended for patrons without providing patrons with access to reporting functions or underlying report data. Patron interactions with library services shall remain primarily through the OPAC. Acceptance testing shall verify that displayed output contains only the information selected for public display and does not expose restricted patron information.

### 5.9 Purge/Weeding & Deletion Utilities (PURGE)

_Weeding/purge candidate identification with customizable criteria, read-only previews, safeguards to prevent accidental mass deletion, scheduling, deletions with DB triggers/audit persistence, reporting/audit trails, last-copy and WorldCat-support deletion lists, and orphaned record handling._

#### REQ-PURGE-001 — Deletion Activity Reporting

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-07 (`conversations/conv_pines022_deletions.eml`), DOC-10 (`early_draft_srs_galecia.txt`), DOC-15 (`interview_cataloging_2009-05-08.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** The agreed reporting request was called an administrative requirement and described as something stakeholders “absolutely need” for compliance; it is supported by several stakeholders and a survey request from 27% of respondents.

The system shall provide reports and queries over deletion audit records so administrators can monitor deletion activity and investigate specific events. Reports shall show total deletions by month, quarter, or year; deletions by record type (including items, patrons, and other records); deletions by location; and the users with the most deletions, with views per system and per location. Users shall be able to filter or aggregate results by date range, user, and record type, retrieve entries for a specific record_id, and review deletion reasons; the system shall count and track deletions per location and system.

#### REQ-PURGE-002 — Last-Item Identification and Pre-Deletion Reports

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-06 (`conversations/conv_pines021_item_purging.eml`), DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`), DOC-15 (`interview_cataloging_2009-05-08.txt`)
- **Priority rationale:** The agreed requirement is explicitly marked “CRITICAL,” and multiple participants requested both per-library and per-system views to avoid deleting a consortium's only copy.

The system shall provide a report identifying items that are the last item within a selected library, library system, or consortium scope. Authorized staff users shall be able to review current last-item status and use the report in a pre-deletion workflow before an authorized purge. Results shall provide item identifiers and actionable details to support cataloging, preservation, and external-catalog decisions.

#### REQ-PURGE-003 — Batch Item Status Conversion

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-06 (`conversations/conv_pines021_item_purging.eml`), DOC-15 (`interview_cataloging_2009-05-08.txt`)
- **Priority rationale:** Cataloging staff described batch conversion as a major time-saving need, and the item-report specification also includes items to be converted; the sources indicate substantial operational benefit.

The system shall allow authorized staff members to select multiple items and change their status in one batch operation, including changing items from missing to discard/weed. Before applying the change, the system shall show the selected item count and the source and destination statuses and require confirmation. Acceptance testing shall verify that the change applies only to the selected items and that items with an invalid status transition are identified rather than silently changed.

#### REQ-PURGE-004 — Bulk Related Record Deletion

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-06 (`conversations/conv_pines021_item_purging.eml`), DOC-10 (`early_draft_srs_galecia.txt`), DOC-15 (`interview_cataloging_2009-05-08.txt`)
- **Priority rationale:** The need is agreed across an email thread and repeated in a stakeholder interview and draft specification; a manual workaround exists but is described as time-consuming.

The system shall provide an efficient utility for authorized cataloging staff and administrators to delete volume entries together with their associated copy entries. The utility shall also identify and delete bibliographic or other records that have no item records attached. These operations shall support cleanup of related and orphaned records without requiring staff to locate and delete each record through a slow manual process.

#### REQ-PURGE-005 — Customizable Weeding Reports

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`), DOC-15 (`interview_cataloging_2009-05-08.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Priority rationale:** Weeding reports are described as frequently used and as the interviewee’s most-used report type, with related needs appearing in both a draft specification and stakeholder sources.

The system shall provide weeding reports that identify items for review using criteria configurable by authorized report users. Criteria shall include an item remaining in the missing status for more than a configurable number of months and items in the discard/weed status, as defined by the Library Automation System's status codes. Each report shall include the date of the item's last circulation. A report shall identify items for review only; it shall not itself purge or delete items.

#### REQ-PURGE-006 — Deletion Audit Trail

- **Priority:** P2  ·  **Type:** data
- **Derived from:** DOC-06 (`conversations/conv_pines021_item_purging.eml`), DOC-07 (`conversations/conv_pines022_deletions.eml`)
- **Priority rationale:** Agreed audit needs appear in multiple stakeholder communications and support accountability and compliance, although no source marks the audit trail as critical or mandatory.

The system shall maintain persistent audit records for purge-related deletions and denied deletion attempts so administrators and auditors can establish what happened and who performed or attempted the action. Each deletion record shall include record_type, record_id, deleted_by, deleted_at, and location, and the audit trail shall identify the actor and timestamp for denied attempts. The system shall support optionally recording an item's status before deletion; deletion reasons shall be captured as specified in Deletion Activity Reporting.

#### REQ-PURGE-007 — Deletion Confirmation Step

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-06 (`conversations/conv_pines021_item_purging.eml`)
- **Priority rationale:** The confirmation safeguard was agreed by cataloging staff and administrators and addresses the significant risk of unintended deletion, although it is stated in one source.

The system shall require users to complete a separate, explicit confirmation step before performing deletions identified by purge reports. The confirmation shall occur after candidate identification and review, rather than being implicit in viewing or running a report. This safeguard shall help prevent accidental execution of purge actions.

#### REQ-PURGE-008 — Read-Only Purge Preview

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-06 (`conversations/conv_pines021_item_purging.eml`)
- **Priority rationale:** The safeguard was agreed by cataloging staff and managers and reduces the risk of accidental deletion, though only one source explicitly requests this preview.

The system shall display purge candidates in a read-only preview before deletion. Users shall be able to review the candidate report without being able to delete records directly from that report. This separation shall help staff inspect proposed purge actions before proceeding to a deletion operation.

#### REQ-PURGE-009 — Deleted Last-Item Reports

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** The report is requested in draft specifications to support external catalog maintenance, but the evidence is limited to one source and no critical priority marker is given.

The system shall provide a report listing items that were purged even though they were the last item owned within the relevant library system. The report shall identify each item and the affected library system so authorized staff users can review the records and update WorldCat or other external catalog records after the purge.

#### REQ-PURGE-010 — Predefined Item Reports

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** The report catalogue is specified in a single draft specification and provides useful operational coverage, but no evidence marks the full catalogue as critical.

The system shall provide predefined item reports for Items Added Count, List of Items Added, Items Edited Count, Items Count, Items Deleted Count, Lists by Fines Stopped Reason, Items Currently Checked Out, Items more than a configurable number of days overdue, Items marked longoverdue, Long Overdue lists, Items in Transit by sending and destination library, Claims returned, Lists by Creation Date Range, Lists with status Missing, Lists by Total Use Count thresholds, a Last Copy Report, a Weeding Report showing date of last circulation and number of circulations, Lists with a specified value in the bibliographic record, Age of collection by call number or shelving location, Price value of collection by call number or shelving location, and Items to be Converted. The reports shall support collection management and operational review, including weeding and identifying items for batch status conversion.

### 5.10 Finance & Transaction Reporting (Fines/Payments/Accounting) (ACCT)

_Financial tracking and reporting: fines/charges by time/type, waived fines, snapshot/history, payments and instruments, ledger/audit trails, patron account balances, outstanding thresholds, and attachment/joining of financial transactions to records._

#### REQ-ACCT-001 — Accounting and Audit Compliance

- **Priority:** P1  ·  **Type:** constraint
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-11 (`email_financial_reports.eml`)
- **Priority rationale:** The source explicitly says reports and archiving must comply with accounting and governmental auditing requirements.

The system shall support financial reports and archived financial data in compliance with applicable accounting and governmental auditing requirements. Before compliance acceptance, the project shall identify the governing accounting standards and applicable state, county, and municipal audit provisions in a controlled compliance register, with exact document, section, and version references. Acceptance testing shall verify the applicable reporting and retention obligations against that approved register.

#### REQ-ACCT-002 — Auditable Payment Ledger

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-11 (`email_financial_reports.eml`), DOC-17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)
- **Priority rationale:** The agreed finance and auditor requirement explicitly marks payment traceability as critical for reconciliation; a related draft also requests transaction tracking and verification.

The system shall maintain an auditable ledger of patron payments that identifies each payment and the specific charge or charges to which it was applied. Finance staff and auditors shall be able to use the ledger and related tools or reports to track and verify financial transactions. The ledger shall provide traceability needed to reconcile accounts.

#### REQ-ACCT-003 — Financial Data Retention Policy

- **Priority:** P1  ·  **Type:** constraint
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-11 (`email_financial_reports.eml`)
- **Priority rationale:** The agreed source identifies legally or policy-required retention, including a seven-year audit period, and explicitly requires the system to enforce it.

The system shall enforce configurable retention periods by financial data category. Where the approved legal or policy requirement specifies a seven-year audit period, the system shall apply that period to the applicable records; other categories shall use their approved periods. De-identified aggregate transaction information shall be governed by the applicable policy and law, not assumed to be exempt from deletion. An authorized legal hold shall suspend deletion for affected records, and the system shall record policy changes and deletion actions. The approved retention schedule shall identify the governing authority and applicable data categories before compliance acceptance.

#### REQ-ACCT-004 — Bills and Debt Reports

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** The specified report set supports routine finance work, but it is requested in one draft source and has no explicit high-priority marker.

The system shall provide bills reports for staff members and finance staff members. The reports shall include bills currently owed by patrons, detailed payments received, forgiven amounts, payments made using work credit, payments made using goods credit, detailed voids, and aged debt. Each report shall label these categories separately so staff members can distinguish payments, credits, and forgiven amounts when reviewing outstanding bills and payment activity.

#### REQ-ACCT-005 — De-Identified Aggregate Transaction Retention

- **Priority:** P2  ·  **Type:** data
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** Indefinite retention is explicitly requested in the draft specification, though it appears in only one source.

The system shall retain monthly and annual aggregate transaction information only after it has been de-identified so it cannot identify a patron. Retention and deletion of these aggregates shall follow the applicable approved retention policy and legal requirements; this requirement does not establish indefinite retention or override a legal hold. The system shall record retention-policy changes and any resulting deletion actions.

#### REQ-ACCT-006 — Financial Data Joining

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-11 (`email_financial_reports.eml`)
- **Priority rationale:** The later source records an agreed need from finance and reporting staff to join the two financial data sources for reporting.

The system shall allow reporting users to join financial data associated with patron records to financial data associated with item records. The joined data shall be usable to combine or correlate those sources in financial reports. This supports reporting across the patron and item dimensions of financial activity.

#### REQ-ACCT-007 — Financial Record Associations

- **Priority:** P2  ·  **Type:** data
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-11 (`email_financial_reports.eml`)
- **Priority rationale:** The need appears in both the draft specification and a later agreed source, with finance and reporting staff identified as stakeholders.

The system shall associate fines, charges, waivers, and ecommerce transactions with the relevant patron and item records. Finance staff members and report users shall be able to use these associations when reviewing financial activity. Acceptance testing shall verify that each supported transaction type is linked to the correct patron and item records when those records exist.

#### REQ-ACCT-008 — Financial Summary and Library Reports

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-11 (`email_financial_reports.eml`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Priority rationale:** The reporting needs are described across draft and later agreed sources, with finance, branch, and director stakeholders identified; the reports support routine reconciliation and budget monitoring.

The system shall provide financial reports for finance staff, authorized staff users at libraries, and library directors. Reports shall show patron account balances by patron, home library, and library system; fines and charges by period and charge type; fines waived by period and library; and payments by period, payment instrument, and collection channel. The reports shall support end-of-month and other reporting by identifying the library where a payment was collected and the library to which it is attributed.

#### REQ-ACCT-009 — Financial Transaction Update Latency

- **Priority:** P2  ·  **Type:** non-functional
- **Derived from:** DOC-11 (`email_financial_reports.eml`)
- **Priority rationale:** The need was agreed by front desk and finance staff, who specifically report that delayed updates impede their work.

The system shall reflect a committed financial transaction, including a front-desk payment, in account balances and reports designated as current within five minutes of the transaction commit. Such reports shall display their data-through timestamp. If the transaction is not available within that interval, the system shall identify the affected data as delayed rather than presenting it as current. Acceptance testing shall measure elapsed time from transaction commit to report availability.

#### REQ-ACCT-010 — Patron Balance Threshold Queries

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-11 (`email_financial_reports.eml`)
- **Priority rationale:** The agreed source says this was repeatedly requested and that manual retrieval currently takes too long, indicating an important daily-work need with a manual workaround.

The system shall allow an authorized staff user to query patron accounts whose balances exceed a threshold amount specified for each query. The result shall identify the patron accounts meeting the threshold and support review of accounts requiring attention. The query shall not use a fixed threshold.

#### REQ-ACCT-011 — Editable Financial Information

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** Ease of updating is requested in one draft source without a specific workflow, urgency marker, or evidence of broader agreement.

The system shall allow authorized staff members to select a financial record, edit permitted fields, review the proposed changes, and save or cancel the update. The system shall validate required fields before saving and identify validation failures to the staff member. Acceptance testing shall verify that authorized staff members can update permitted fields and that unauthorized changes are rejected.

#### REQ-ACCT-012 — Historical Bill Snapshots

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** The capability is listed as an unmet need in one reference document, without an explicit high-priority marker or broader stakeholder agreement.

The system shall provide a snapshot bills report that shows bill states as they existed at earlier points in time. Finance and reporting users shall be able to review historical snapshots rather than only current bill states. This supports investigation and comparison of past financial positions.

### 5.11 Collections, Circulation & Capacity/Inventory Analytics (CALCD)

_Collection usage and volume analytics (acquisitions, circulation breakdowns, item counts by status/genre/format), item value and price/call-number aging, hold counts, uncataloged material tracking, and capacity/shelf-space utilization with color-coded status and central database aggregation._

#### REQ-CALCD-001 — Circulation Activity Reporting

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Activity reporting is requested in a draft specification and survey results, with specific breakdowns requested by library staff; a manual reporting workaround is possible.

The system shall provide activity reports showing counts of check-outs, check-ins, holds placed, and holds filled. It shall also report transaction types including fines collected and patron registrations, as well as check-in counts by method, including book drop, terminal, and self-service. The system shall report check-out and renewal types separately, including staff checkout, self checkout, staff renewal, self checkout renewal, online renewal, and OPAC renewal, so staff and management can understand circulation activity and service use.

#### REQ-CALCD-002 — Collection Value Reporting

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-11 (`email_financial_reports.eml`), DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** Value reporting is requested in a draft specification and an agreed finance/staff email, which identifies purchase price data already present in item records.

The system shall generate reports of monetary item value using the purchase price field in item records, querying and aggregating that field as needed. Users shall be able to report value for the entire collection or a selected portion, with filters including item status, material type, and collection membership; examples include long-overdue items and children's DVDs. The system shall also report collection value aggregated by call number ranges to support collection and finance analysis.

#### REQ-CALCD-003 — Collection Volume History

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-01 (`conversations/conv_pines014_material_volume.eml`), DOC-10 (`early_draft_srs_galecia.txt`), DOC-15 (`interview_cataloging_2009-05-08.txt`)
- **Priority rationale:** The collection history capability is requested across multiple sources and supports important board and assessment reporting, but a temporary workaround exists and the evidence does not establish a mandatory constraint.

The system shall provide a collection volume report for a specified library and date or point in time, including historical counts rather than only current values. The report shall distinguish new acquisitions, items on the shelf, and items out in circulation, and shall include checked-out items in the total volume. It shall use the item acquisition date for acquisition and time-range reporting, show changes over time, and allow recent-addition intervals such as the last 30, 60, or 90 days. Users shall be able to report on acquisitions, shelf items, and circulating items with category breakdowns including total items, holds, adult fiction, and board books.

#### REQ-CALCD-004 — Library Capacity Analysis

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-02 (`conversations/conv_pines015_capacity_interface.eml`), DOC-10 (`early_draft_srs_galecia.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Priority rationale:** Branch capacity analysis is requested in the draft specification and technical email, and meeting minutes state that inventory and capacity reports are used daily.

The system shall provide capacity reports for selected libraries and a consolidated view across selected libraries. Reports shall identify each library, the configured capacity measure, the observed value, the capacity limit, and the difference between the observed value and limit. Authorized staff users shall be able to select the reporting scope and period; acceptance testing shall verify displayed values against configured limits and reference inventory data.

#### REQ-CALCD-005 — Shelf Space Utilization Analysis

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-03 (`conversations/conv_pines016_shelf_space.eml`), DOC-10 (`early_draft_srs_galecia.txt`), DOC-15 (`interview_cataloging_2009-05-08.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Priority rationale:** The comparison is requested in multiple sources, including an agreed working-group summary and a stakeholder interview, and is described as important for collection management.

The system shall provide shelf-space utilization reports for each genre and format, comparing the percentage of total circulations, the percentage of the collection, and the percentage of total shelf space. Reports shall be runnable for an individual library and for the library system. The system shall estimate shelf space by genre and format using item dimensions when available and item count as a proxy when dimensions are unavailable, so planners can assess the percentage of shelf space occupied.

#### REQ-CALCD-006 — Uncataloged Material Inventory

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-15 (`interview_cataloging_2009-05-08.txt`)
- **Priority rationale:** The need is described in both a draft specification and a stakeholder interview, with concrete operational needs for distribution and inventory tracking.

The system shall allow staff to track uncataloged material as inventory even when individual bibliographic records are unavailable. It shall support material such as paperback books and children's board books, and shall support quick distribution with minimal branch labor. This inventory capability shall allow branch staff and collection managers to control and locate uncataloged material.

#### REQ-CALCD-007 — Uncataloged Material Usage

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-15 (`interview_cataloging_2009-05-08.txt`)
- **Priority rationale:** Transaction counting is requested in both a draft specification and a stakeholder interview, and the interview also requests usage information.

The system shall count transactions involving uncataloged material and include those counts in circulation statistics and reports. It shall record and report how uncataloged material is used so staff can evaluate its circulation and use. The system shall support this reporting even when the material is not fully cataloged.

#### REQ-CALCD-008 — Circulation Count Breakdowns

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** Four distinct report types are listed as missing or partially available in one reference source, but no priority marker or broad stakeholder agreement is stated.

The system shall provide circulation count reports grouped by patron age demographic, circulation modifier, Dewey classification, and MARC field values. Users shall be able to select the relevant breakdown when reviewing circulation counts. These reports shall support collection and circulation analysis using the classification and record data identified in the sources.

#### REQ-CALCD-009 — Claims Returned Reporting

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** This report is listed as unavailable in one reference source, with no stated priority marker or supporting source.

The system shall provide a Claims Returned report listing items that patrons have claimed to have returned. Circulation staff shall be able to use the report to identify and review those items. The report shall make claims-returned information available as a distinct report type.

#### REQ-CALCD-010 — Collection Age By Call Number

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** The report is listed as missing in one reference source and has no explicit priority marker.

The system shall provide a report showing the age of the collection aggregated by call number ranges. Collection managers shall be able to use the report to assess the age profile of holdings across those ranges. The report shall use collection item data to calculate the grouped results.

#### REQ-CALCD-011 — Collection Usage Analysis

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)
- **Priority rationale:** The need appears in two sources, but neither identifies a priority marker or a specific operational blocker.

The system shall provide collection managers and librarians with reports and analysis tools for examining the library collection and how patrons use it. The analysis shall support collection-management decisions by making collection holdings and patron use available for review. It shall allow users to analyze collection usage without requiring a specific report format.

#### REQ-CALCD-012 — Configurable Capacity Metrics

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-02 (`conversations/conv_pines015_capacity_interface.eml`)
- **Priority rationale:** A working-group discussion identifies capacity metrics as an input needed for the interface, but the request remains questioned and has no explicit priority marker.

The system shall allow authorized users to define and configure the metrics used to represent capacity. Supported metric choices shall include item count versus shelf space, physical item count versus a configured limit, and circulation volume versus processing capacity. The system shall use the selected metric when presenting capacity information so that branches can apply a consistent, meaningful definition of capacity.

#### REQ-CALCD-013 — Item Use Count Reporting

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** Use counts and filtering by a specified count are requested in a draft specification and a reference report list, without explicit priority markers.

The system shall maintain and report total use counts for items. It shall also provide use counts by date range, including fiscal-year and monthly counts. Collection analysts shall be able to identify items matching a specified total use count.

#### REQ-CALCD-014 — Items By Creation Date

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** This report is listed as unavailable in one reference source and has no explicit priority marker.

The system shall provide a report listing items created within a specified creation-date range. Inventory managers shall be able to use the report to identify items added during the selected period. The report shall allow the user to specify the date range used to select items.

#### REQ-CALCD-015 — Items By Fines Stopped

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** This report is listed as unavailable in one reference source, with no additional evidence of priority.

The system shall provide a report listing items grouped by the reason fines were stopped. Circulation and finance staff shall be able to review the items and their associated reasons. The report shall make the fines-stopped reason available as a grouping criterion.

#### REQ-CALCD-016 — Last Circulation Date

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** This is a single survey request with no explicit priority marker or evidence of broad agreement.

The system shall indicate the last circulation date on item reports. Collection and circulation staff shall be able to use this date when reviewing individual items. The report shall display the date associated with the item's most recent circulation.

#### REQ-CALCD-017 — Overdue Items With Contact

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** The report is listed as unavailable in one reference source; the overdue threshold is specified as configurable but no priority marker is provided.

The system shall provide a report of items that are more than a user-specified number of days overdue. The report shall include patron contact information for each item. Circulation staff shall be able to use the report to identify overdue items requiring follow-up.

#### REQ-CALCD-018 — Unfilled and Stale Holds Reporting

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** Stale holds are listed as an unavailable report type in one reference source, with no stated priority marker.

The system shall provide reports for unfilled holds and stale holds. An unfilled hold is a hold that has not been fulfilled; a stale hold is an unfilled hold that has remained unfulfilled beyond a report-user-configurable age threshold. Report users shall be able to select the threshold and identify which category each result meets. Acceptance testing shall verify that all stale holds are included among unfilled holds and that unfilled holds below the threshold are not classified as stale.

#### REQ-CALCD-019 — Volume Category Breakdowns

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-01 (`conversations/conv_pines014_material_volume.eml`)
- **Priority rationale:** The cited evidence is primarily a draft or email request and does not establish a legal, technical, mandatory, or consistently demanded need. The capability is useful but can be delivered after core reporting.

The system shall allow users to break down collection volume by categories including total items, holds, adult fiction, and board books. It shall support grouping by category attributes such as fiction or non-fiction and format, and shall allow each library to customize the categories used. The report shall show hold counts per category so collection managers can examine volume using categories relevant to their library.

#### REQ-CALCD-020 — Configurable Color-Coded Capacity Status

- **Priority:** P4  ·  **Type:** functional
- **Derived from:** DOC-02 (`conversations/conv_pines015_capacity_interface.eml`)
- **Priority rationale:** Color coding is proposed as a usability enhancement in one source, with no evidence that it is required for core operation.

The system shall display capacity status using green, yellow, and red indicators based on library-configured capacity thresholds. The configuration shall define the numeric boundary for each status, with green below the yellow boundary, yellow from that boundary to the red boundary, and red at or above the red boundary. Acceptance testing shall verify the displayed status immediately below, at, and above each configured boundary.

### 5.12 Patron Analytics & Demographic/Inactivity Reporting (STKID)

_Patron demographics/behavior statistics, age calculation and configurable age ranges, last activity computation, inactivity thresholds, inclusion/exclusion of nulls/blanks, outstanding fines handling, inactivity/low-balance list generation, and completeness indicators for patron report outputs._

#### REQ-STKID-001 — Patron Characteristic Filtering and Grouping

- **Priority:** P1  ·  **Type:** functional
- **Derived from:** DOC-08 (`conversations/conv_pines023_patron_characteristics.eml`), DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** The reporting working group agreed on these characteristics, and a stakeholder explicitly called the capability essential; patron-type categories are also identified as important.

The system shall allow report users to filter and group queries and reports by patron age range, ZIP code, county of residence, home library, patron type, and preferred language. Patron type shall support categories such as adult, juvenile, senior, and student. Acceptance testing shall verify that each characteristic can be selected as a filter and grouping field and that results reflect the selected criteria.

#### REQ-STKID-002 — Combined Demographic Activity Filters

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-08 (`conversations/conv_pines023_patron_characteristics.eml`)
- **Priority rationale:** The combined-filter need was agreed in an email thread, and technical feasibility was confirmed, but it appears in one source.

The system shall let report users combine demographic criteria with activity-based conditions in a single query. Conditions shall support examples such as juvenile patrons in zip code 30505 who have not checked anything out in six months. This shall allow users to identify targeted patron groups without running separate reports and manually combining results.

#### REQ-STKID-003 — Configurable Age-Based Reporting

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-08 (`conversations/conv_pines023_patron_characteristics.eml`)
- **Priority rationale:** Age calculation feasibility was confirmed and configurable age ranges were agreed in the same reporting discussion, though no mandatory marker or broad survey support is given.

The system shall calculate a patron's age at query time from the stored birth_date field. Report users shall be able to configure age ranges for each report and use those ranges for filtering and grouping. Configurable examples include 0–5, 6–10, 11–15 and 0–6, 7–12, 13–17, 18–24, and 25–34.

#### REQ-STKID-004 — Configurable Inactive Patron Reports

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-09 (`conversations/conv_pines024_inactive_patrons.eml`), DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** The inactive-patron report is requested in multiple sources and the threshold is agreed as configurable; a listed report is also identified as unavailable.

The system shall generate a list of patrons with no circulation or electronic activity during a number of days specified by a report user. The report user shall be able to enter any number of days and select presets of 30, 90, 180, or 365 days, with report scope options including library system, home library, and county. The output shall identify the selected inactivity threshold and the patron records meeting it.

#### REQ-STKID-005 — Demographic Statistics and Privacy

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-08 (`conversations/conv_pines023_patron_characteristics.eml`), DOC-10 (`early_draft_srs_galecia.txt`), DOC-12 (`email_report_features.eml`), DOC-14 (`evergreen_reference_2009.txt`), DOC-17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Demographic analysis is requested across a draft specification, meeting minutes, email, and survey; the sources also explicitly call for anonymized data, but do not mark the overall capability mandatory.

The system shall provide demographic statistics to support program planning and analysis of patron demographics and interests. Statistics shall include transactions by geographic region, county, city, ZIP code, and age range, as well as patron and circulation aggregates grouped by demographic fields. The system shall use de-identified data for these statistics and shall not expose patron-identifying information in the reported results.

#### REQ-STKID-006 — Inactive Patron Exclusion Criteria

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-09 (`conversations/conv_pines024_inactive_patrons.eml`)
- **Priority rationale:** An agreed email thread gives an explicit list of exclusion categories for report users, but the request is from one source.

The system shall let users exclude selected patron categories from inactive-patron reports. Exclusion criteria shall include do-not-disturb flags, VIP status, staff membership, and opting out of communications. This shall allow users to limit report results to patrons appropriate for the intended follow-up.

#### REQ-STKID-007 — Inactive Patron Mailing Addresses

- **Priority:** P2  ·  **Type:** data
- **Derived from:** DOC-09 (`conversations/conv_pines024_inactive_patrons.eml`)
- **Priority rationale:** Outreach staff explicitly request current mailing addresses for a stated postcard workflow in an agreed source.

The system shall include each inactive patron's current mailing address in the inactive-patron report. The address shall be available to outreach staff using the report to mail postcards. The report shall use the patron's current address information.

#### REQ-STKID-008 — Inactive Report CSV Export

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-09 (`conversations/conv_pines024_inactive_patrons.eml`)
- **Priority rationale:** The CSV format and outreach-system use are explicitly requested by multiple stakeholders in an agreed email thread.

The system shall allow users to export the inactive-patron report as a CSV file. The export shall contain the report results in a format suitable for upload to outreach systems. This shall support the stated workflow of using the report for patron outreach.

#### REQ-STKID-009 — Null Values In Report Results

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-08 (`conversations/conv_pines023_patron_characteristics.eml`)
- **Priority rationale:** The reporting working group agreed that null values should be included, with multiple participants supporting the approach to prevent misleading results.

The system shall include records with null values for optional patron fields in report results rather than silently excluding those records. The report shall display missing values explicitly as null. This shall help users interpret results without misleading omissions caused by incomplete patron data.

#### REQ-STKID-010 — Patron Activity Data Integration

- **Priority:** P2  ·  **Type:** data
- **Derived from:** DOC-09 (`conversations/conv_pines024_inactive_patrons.eml`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Priority rationale:** Multiple participants agreed that inactivity must account for electronic activity as well as circulation, and implementer notes identify the combined query needed to retrieve it.

The system shall determine each patron's most recent activity date using circulation transactions and available electronic-activity data from the relevant tables. Electronic activity shall include OPAC or patron-account logins, online holds, online renewals, and digital-collection access when integrated. The system shall query OPAC patron data, including holds and circulation, and combine the sources to support reporting.

#### REQ-STKID-011 — Patron Behavior Analytics

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Similar behavior-analysis needs and example metrics appear in both a draft specification and survey results, indicating support across two sources.

The system shall produce statistics to help users understand and predict patron behavior and use of materials. Metrics shall include average time to return an item, renewal likelihood or probability, and the percentage of check-outs that are renewals. Users shall be able to analyze the renewal percentage for a particular branch.

#### REQ-STKID-012 — Patron Reporting Data Fields

- **Priority:** P2  ·  **Type:** data
- **Derived from:** DOC-08 (`conversations/conv_pines023_patron_characteristics.eml`)
- **Priority rationale:** An agreed technical response confirms these fields exist in the patron table and are straightforward to query, supporting several reporting needs.

The system shall store and make available the patron fields needed for reporting: zip code, county of residence, home branch, patron type, preferred language, and birth_date. These fields shall be accessible to patron reports and queries. The birth_date field shall support age calculation.

#### REQ-STKID-013 — Aged Debt Report Field Decision

- **Priority:** P3  ·  **Type:** documentation
- **Derived from:** DOC-14 (`evergreen_reference_2009.txt`)
- **Priority rationale:** A reference document identifies the report as partially available and needing enhancement, but provides no field details or evidence of broader agreement.

This item is a stakeholder decision, not a current software requirement: stakeholders shall approve and document the additional fields required for the Aged Debt report before the report enhancement is specified. The decision record shall identify each field, its definition, source data, and expected output behavior. No implementation or acceptance claim for additional fields is made until that controlled decision is approved.

#### REQ-STKID-014 — Outstanding Fines Inactivity Flags

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-09 (`conversations/conv_pines024_inactive_patrons.eml`)
- **Priority rationale:** The request to flag inactive patrons with fines is agreed in one email thread, but the source frames it as a proposed handling distinction.

The system shall identify inactive patrons who have outstanding fines in inactive-patron report results. It shall flag those accounts so staff can distinguish them from other inactive patrons. This shall support handling those accounts differently during follow-up.

#### REQ-STKID-015 — Patron Data Completeness Indicators

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-08 (`conversations/conv_pines023_patron_characteristics.eml`)
- **Priority rationale:** A report completeness indicator is proposed in one email thread, with examples but no explicit priority or broader agreement.

The system shall show the completeness of selected patron fields in report outputs. Users shall be able to see how many records lack fields such as zip code or preferred language. This shall help users assess whether those fields are populated consistently before interpreting report results.

#### REQ-STKID-016 — Patron Report Catalog

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** The full report catalog appears in one draft specification and is proposed without a priority marker or evidence of stakeholder agreement.

The system shall provide the requested patron-report set for management and report users. The set shall include Patron Count; Patron Added Count by Month; New Patron Count by Demographic Category; counts by age demographic, county, county/city/zip, home library, profile group, and survey answer; lists by survey answer, expiration date, barred status, inactive status, and wording in notes; and Voter Survey Responses County by Week. The set shall also include staff-account lists showing the date of last password change and account expiration.

#### REQ-STKID-017 — Per-Patron Transaction Counts

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** The need is stated in one draft specification without an explicit priority or evidence of wider agreement.

The system shall show the number of check-outs and placed holds for each patron in transaction reports. Users shall be able to review both counts in the report results. This shall support analysis of patron transaction activity at the individual-patron level.

### 5.13 Non-Functional Constraints & Platform/Deployment/Compliance (NFRQA)

_Cross-cutting non-functional constraints and platform compatibility: relational backend and reporting replicas/warehouses, enterprise/centralized integration assumptions, performance under load & operational-hour processing, background processing/caching, scalability and large datasets, transaction safety/retention policies/anonymization, availability and cancellation behavior, OPAC isolation/non-interference, accessibility compliance and browser/server OS support._

#### REQ-NFRQA-001 — Client Platform and Browser Compatibility

- **Priority:** P1  ·  **Type:** constraint
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-16 (`interview_sysadmin_2009-05-10.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Priority rationale:** Client access is explicitly marked high priority, and the browser versions are agreed across sources; one source cites the cost of upgrading more than 200 computers.

The system shall be accessible through a web browser or a Windows-compatible client. When browser access is used, the system shall support Microsoft Internet Explorer version 6.0 and later and Mozilla Firefox version 2.0 and later. Acceptance testing shall verify access using the specified minimum browser versions where those platforms are part of the deployment baseline.

#### REQ-NFRQA-002 — Consortium Capacity

- **Priority:** P1  ·  **Type:** non-functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Priority rationale:** The source explicitly marks this capacity requirement high priority and gives concrete consortium scale figures.

The system shall support consortium operations across at least 286 libraries, 17 million annual circulations, and the purchasing and processing of more than 900,000 items annually. Acceptance testing shall load representative records at these stated volumes and verify that reports can query the full consortium data set without data loss or errors. These figures define the minimum operational scale the system must accommodate.

#### REQ-NFRQA-003 — Online-Hours Workload Continuity

- **Priority:** P1  ·  **Type:** non-functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-16 (`interview_sysadmin_2009-05-10.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), DOC-20 (`survey_results_2009.txt`)
- **Priority rationale:** Open-hours processing is marked high priority in one source and identified as a key requirement in another; survey feedback also reports slow reports during busy hours.

The system shall allow reports to run during open hours without disrupting circulation or OPAC use. Under the consortium workload capacity specified for acceptance testing, the 95th-percentile response time for interactive circulation and OPAC requests shall not exceed two seconds, excluding network latency outside the system boundary. Long-running reports shall be queued and processed in the background. Acceptance testing shall compare interactive response times with and without the representative reporting workload.

#### REQ-NFRQA-004 — OPAC Non-Interference

- **Priority:** P1  ·  **Type:** non-functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-16 (`interview_sysadmin_2009-05-10.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** The requirement is supported by multiple sources, including an agreed statement that reporting absolutely cannot constrain the OPAC and a source marking OPAC protection high priority.

The system shall be architected and operated so that reporting activity does not constrain OPAC functionality or degrade catalog responsiveness for patrons. Heavy reporting queries shall not slow down the OPAC. Reporting shall preserve the OPAC's ability to provide its existing features.

#### REQ-NFRQA-005 — Privacy-Preserving Transaction Archive

- **Priority:** P1  ·  **Type:** constraint
- **Derived from:** DOC-12 (`email_report_features.eml`)
- **Priority rationale:** The sources identify state-law retention and patron privacy as compliance requirements, including an explicit legal-constraint signal.

The system shall archive transaction data in a form that protects patron privacy and follows the retention periods established for applicable data categories in REQ-ACCT-003. The archive shall not retain personally identifiable patron information where the approved privacy policy requires de-identification. The project compliance baseline shall identify the governing state-law or approved policy provision and its retention period before compliance acceptance; this requirement does not introduce an unspecified period such as “X years.”

#### REQ-NFRQA-006 — Privacy-Protected Transaction Archive

- **Priority:** P1  ·  **Type:** non-functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** The source marks this as high priority and cites State Law and privacy officers as evidence of a legal and privacy obligation.

The system shall archive transaction data in a form that protects patron privacy as required by the applicable law and approved privacy policy. Before compliance acceptance, the project shall identify the governing law or policy, including exact document, section, and version references, in a controlled compliance register. The archive shall support approved demographic statistics without exposing personally identifiable patron information, and acceptance testing shall verify those privacy controls against the register.

#### REQ-NFRQA-007 — Relational Database Backend

- **Priority:** P1  ·  **Type:** constraint
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-16 (`interview_sysadmin_2009-05-10.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** The relational backend is explicitly marked high priority and mandatory in a source, and PostgreSQL compatibility is supported by the stated existing environment.

The system shall use a fully relational database backend and operate against a fully relational database schema. It shall be compatible with PostgreSQL, including the stated current environment of PostgreSQL 8.3. This constraint shall align the reporting system with the existing database environment.

#### REQ-NFRQA-008 — System Accessibility

- **Priority:** P1  ·  **Type:** non-functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`), DOC-16 (`interview_sysadmin_2009-05-10.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** Section 508 is identified as mandatory and a legal requirement, with additional accessibility requests from multiple sources.

The system, including reporting functions, online help, and HTML report output, shall comply with Section 508 and applicable accessibility standards. It shall support screen-reading software, including JAWS and NVDA, screen-magnification software, including ZoomText, and other assistive technologies. Acceptance testing shall assess the system's user-facing functions against the applicable accessibility criteria and verify access using the identified assistive technologies.

#### REQ-NFRQA-009 — Administrative Error Feedback

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** Error feedback is requested in multiple sources, including an agreed source with concrete diagnostic details; the source material also identifies staff need when reports fail.

The system shall provide users with clear, high-level error reporting and feedback when operations or reports fail. For administrators, it shall also provide query-specific details, including the table, field, and kind of error when available. This feedback shall help users understand failures and help administrators diagnose and resolve them.

#### REQ-NFRQA-010 — Enterprise Deployment Assumptions

- **Priority:** P2  ·  **Type:** constraint
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** Enterprise membership is agreed or stated in three sources, and centralized connectivity and infrastructure assumptions are documented for IT operations.

The system shall operate as part of an enterprise-level Library Automation System and use the enterprise infrastructure on which it depends. The deployment shall support centralized operation across multiple locations and rely on reliable network connectivity between those locations and central servers. The enterprise infrastructure assumption includes redundant servers and backups.

#### REQ-NFRQA-011 — Enterprise Library Automation System Integration

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** Integration with the enterprise ILS and its Acquisitions and Cataloging modules is described across three sources, including an agreed assumption.

The system shall integrate with the enterprise Library Automation System, including its Acquisitions and Cataloging modules, and shall not replace their operational functions. The Library Automation System shall remain the system of record for its data; the reporting system shall read the data required for reporting through supported interfaces or read-only access. The implementation shall document the interfaces, data ownership, supported read operations, and synchronization behavior for each module.

#### REQ-NFRQA-012 — Environment Separation and Configuration Migration

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-14 (`evergreen_reference_2009.txt`), DOC-16 (`interview_sysadmin_2009-05-10.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** Environment separation and migration are requested across multiple sources, including an agreed description of existing environments; a manual configuration transfer is a possible temporary workaround.

The system shall provide separate development, training, and production environments so that development and training work does not affect production. Authorized report users shall be able to export and import report templates, saved queries, permission settings, and other report configurations between environments. Acceptance testing shall verify that each artifact type can be migrated and that imported configurations retain their settings and permissions without changing production until explicitly applied.

#### REQ-NFRQA-013 — Isolated Training Environment

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-16 (`interview_sysadmin_2009-05-10.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** The need appears in an interview and was subsequently agreed in meeting notes, with production-data protection emphasized.

The system shall provide a training environment in which new staff can practice running reports. The training environment shall be separate from production and shall prevent practice or experimentation from affecting production data. This shall allow staff to learn report functions without risking live records.

#### REQ-NFRQA-014 — Linux and Solaris Server Compatibility

- **Priority:** P2  ·  **Type:** constraint
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-16 (`interview_sysadmin_2009-05-10.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Priority rationale:** Linux and Solaris support is agreed as acceptable in one source and requested in another, with specific platform versions and hardware stated by the technical stakeholder.

The system shall be deployable and operable on Linux or Solaris servers. Supported platform constraints include Red Hat Enterprise Linux 5 and Solaris 10 on SPARC hardware, as specified by the sources. The approved deployment baseline shall identify the selected server platform and verify that the system's supported functionality operates on it.

#### REQ-NFRQA-015 — Management Reporting Scope

- **Priority:** P2  ·  **Type:** constraint
- **Derived from:** DOC-17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)
- **Priority rationale:** The scope boundary is established in agreed meeting material and defines which system functions belong in this reporting effort.

The system's reporting scope shall focus on Management Processes: reports and analysis tools used by managers, administrators, and staff for planning, evaluation, and oversight. It shall exclude day-to-day patron-facing OPAC and circulation client functions. Acquisitions and Cataloging shall be specified separately rather than within the Management Processes reports specification.

#### REQ-NFRQA-016 — Queued Background Report Processing

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-09 (`conversations/conv_pines024_inactive_patrons.eml`), DOC-14 (`evergreen_reference_2009.txt`), DOC-16 (`interview_sysadmin_2009-05-10.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Priority rationale:** Background processing is agreed or requested in three sources, with database contention and performance identified as major concerns; reports can otherwise be run interactively as a workaround.

The system shall queue complex and long-running report jobs and process them in the background, separately from interactive sessions. A report user shall receive job status within five seconds of submission, and the queue shall accept at least 100 pending jobs without blocking submission or interactive operations. Report execution shall not directly block circulation or other interactive operations; acceptance testing shall verify that circulation response times remain within the target specified for online-hours workload continuity. Results for the inactive-patrons report shall be cached for the same parameters and data snapshot, with the cache invalidated when that snapshot changes.

#### REQ-NFRQA-017 — Read-Only OPAC Data Access

- **Priority:** P2  ·  **Type:** functional
- **Derived from:** DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** The read-only boundary is agreed in one source and provides a clear integration constraint for reporting on OPAC-related data.

The system shall query OPAC-related data for patron-created holds and circulation transactions when needed for reporting. It shall not modify OPAC data. This read-only access shall allow reporting to use relevant patron activity data while preserving the OPAC as the source of that data.

#### REQ-NFRQA-018 — Relational Database Compatibility

- **Priority:** P2  ·  **Type:** constraint
- **Derived from:** DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** The relational-model constraint was stated as an agreed architectural requirement by a systems administrator.

The system shall operate within and use the relational database structure. Its architecture shall not violate or work against the relational model. This constraint shall preserve compatibility with the agreed database structure.

#### REQ-NFRQA-019 — Deletion Audit Logging

- **Priority:** P3  ·  **Type:** functional
- **Derived from:** DOC-07 (`conversations/conv_pines022_deletions.eml`)
- **Priority rationale:** This was agreed in one source, but no legal mandate, high-priority marker, or broader stakeholder agreement is stated.

The system shall record database deletions in a deletion audit table. It shall implement database-triggered logging so that deletions are captured when they occur. The audit record shall support administrators who need to review deletion activity.

#### REQ-NFRQA-020 — Large Dataset Report Performance

- **Priority:** P3  ·  **Type:** non-functional
- **Derived from:** DOC-09 (`conversations/conv_pines024_inactive_patrons.eml`)
- **Priority rationale:** One source raises an explicit performance concern and gives a 3.5-million-patron example; no priority marker or broader agreement is recorded.

The system shall generate the inactive-patrons report for a dataset containing 3.5 million patron records within 30 minutes when run under the acceptance-test environment and workload. During that run, interactive circulation and OPAC requests shall continue to meet the response-time target for online-hours workload continuity. Acceptance testing shall verify the report results against a reference data set.

#### REQ-NFRQA-021 — Large-Scale Batch Updates

- **Priority:** P3  ·  **Type:** non-functional
- **Derived from:** DOC-04 (`conversations/conv_pines018_item_transfer.eml`)
- **Priority rationale:** The need is based on a concrete 9.6-million-item collection and technical staff concern, but is supported by one source and has no explicit high-priority marker.

The system shall process large batch updates in smaller chunks to limit database locking. It shall scale to batch transfer operations in collections containing millions of items without excessive locking or performance degradation. The stated environment includes 9.6 million items.

#### REQ-NFRQA-022 — Management Scope Boundary

- **Priority:** P3  ·  **Type:** constraint
- **Derived from:** DOC-17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)
- **Priority rationale:** The boundary was agreed in meeting minutes, but it is a project-scope constraint rather than a blocker to system operation.

The project shall specify requirements that directly or indirectly relate to management activities. It shall not attempt to fully specify unrelated ILS modules. This boundary shall keep the specification focused on the agreed management scope.

#### REQ-NFRQA-023 — Process Flow Documentation

- **Priority:** P3  ·  **Type:** documentation
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`), DOC-18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), DOC-19 (`meeting_tech_subcommittee_2009-06-30.txt`)
- **Priority rationale:** Process documentation is requested in two sources and is useful to staff and developers, but it has no high-priority marker.

The software developer shall provide a thorough high-level description of major processes. The documentation shall cover bibliographic record import and export, validation of bibliographic records against internal and external authority sources, and standard reports. This documentation shall help staff and developers understand how data and processes flow through the system.

#### REQ-NFRQA-024 — Report Output Accuracy

- **Priority:** P3  ·  **Type:** non-functional
- **Derived from:** DOC-10 (`early_draft_srs_galecia.txt`)
- **Priority rationale:** A single draft source states the quality need without a priority marker or measurable acceptance criteria.

The system shall produce report outputs that match the selected report criteria and source data. For each release, acceptance testing shall run a defined suite of reports against reference data containing known records, totals, and edge cases; all returned records and aggregate values shall match the expected results. The system shall identify execution failures and shall not present a partial result as a complete report.

#### REQ-NFRQA-025 — SRS Audience And Readability

- **Priority:** P3  ·  **Type:** documentation
- **Derived from:** DOC-17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)
- **Priority rationale:** One meeting source identifies both audiences and the readability need; no higher-priority marker is given.

The Software Requirements Specification shall serve library managers and staff who may contribute requirements, as well as software project managers and developers. It shall be readable to non-technical readers while remaining specific enough for developers. This balance shall support both stakeholder review and implementation.

#### REQ-NFRQA-026 — Transactional Batch Updates

- **Priority:** P3  ·  **Type:** non-functional
- **Derived from:** DOC-04 (`conversations/conv_pines018_item_transfer.eml`)
- **Priority rationale:** One source requests transaction safety for batch updates, with no explicit priority marker or additional agreement.

The system shall perform batch location updates within database transactions. Each batch shall preserve data safety and consistency if an update does not complete successfully. This shall reduce the risk of partially applied location changes.

## 6. Discarded Requirements (Blacklist)

Candidate requirements identified in the sources but **not** included in the specification.

| ID | Candidate | Category | Reason | Conflicts with / superseded by | Sources |
|---|---|---|---|---|---|
| DIS-001 | User Choice To Exclude Nulls | Superseded | This candidate raises the earlier question of whether users should exclude records with null values, but the later agreed meeting decision requires null and blank values to be included. | Include Null And Blank Values | DOC-08 |
| DIS-002 | Vendor Data Integration | Out of scope | These candidates require interfaces with vendor websites and ingestion of standard-format data files, which are integration capabilities rather than query-building, filtering, or candidate-selection behavior. | — | DOC-18, DOC-19 |
| DIS-003 | Library Terminology Assumption | Not a requirement | This states an assumption about the readers of the specification rather than a system obligation. | — | DOC-17 |
| DIS-004 | Circulate Reference Draft | Not a requirement | This is a project communication task to circulate a draft document, not a requirement for the software system. | — | DOC-17 |
| DIS-005 | Defer UI Specification | Not a requirement | This describes when the project should produce UI specifications rather than system behavior. | — | DOC-17 |
| DIS-006 | Reports Specification Project Task | Not a requirement | This is a project documentation deliverable about a future release rather than a requirement for the system. | — | DOC-17 |
| DIS-007 | Iterative Prototype Methodology | Not a requirement | This specifies a development and review methodology rather than a system requirement. | — | DOC-17 |
| DIS-008 | Member Interview Assignment | Not a requirement | This assigns project members an interview task and deadline rather than specifying system behavior. | — | DOC-17 |
| DIS-009 | Follow-Up Meeting Schedule | Not a requirement | This schedules a project meeting and does not impose a software system requirement. | — | DOC-17 |
| DIS-010 | Patron OPAC Interaction | Conflict | These candidates describe patron-facing interaction through the OPAC, which is excluded from the Management Processes reporting scope; the retained read-only data-access requirement covers reporting queries without enabling patron-facing OPAC functions. | Management Reporting Scope, Read-Only OPAC Data Access | DOC-10 |
| DIS-011 | Architectural Subcommittee Meeting | Not a requirement | This candidate schedules a project meeting to discuss constraints rather than specifying a system obligation. | — | DOC-17 |
| DIS-012 | Foundation Draft Selection | Not a requirement | This candidate records a decision about the source document for drafting the specification, not a system requirement. | — | DOC-17 |
| DIS-013 | Reports Working Group Approval | Not a requirement | This candidate defines a project development and testing process rather than a requirement of the system. | — | DOC-17 |
| DIS-014 | Reports Mission Statement | Not a requirement | This candidate states a planning mission to document future reports functionality and develop a requirements list, rather than specifying behavior the system shall provide. | — | DOC-18 |
| DIS-015 | Reports Testing Workflow | Not a requirement | This describes an organizational Reports Working Group process for filtering development rather than a capability the software system shall provide. | — | DOC-18 |
| DIS-016 | Compile Executive Reports List | Not a requirement | The source records a meeting action to compile a list of reports needed for an Executive Reports Interface, rather than specifying behavior the software itself shall provide. | — | DOC-17 |
| DIS-017 | Vendor Data Interfaces | Out of scope | Vendor website interfaces and automated vendor data-file integrations are outside the scope established by DIS-002. This requirement would impose the vendor integration capability excluded by that scope decision. | REQ-DATAQ-024 | DOC-10, DOC-18, DOC-19 |
| DIS-018 | Handle Optional EDI Data | Out of scope | Ingesting and handling vendor-provided EDI data is a vendor data integration capability and is outside the scope established by DIS-002. The system is not required by this specification to integrate vendor data. | REQ-NFRQA-035 | DOC-19 |

## 7. Traceability Matrix

Which requirements were derived from each source document.

| Document | Requirements | Discarded |
|---|---|---|
| DOC-01 `conversations/conv_pines014_material_volume.eml` | REQ-LOCAP-004, REQ-LOCAP-008, REQ-CALCD-003, REQ-CALCD-019 | — |
| DOC-02 `conversations/conv_pines015_capacity_interface.eml` | REQ-ROLE-010, REQ-UIXT-005, REQ-RPTMG-003, REQ-ANALY-008, REQ-LOCAP-002, REQ-LOCAP-006, REQ-LOCAP-007, REQ-CALCD-004, REQ-CALCD-012, REQ-CALCD-020 | — |
| DOC-03 `conversations/conv_pines016_shelf_space.eml` | REQ-RPTMG-003, REQ-ANALY-003, REQ-ANALY-004, REQ-ANALY-015, REQ-LOCAP-009, REQ-LOCAP-010, REQ-CALCD-005 | — |
| DOC-04 `conversations/conv_pines018_item_transfer.eml` | REQ-ROLE-012, REQ-DATAQ-017, REQ-DATAQ-018, REQ-DATAQ-021, REQ-RPTMG-018, REQ-OPMIS-002, REQ-OPMIS-003, REQ-OPMIS-005, REQ-OPMIS-006, REQ-OPMIS-008, REQ-OPMIS-009, REQ-OPMIS-011, REQ-OPMIS-012, REQ-NFRQA-021, REQ-NFRQA-026 | — |
| DOC-05 `conversations/conv_pines019_020_missing_intransit.eml` | REQ-ANALY-008, REQ-OPMIS-001, REQ-OPMIS-004, REQ-OPMIS-010 | — |
| DOC-06 `conversations/conv_pines021_item_purging.eml` | REQ-ROLE-011, REQ-DATAQ-001, REQ-DATAQ-013, REQ-RPTMG-037, REQ-PURGE-002, REQ-PURGE-003, REQ-PURGE-004, REQ-PURGE-006, REQ-PURGE-007, REQ-PURGE-008 | — |
| DOC-07 `conversations/conv_pines022_deletions.eml` | REQ-PURGE-001, REQ-PURGE-006, REQ-NFRQA-019 | — |
| DOC-08 `conversations/conv_pines023_patron_characteristics.eml` | REQ-DATAQ-001, REQ-DATAQ-011, REQ-STKID-001, REQ-STKID-002, REQ-STKID-003, REQ-STKID-005, REQ-STKID-009, REQ-STKID-012, REQ-STKID-015 | DIS-001 |
| DOC-09 `conversations/conv_pines024_inactive_patrons.eml` | REQ-LOCAP-005, REQ-STKID-004, REQ-STKID-006, REQ-STKID-007, REQ-STKID-008, REQ-STKID-010, REQ-STKID-014, REQ-NFRQA-016, REQ-NFRQA-020 | — |
| DOC-10 `early_draft_srs_galecia.txt` | REQ-AUTH-001, REQ-ROLE-001, REQ-ROLE-002, REQ-ROLE-003, REQ-ROLE-004, REQ-ROLE-005, REQ-ROLE-006, REQ-ROLE-007, REQ-ROLE-009, REQ-UIXT-001, REQ-UIXT-002, REQ-UIXT-007, REQ-DATAQ-001, REQ-DATAQ-002, REQ-DATAQ-003, REQ-DATAQ-004, REQ-DATAQ-005, REQ-DATAQ-006, REQ-DATAQ-007, REQ-DATAQ-008, REQ-DATAQ-010, REQ-DATAQ-014, REQ-DATAQ-015, REQ-DATAQ-016, REQ-DATAQ-018, REQ-DATAQ-019, REQ-DATAQ-020, REQ-RPTMG-001, REQ-RPTMG-002, REQ-RPTMG-003, REQ-RPTMG-004, REQ-RPTMG-005, REQ-RPTMG-006, REQ-RPTMG-007, REQ-RPTMG-008, REQ-RPTMG-009, REQ-RPTMG-011, REQ-RPTMG-012, REQ-RPTMG-015, REQ-RPTMG-016, REQ-RPTMG-017, REQ-RPTMG-018, REQ-RPTMG-019, REQ-RPTMG-022, REQ-RPTMG-023, REQ-RPTMG-024, REQ-RPTMG-025, REQ-RPTMG-029, REQ-RPTMG-030, REQ-RPTMG-031, REQ-RPTMG-032, REQ-RPTMG-033, REQ-RPTMG-034, REQ-RPTMG-035, REQ-RPTMG-036, REQ-RPTMG-038, REQ-ANALY-002, REQ-ANALY-004, REQ-ANALY-005, REQ-ANALY-009, REQ-ANALY-010, REQ-ANALY-011, REQ-ANALY-014, REQ-ANALY-017, REQ-ANALY-018, REQ-LOCAP-001, REQ-OPMIS-001, REQ-OPMIS-002, REQ-OPMIS-004, REQ-OPMIS-005, REQ-OPMIS-007, REQ-PURGE-001, REQ-PURGE-002, REQ-PURGE-004, REQ-PURGE-005, REQ-PURGE-009, REQ-PURGE-010, REQ-ACCT-001, REQ-ACCT-002, REQ-ACCT-003, REQ-ACCT-004, REQ-ACCT-005, REQ-ACCT-007, REQ-ACCT-008, REQ-ACCT-010, REQ-ACCT-011, REQ-CALCD-001, REQ-CALCD-002, REQ-CALCD-003, REQ-CALCD-004, REQ-CALCD-005, REQ-CALCD-006, REQ-CALCD-007, REQ-CALCD-011, REQ-CALCD-013, REQ-STKID-001, REQ-STKID-004, REQ-STKID-005, REQ-STKID-011, REQ-STKID-016, REQ-STKID-017, REQ-NFRQA-001, REQ-NFRQA-002, REQ-NFRQA-003, REQ-NFRQA-004, REQ-NFRQA-006, REQ-NFRQA-007, REQ-NFRQA-008, REQ-NFRQA-009, REQ-NFRQA-010, REQ-NFRQA-011, REQ-NFRQA-012, REQ-NFRQA-014, REQ-NFRQA-023, REQ-NFRQA-024 | DIS-010, DIS-017 |
| DOC-11 `email_financial_reports.eml` | REQ-ACCT-001, REQ-ACCT-002, REQ-ACCT-003, REQ-ACCT-006, REQ-ACCT-007, REQ-ACCT-008, REQ-ACCT-009, REQ-ACCT-010, REQ-CALCD-002 | — |
| DOC-12 `email_report_features.eml` | REQ-ROLE-002, REQ-ROLE-003, REQ-ROLE-005, REQ-ROLE-006, REQ-ROLE-008, REQ-ROLE-009, REQ-DATAQ-001, REQ-DATAQ-002, REQ-DATAQ-004, REQ-DATAQ-005, REQ-DATAQ-006, REQ-DATAQ-007, REQ-DATAQ-016, REQ-RPTMG-001, REQ-RPTMG-002, REQ-RPTMG-004, REQ-RPTMG-005, REQ-RPTMG-006, REQ-RPTMG-021, REQ-RPTMG-026, REQ-ANALY-002, REQ-ANALY-011, REQ-STKID-005, REQ-NFRQA-005 | — |
| DOC-13 `email_staff_login.eml` | REQ-AUTH-001, REQ-AUTH-002, REQ-AUTH-003, REQ-ROLE-004, REQ-ROLE-007, REQ-ROLE-009 | — |
| DOC-14 `evergreen_reference_2009.txt` | REQ-AUTH-004, REQ-ROLE-002, REQ-UIXT-001, REQ-UIXT-003, REQ-UIXT-004, REQ-UIXT-006, REQ-UIXT-007, REQ-DATAQ-001, REQ-DATAQ-003, REQ-DATAQ-005, REQ-DATAQ-007, REQ-DATAQ-009, REQ-DATAQ-012, REQ-DATAQ-014, REQ-DATAQ-019, REQ-RPTMG-002, REQ-RPTMG-003, REQ-RPTMG-004, REQ-RPTMG-005, REQ-RPTMG-008, REQ-RPTMG-011, REQ-RPTMG-012, REQ-RPTMG-015, REQ-RPTMG-016, REQ-RPTMG-017, REQ-RPTMG-018, REQ-RPTMG-019, REQ-RPTMG-022, REQ-RPTMG-036, REQ-ANALY-005, REQ-ANALY-006, REQ-ANALY-007, REQ-ANALY-009, REQ-ANALY-013, REQ-ANALY-016, REQ-ANALY-019, REQ-LOCAP-011, REQ-LOCAP-012, REQ-PURGE-002, REQ-PURGE-005, REQ-ACCT-012, REQ-CALCD-002, REQ-CALCD-008, REQ-CALCD-009, REQ-CALCD-010, REQ-CALCD-013, REQ-CALCD-014, REQ-CALCD-015, REQ-CALCD-017, REQ-CALCD-018, REQ-STKID-004, REQ-STKID-005, REQ-STKID-013, REQ-NFRQA-008, REQ-NFRQA-012, REQ-NFRQA-016 | — |
| DOC-15 `interview_cataloging_2009-05-08.txt` | REQ-DATAQ-012, REQ-DATAQ-017, REQ-DATAQ-018, REQ-RPTMG-018, REQ-ANALY-007, REQ-OPMIS-001, REQ-OPMIS-002, REQ-OPMIS-004, REQ-OPMIS-005, REQ-OPMIS-013, REQ-PURGE-001, REQ-PURGE-002, REQ-PURGE-003, REQ-PURGE-004, REQ-PURGE-005, REQ-CALCD-003, REQ-CALCD-005, REQ-CALCD-006, REQ-CALCD-007 | — |
| DOC-16 `interview_sysadmin_2009-05-10.txt` | REQ-ROLE-004, REQ-ROLE-007, REQ-ROLE-009, REQ-UIXT-001, REQ-UIXT-002, REQ-DATAQ-014, REQ-NFRQA-001, REQ-NFRQA-003, REQ-NFRQA-004, REQ-NFRQA-007, REQ-NFRQA-008, REQ-NFRQA-012, REQ-NFRQA-013, REQ-NFRQA-014, REQ-NFRQA-016 | — |
| DOC-17 `meeting_minutes/meeting_2009-03-15_minutes.txt` | REQ-ROLE-004, REQ-UIXT-003, REQ-RPTMG-013, REQ-ANALY-010, REQ-ANALY-017, REQ-LOCAP-013, REQ-LOCAP-014, REQ-LOCAP-015, REQ-LOCAP-016, REQ-OPMIS-014, REQ-ACCT-002, REQ-CALCD-011, REQ-STKID-005, REQ-NFRQA-015, REQ-NFRQA-022, REQ-NFRQA-025 | DIS-003, DIS-004, DIS-005, DIS-006, DIS-007, DIS-008, DIS-009, DIS-011, DIS-012, DIS-013, DIS-016 |
| DOC-18 `meeting_minutes/meeting_2009-07-20_minutes.txt` | REQ-AUTH-001, REQ-ROLE-004, REQ-UIXT-001, REQ-UIXT-002, REQ-DATAQ-008, REQ-RPTMG-001, REQ-RPTMG-005, REQ-RPTMG-013, REQ-RPTMG-028, REQ-ANALY-012, REQ-ANALY-015, REQ-LOCAP-001, REQ-OPMIS-001, REQ-OPMIS-004, REQ-PURGE-005, REQ-ACCT-008, REQ-CALCD-004, REQ-CALCD-005, REQ-STKID-005, REQ-STKID-010, REQ-NFRQA-001, REQ-NFRQA-002, REQ-NFRQA-003, REQ-NFRQA-004, REQ-NFRQA-007, REQ-NFRQA-008, REQ-NFRQA-009, REQ-NFRQA-010, REQ-NFRQA-011, REQ-NFRQA-012, REQ-NFRQA-014, REQ-NFRQA-016, REQ-NFRQA-023 | DIS-002, DIS-014, DIS-015, DIS-017 |
| DOC-19 `meeting_tech_subcommittee_2009-06-30.txt` | REQ-ROLE-004, REQ-ROLE-007, REQ-ROLE-009, REQ-UIXT-001, REQ-UIXT-002, REQ-DATAQ-003, REQ-DATAQ-008, REQ-DATAQ-010, REQ-DATAQ-014, REQ-RPTMG-003, REQ-RPTMG-015, REQ-ANALY-005, REQ-ANALY-006, REQ-LOCAP-001, REQ-LOCAP-003, REQ-NFRQA-004, REQ-NFRQA-007, REQ-NFRQA-008, REQ-NFRQA-009, REQ-NFRQA-010, REQ-NFRQA-011, REQ-NFRQA-012, REQ-NFRQA-013, REQ-NFRQA-017, REQ-NFRQA-018, REQ-NFRQA-023 | DIS-002, DIS-017, DIS-018 |
| DOC-20 `survey_results_2009.txt` | REQ-ROLE-002, REQ-ROLE-003, REQ-UIXT-008, REQ-DATAQ-003, REQ-DATAQ-009, REQ-DATAQ-015, REQ-DATAQ-017, REQ-DATAQ-018, REQ-RPTMG-002, REQ-RPTMG-003, REQ-RPTMG-005, REQ-RPTMG-010, REQ-RPTMG-011, REQ-RPTMG-014, REQ-RPTMG-015, REQ-RPTMG-018, REQ-RPTMG-020, REQ-RPTMG-027, REQ-ANALY-001, REQ-ANALY-002, REQ-ANALY-005, REQ-ANALY-006, REQ-ANALY-009, REQ-ANALY-014, REQ-ANALY-016, REQ-LOCAP-017, REQ-OPMIS-002, REQ-OPMIS-005, REQ-PURGE-001, REQ-CALCD-001, REQ-CALCD-016, REQ-STKID-005, REQ-STKID-011, REQ-NFRQA-003 | — |

## 8. Quality Assurance Record

- Candidate coverage: 580/580 extracted candidates are linked to a requirement or a discard.
- Review rounds: 3 (maximum 3).
  - Round 1: approved=False, 30 issues (28 blocking) — The specification has complete source traceability and no uncovered candidates, but it contains several duplicate requirements, inconsistent priorities, terminology inconsistencies, unresolved retention and scope issues, and multiple vague or non-testable statements.
  - Round 2: approved=False, 31 issues (27 blocking) — The specification has complete candidate and source traceability according to the automatic checks, but blocking issues remain: several duplicate requirements, unresolved conflicts and undefined legal or controlled artifacts, and multiple requirements whose acceptance criteria are not testable.
  - Round 3: approved=False, 10 issues (6 blocking) — Blocking issues remain: one explicit retention conflict, several overlapping or duplicate requirements, and one retained entry that explicitly states it is not a current software requirement. Traceability and uncovered-candidate checks are otherwise satisfactory.

Issues reported in the final review round (not all may have been resolved):

- [blocking/conflict] REQ-ACCT-005, REQ-ACCT-003, REQ-ANALY-006: REQ-ACCT-005 and REQ-ACCT-003 state that de-identified aggregates follow approved policy and legal requirements and do not imply indefinite retention. REQ-ANALY-006 instead refers to a separate 'indefinite-retention rule' for de-identified monthly and annual aggregates. These retention obligations contradict one another.
- [blocking/duplicate] REQ-NFRQA-006, REQ-NFRQA-005: REQ-NFRQA-006 and REQ-NFRQA-005 both require a privacy-preserving transaction archive, prohibit or constrain personally identifiable patron information, require an approved legal or policy baseline, and address retention. The differences are mostly wording and source attribution, not separate system needs.
- [blocking/duplicate] REQ-NFRQA-007, REQ-NFRQA-018: Both requirements require the system to use and remain compatible with a relational database structure. REQ-NFRQA-007 is the more complete version because it identifies PostgreSQL and the current environment; REQ-NFRQA-018 adds no distinct testable need.
- [blocking/duplicate] REQ-NFRQA-004, REQ-NFRQA-003: Both requirements address preventing reporting workloads from degrading OPAC and circulation performance during operating hours. REQ-NFRQA-003 supplies the measurable two-second 95th-percentile target and workload test, while REQ-NFRQA-004 repeats the same need in qualitative terms.
- [minor/duplicate] REQ-RPTMG-019, REQ-RPTMG-014: REQ-RPTMG-019 requires scheduling reports hourly, daily, weekly, monthly, and yearly, while REQ-RPTMG-014 separately requires recurring report scheduling. REQ-RPTMG-014 adds no distinct behavior beyond the scheduling capability already specified in REQ-RPTMG-019.
- [blocking/blacklist] REQ-STKID-013: REQ-STKID-013 explicitly states that it is a stakeholder decision rather than a current software requirement and makes no implementation or acceptance claim. It is therefore incorrectly retained in the requirements set.
- [blocking/quality] REQ-CALCD-011, REQ-LOCAP-001, REQ-UIXT-008: These requirements contain broad, difficult-to-test obligations. REQ-CALCD-011 refers to unspecified 'analysis tools' and collection usage without identifying measures or supported operations. REQ-LOCAP-001 uses undefined terms such as 'central location,' 'provide services,' and 'single source of truth.' REQ-UIXT-008 requires an 'intuitive' and 'understandable' interface without measurable usability criteria.
- [minor/quality] REQ-NFRQA-010, REQ-ANALY-008: REQ-NFRQA-010 mixes system requirements with external deployment assumptions and uses undefined terms such as 'reliable network connectivity,' 'enterprise infrastructure,' and 'redundant servers.' REQ-ANALY-008 requires reports to show whether branches are 'growing or shrinking' without defining the measure, comparison baseline, or calculation.
- [minor/terminology] REQ-ACCT-008, REQ-ACCT-010, REQ-ANALY-011, REQ-ANALY-017, REQ-ANALY-001, REQ-ANALY-003, REQ-ANALY-004, REQ-ANALY-015, REQ-ANALY-002: The specification alternates between 'system,' 'library system,' and 'consortium,' and the unqualified 'system' can be confused with either a library system or the entire consortium. The automatic terminology finding is not a valid patron/client correction in REQ-NFRQA-001 and REQ-NFRQA-015 because 'client' there denotes client software, not a library customer; however, organizational-scope terminology still needs clarification.
- [minor/priority] REQ-ANALY-001, REQ-STKID-005: Both requirements cover privacy-protected demographic reporting. REQ-ANALY-001 rates anonymization as P1, while REQ-STKID-005 rates the same de-identification and non-exposure obligation as P2. The analytical feature may be P2, but the shared privacy constraint should not appear to have a lower priority in the later requirement.
