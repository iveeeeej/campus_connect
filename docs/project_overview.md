# Campus Connect
## University Student e-Governance and Services Platform

---

## 1. Project Overview

Campus Connect is a web and mobile-based e-governance and student services platform for USTP-Oroquieta student organization operations.

Campus Connect may be introduced first through the University Student Government (USG), but the system must be designed for **organization-scoped use**. This means the same system structure can support course/department organizations such as SITE, PAFE, and AFPROTECH without changing the main UI and module layout.

The system centralizes organization operations that are commonly handled through paper records, separate files, manual attendance sheets, social media posts, and informal messaging channels. It provides one controlled digital environment for officer-side management and student-side participation.

Campus Connect must support clear organization boundaries:

- USG records cover the full student body.
- Course/department organization records cover only students aligned with that course or department.
- Each organization manages only its own records.
- Students may view USG records and records from their assigned course/department organization.

The platform follows a **web + mobile + centralized backend** model with three user-facing interfaces:

- the **Officer / Super Admin Web Platform** is used for management, monitoring, verification, approvals, reporting, and administrative control
- the **Signatory Web Platform** is used by approved signatory users to review assigned event documents and reports and mark them as **For Approval** or **For Disapproval**
- the **Student Mobile Application** is used for registration, attendance participation, record viewing, receipt submission, receiving in-app notifications, and receiving mobile push notifications where enabled
- the **backend API** acts as the single source of truth and must enforce authentication, validation, organization ownership, workflow rules, signatory assignment, and data integrity
- the **database layer** stores accounts, organizations, attendance records, event documents, reports, payments, violations, announcements, meetings, events, signatures, export history, Cloudinary media references where applicable, and other official system records

This file is intended as a **development guide for an LLM agent or developer**. It defines the official product direction, module boundaries, role model, organization-scoped access model, and core workflow rules for the system.

---

## 2. Core Purpose

Campus Connect exists to improve the efficiency, transparency, consistency, and traceability of organization operations.

The system must address the following operational problems across covered organizations:

- scattered announcements and communication channels
- manual event and meeting coordination
- manual attendance tracking
- delayed or unclear violation monitoring
- disconnected payment verification processes
- disorganized lost-and-found handling
- difficulty preparing structured organization reports
- limited visibility into student participation and organizational records

The system must consolidate these workflows into one secured platform where organization officers can manage their own records and students can access services and records relevant to them.

---

## 3. Core Objectives

Campus Connect must support the following objectives:

- provide a centralized officer dashboard connected to backend data, including a calendar for event and meeting schedules
- manage organization-owned events and meetings through the officer web platform
- support official announcements and global Chats / Messaging for student-officer communication
- support student mobile registration through preloaded student master record matching
- digitize attendance using school ID QR scanning, geolocation validation, and facial recognition
- support sign-in and sign-out attendance validation
- detect missing sign-in/sign-out checkpoints and prepare pending violations for officer confirmation
- support Lost and Found visibility through USG-posted found item records, including item images stored through Cloudinary where applicable
- support payment tracking through student receipt screenshot submission, manual payment recording, and officer verification
- support structured event documents and official reports using fixed templates and controlled editable fields
- support DOCX/PDF export for finalized event documents and reports after required signatories are completed
- provide database-backed in-app notifications and mobile push notification support where enabled
- maintain student-facing records such as attendance, violations, payments, and profile information

---

## 4. Platform Scope and Boundaries

### 4.1 Organization Coverage and Boundaries

Campus Connect may support the USG and course/department-based student organizations within one system.

The UI and core modules must remain the same across organizations. The main difference is the student coverage assigned to each organization:

- **USG coverage** includes the full student body.
- **Course/department organization coverage** includes only students under the aligned course or department.

The first implementation may start with the USG only, but the database, backend logic, and access rules should be designed so additional organizations can be added later without redesigning the whole system.

Each organization must have its own shared officer account.

Examples:

- `USG_OFFICER`
- `SITE_OFFICER`
- `PAFE_OFFICER`
- `AFPROTECH_OFFICER`

Each organization officer account must only view and manage records owned by its organization, including:

- dashboard records
- events
- meetings
- announcements
- attendance sessions and records
- violations
- payments
- reports
- notifications

Lost and Found is an exception. It is handled as a USG-managed service and is not managed separately by SITE, PAFE, or AFPROTECH officer accounts.

Student organization visibility must be based on the student profile, especially the student's course or department.

A student may see:

- USG records, because USG covers all students
- records from the student's assigned course/department organization

Student-facing records must show the organization label so students know where the item came from.

Examples:

- `[USG] General Assembly`
- `[SITE] Programming Seminar`

Technical rule for developers:

- records that belong to an organization should include an organization reference or equivalent ownership field
- officer queries must be filtered by the logged-in officer organization account
- student queries must include USG records plus records from the student's assigned course/department organization
- users must not manually switch organizations unless a separate system redesign formally allows it

### 4.2 Web and Mobile Platform Scope

Campus Connect uses three platform-facing interfaces:

- **Officer / Super Admin Web Platform**
- **Signatory Web Platform**
- **Student Mobile Application**

The **Officer / Super Admin Web Platform** is the official administrative interface for `SUPER_ADMIN`, `USG_OFFICER`, and `ORG_OFFICER` users.

`SUPER_ADMIN` uses the same officer web platform as officer users, but must have additional Super Admin controls for system-wide management actions such as student account management, cross-organization record access, organization filtering, and global payment QR management.

Officer accounts use the same officer web platform, but the records shown must depend on the logged-in account role and organization ownership.

Examples:

- `SUPER_ADMIN` can view records across all organizations and may filter records by organization.
- `USG_OFFICER` sees and manages USG-owned records only.
- `SITE_OFFICER` sees and manages SITE-owned records only.
- `PAFE_OFFICER` sees and manages PAFE-owned records only.
- `AFPROTECH_OFFICER` sees and manages AFPROTECH-owned records only.

Officer dashboards must follow the same access rule:

- `SUPER_ADMIN` may view all dashboard data by default and filter by organization.
- `USG_OFFICER` must see only USG dashboard data.
- `ORG_OFFICER` accounts must see only dashboard data for their assigned organization.

The **Signatory Web Platform** is a separate simplified web interface for `SIGNATORY` users.

Signatory users must register and be approved before they can use the signatory interface. A pending or rejected signatory account must not access assigned event documents or reports.

The signatory interface must not expose officer management features. It should only allow approved signatory users to:

- log in
- view assigned event documents and reports
- review the assigned event document or report content
- mark the assigned event document or report as **For Approval**
- mark the assigned event document or report as **For Disapproval**
- provide **Reason/s for Disapproval** when disapproving

The **Student Mobile Application** is the official student-facing participation and service interface. Students use one mobile app. The app must show:

- USG records, because USG covers all students
- records from the student's assigned course/department organization

Student organization visibility must be derived from the student profile, especially the student's course or department.

Examples:

- IT students see USG + SITE records.
- BTLED students see USG + PAFE records.
- BFPT students see USG + AFPROTECH records.

Users must not manually switch organizations inside the app.

The system must decide visibility automatically based on:

- the logged-in role, for web access
- the logged-in officer account organization, for officer web access
- assigned event document and report access, for signatory web access
- the student's profile, course, or department, for mobile student access

Student mobile content should be combined by default, with clear organization labels. A filter option may be provided so students can view records by organization when needed.

Technical rule for developers:

- web routes and API responses must be filtered based on role and organization ownership
- `SUPER_ADMIN` access must be system-wide but still support organization filters
- `USG_OFFICER` and `ORG_OFFICER` access must be organization-scoped
- `SIGNATORY` access must be assignment-scoped, not organization-management-scoped
- `STUDENT` access must include USG records plus records from the student's assigned course/department organization
- Chats / Messaging is a system-wide exception and must allow students, officer accounts, and `SUPER_ADMIN` in one global chat room
- the frontend must not be treated as the final authority for access control; the backend must enforce role, organization, student-visibility, and signatory-assignment rules

### 4.3 Architecture Scope

The system must follow an API-first architecture.

The backend must enforce:

- authentication
- role-based access
- student master record matching and student account activation rules
- attendance validation
- payment verification workflow
- violation confirmation workflow
- event document template rules
- report template rules
- signatory assignment and approval/disapproval rules
- finalized DOCX/PDF export rules for event documents and reports
- notification record creation
- data integrity and status transitions

Frontend and mobile clients may guide the user experience, but they must not be treated as the final authority for business rules.

### 4.4 Functional Scope

The system scope includes:

- organization-scoped ownership for all major records
- officer dashboard wiring to backend data
- dashboard calendar for event and meeting schedules
- schedule conflict checking for events and meetings
- event management
- meeting management
- announcements
- global Chats / Messaging for students, officers, and Super Admin
- student registration through preloaded student master record matching and auto-approval when all required checks pass
- attendance with school ID QR scan, geolocation, and facial recognition
- violation monitoring and officer confirmation
- USG Lost and Found viewing from USG-posted records, including item images stored through Cloudinary where applicable
- payment tracking with receipt screenshot upload, manual payment recording, and officer verification
- fixed-template event documents and reports
- DOCX/PDF export for finalized event documents and reports
- database-backed in-app notifications and mobile push notification support where enabled
- consolidated student records

Even when the rollout starts with USG only, the backend and database design must not hardcode USG as the only possible organization. Major records must support organization ownership so SITE, PAFE, and AFPROTECH can be added without redesigning the system. Lost and Found is the exception because it is a USG-managed service visible to all students.

---

## 5. User Roles and Access Model

Campus Connect uses a five-role access model.

The system must clearly separate full system administration, USG officer management, organization officer management, student access, and assigned event document and report access.

Technical role names:

```text
SUPER_ADMIN
USG_OFFICER
ORG_OFFICER
STUDENT
SIGNATORY
```

Access control must be enforced by the backend. The web frontend and mobile app may guide the user experience, but they must not be trusted as the final authority for role permissions, organization ownership, document access, or workflow approval.

---

### 5.1 Role List

The system recognizes the following application-level roles:

- `SUPER_ADMIN`
- `USG_OFFICER`
- `ORG_OFFICER`
- `STUDENT`
- `SIGNATORY`

Role purpose summary:

- `SUPER_ADMIN` is used by the USG Moderator and has full access across all organizations.
- `USG_OFFICER` is the shared officer account for USG-owned records and workflows.
- `ORG_OFFICER` is used by course/department organization officer accounts such as SITE, PAFE, and AFPROTECH.
- `STUDENT` is used by individual student accounts through the mobile application.
- `SIGNATORY` is used by individual signatory accounts through a separate web interface for assigned event documents and reports only.

The system must not use officer position names such as president, treasurer, auditor, or adviser as login roles or authorization roles.

---

### 5.2 SUPER_ADMIN / USG Moderator

The `SUPER_ADMIN` role represents the USG Moderator.

The `SUPER_ADMIN` uses the same officer web platform as officers, but with additional Super Admin controls.

The `SUPER_ADMIN` must be able to view and manage records across all organizations, including:

- USG records
- SITE records
- PAFE records
- AFPROTECH records
- student accounts
- organization records
- events
- meetings
- announcements
- global chat/messaging records
- attendance records
- violations
- USG Lost and Found records
- payment records
- reports
- notifications
- system-level configuration

The `SUPER_ADMIN` may manage event document and report records, but must not perform signatory approval actions unless assigned through the signatory workflow.

The `SUPER_ADMIN` is the only role allowed to upload or update the global payment QR code used for payment scanning.

There is only one global payment QR code for all organizations. However, payment records must still belong to the correct organization, and officers must verify payment submissions under their own organization records.

The `SUPER_ADMIN` must also support student account management through the web UI.

The `SUPER_ADMIN` may also approve or reject signatory registrations.

Student master record and student account management includes:

- add or import preloaded student master records
- edit student master record information
- view linked student user accounts
- deactivate student accounts where necessary

Student mobile registration is not manually approved by default. A student account is activated only when the submitted registration details match an existing student master record and all required checks pass.

The `SUPER_ADMIN` must not replace the need for organization ownership. Even though the `SUPER_ADMIN` can access everything, normal officer accounts must still be restricted to their own organization records.

---

### 5.3 USG_OFFICER

The `USG_OFFICER` role is used for the shared USG officer account.

Example account:

```text
username: USG_OFFICER
role: USG_OFFICER
organization: USG
```

The `USG_OFFICER` account manages USG-owned records only.

USG coverage includes the full student body, so USG-owned events, meetings, announcements, attendance sessions, payments, violations, reports, and notifications may apply to all students when appropriate.

The `USG_OFFICER` account must not automatically view, manage, verify, approve, or edit records owned by SITE, PAFE, or AFPROTECH.

The `USG_OFFICER` account may perform officer-side actions for USG records, including:

- manage USG dashboard records
- create and manage USG events
- create and manage USG meetings
- create and manage USG announcements
- send and reply in Chats / Messaging as `USG Officer`
- open and close USG attendance sessions
- review USG attendance records
- confirm USG-related violations
- review and verify USG payment submissions
- manage USG lost-and-found records
- prepare USG reports
- assign signatories to USG reports
- manage USG notifications
- approve or reject signatory registrations

Because this is a shared account, important actions must require the real officer name to be entered manually.

---

### 5.4 ORG_OFFICER

The `ORG_OFFICER` role is used for shared course/department organization officer accounts.

Examples:

```text
username: SITE_OFFICER
role: ORG_OFFICER
organization: SITE
```

```text
username: PAFE_OFFICER
role: ORG_OFFICER
organization: PAFE
```

```text
username: AFPROTECH_OFFICER
role: ORG_OFFICER
organization: AFPROTECH
```

All course/department organization officer accounts use the same technical role: `ORG_OFFICER`.

The `organization` field determines which organization records the account may access.

An `ORG_OFFICER` account may only view and manage records owned by its assigned organization.

This applies to:

- dashboard data
- events
- meetings
- announcements
- attendance sessions
- attendance records
- violations
- payment records
- reports
- notifications

An `ORG_OFFICER` account must not view or manage records from USG or from another course/department organization.

Examples:

- `SITE_OFFICER` manages SITE records only.
- `PAFE_OFFICER` manages PAFE records only.
- `AFPROTECH_OFFICER` manages AFPROTECH records only.

`ORG_OFFICER` accounts do not manage Lost and Found because Lost and Found is a USG-managed service.

Organization officer accounts may send and reply in the global Chats / Messaging room using their organization officer display name.

Because organization officer accounts are shared, important actions must require the real officer name to be entered manually.

---

### 5.5 STUDENT

The `STUDENT` role is used for individual student accounts.

Students use the mobile application as the primary student-facing interface.

Campus Connect assumes that official student data is already stored in the database before student mobile registration begins. This official stored data is called the **student master record**.

A student master record represents the school-validated student identity. It should include information such as:

- student ID
- firstname
- middlename
- lastname
- email
- course
- year level
- section
- school ID QR reference or extracted student identity value
- student record status

Student registration is treated as an **account claiming or account activation process**, not as open registration.

A student may register through the mobile application only if the submitted registration details match an existing student master record.

Required matching checks must include:

- Student ID
- full name
- email
- school ID QR scan or extracted school ID QR value

If all required checks pass, including student master record matching, school ID QR matching, and successful face registration, the student account may be automatically approved or activated.

If any required check fails, the registration must be rejected immediately and the system must not create an active student account.

The system must prevent duplicate account claims for the same student master record. Once a student master record is already linked to an active student user account, another account must not be allowed to claim the same record.

A student user account is required for:

- mobile login
- linked student master record ownership
- student ID verification
- school ID QR matching
- face registration
- attendance sign-in and sign-out
- violation records
- payment records
- personal notification delivery
- personal record viewing

Student user accounts should store or reference:

- linked student master record
- username or email
- password
- account status
- face embedding registration status
- optional approved face reference image record where formally allowed

Student course/department information must come from the linked student master record so the backend can determine the student's assigned course/department organization.

Student visibility rules:

- all students can see USG records
- IT students can see USG + SITE records
- BTLED students can see USG + PAFE records
- BFPT students can see USG + AFPROTECH records

Students must not manually switch organizations.

The backend must determine student-visible records automatically from the linked student master record.

Student mobile records should include:

- USG-owned records
- records owned by the student's assigned course/department organization

Student-facing records must show the organization label.

Examples:

- `[USG] General Assembly`
- `[SITE] Programming Seminar`
- `[PAFE] Department Activity`
- `[AFPROTECH] Organization Meeting`

A student belongs to:

- USG by default
- one assigned course/department organization based on the linked student master record

The system uses one course/department organization assignment per student for organization visibility.

---

### 5.6 SIGNATORY

The `SIGNATORY` role is used for individual signatory accounts.

Signatory users must register before using the Signatory Web Platform.

Signatory registration must collect:

- firstname
- middlename
- lastname
- email
- username
- password
- position
- signature

The signature may be provided in either of the following ways:

- drawing the signature directly inside the system
- uploading a signature image

The stored signature should support a transparent background when possible so it can be placed cleanly in exported DOCX/PDF documents.

Approved signatory signatures must appear in exported event documents and reports when the event document/report requires their signature.

If a signatory updates their stored signature later, the updated signature must apply only to future documents. It must not alter already finalized, signed, or exported documents.

Signatory accounts follow this status flow:

```text
Pending → Approved → Rejected
```

Only `SUPER_ADMIN` and `USG_OFFICER` may approve or reject signatory registrations.

Rejected signatory registrations must include a rejection reason.

A `SIGNATORY` user must not view or act on assigned documents until the account is approved.

Signatory users must have a separate, simplified web interface.

The signatory interface should include only the functions needed for event document and report signing workflows, such as:

- login
- view assigned event documents and reports
- open assigned event document/report details
- mark the assigned event document/report as `For Approval`
- mark the assigned event document/report as `For Disapproval`
- provide `Reason/s for Disapproval` when disapproving

A `SIGNATORY` user must only access assigned event documents and reports.

A `SIGNATORY` user must not access the full officer dashboard, student management, payment verification, attendance management, violation management, announcement management, event management, meeting management, Chats / Messaging, Lost and Found, or organization settings.

Signatory users are assigned to event documents or reports by officers when preparing the document or report.

Signatory users must not be able to assign themselves to documents.

Signatory actions must be recorded for traceability.

---

### 5.7 Officer Action Traceability

Some officer accounts are shared accounts.

Shared officer accounts include:

- `USG_OFFICER`
- `SITE_OFFICER`
- `PAFE_OFFICER`
- `AFPROTECH_OFFICER`

Each organization has its own shared officer account. Since several officers within the same organization may use that account, the system must ask for the real officer's name when important actions are performed.

This rule applies to all important officer actions, including:

- student master record creation or update
- student account deactivation
- event creation or major update
- meeting creation or major update
- announcement creation or major update
- attendance session opening or closing
- violation confirmation
- payment verification or rejection
- report preparation
- report checking
- report approval
- signatory assignment
- report locking or unlocking
- USG Lost and Found status update

Recommended field names include:

- `acted_by_name`
- `approved_by_name`
- `verified_by_name`
- `prepared_by_name`
- `checked_by_name`
- `posted_by_name`
- `assigned_by_name`

The exact field depends on the module and action.

The manually typed officer name is for action traceability only. It must not create a separate login account or permission level.

---

### 5.8 Access Enforcement Rules

The backend must enforce access rules for every protected workflow.

Access enforcement must consider:

- authenticated user identity
- technical role
- organization ownership
- student course/department visibility
- assigned signatory access
- workflow status
- record ownership

General enforcement rules:

- `SUPER_ADMIN` may access and manage records across all organizations.
- `SUPER_ADMIN` is the only role allowed to upload or update the global payment QR code.
- `USG_OFFICER` may manage USG-owned records only.
- `ORG_OFFICER` may manage records owned by its assigned organization only.
- `STUDENT` may view USG records plus records from their assigned course/department organization.
- `STUDENT` may access only their own personal records for attendance, violations, payments, profile, and notifications.
- Student mobile registration must match a preloaded student master record using Student ID, full name, email, and school ID QR before account activation.
- Student accounts may be auto-approved only when all required identity checks and face registration pass.
- Failed student registration matching must be rejected immediately and must not create an active student account.
- Duplicate account claims for the same student master record must be prevented.
- `SIGNATORY` may access only assigned event documents or reports after the signatory account is approved.
- Only `SUPER_ADMIN` and `USG_OFFICER` may approve or reject signatory registrations.
- Signatory signatures may be drawn in the system or uploaded as signature images.
- Signatory signature updates must apply only to future documents and must not alter finalized or exported files.
- Payment records must remain organization-owned even though there is one global payment QR code.
- Event documents and reports must support signatory assignment and signatory action tracking.
- Officer position must not be used for login, authorization, or permission control.

The frontend and mobile app must not rely on hidden UI controls alone for security. All restrictions must be enforced in the backend.

## 6. Governance Model

Campus Connect uses an **organization-scoped governance model** with a system-level administrator role.

The governance model must clearly separate:

- full system-level control
- USG-owned record management
- course/department organization record management
- student account governance
- signatory account governance
- payment QR governance
- assigned event document and report signatory access

The backend must enforce these boundaries. The frontend may show or hide menus, but backend validation remains the final authority.

---

### 6.1 System-Level Governance

The `SUPER_ADMIN` role represents the USG Moderator and is the highest system-level authority in Campus Connect.

The `SUPER_ADMIN` can access records across all organizations, including USG, SITE, PAFE, and AFPROTECH.

The `SUPER_ADMIN` may manage system records, organization-scoped records, event document records, and report records. However, the `SUPER_ADMIN` must not perform signatory approval actions for event documents or reports unless assigned through the signatory workflow.

The `SUPER_ADMIN` web interface should use the same general officer web UI structure, but it must include additional Super Admin controls for system-wide administration.

Super Admin views may show all records by default, but they must provide organization filters so records can be reviewed by organization when needed.

---

### 6.2 Organization-Level Governance

Each officer account manages only the records owned by its organization.

The `USG_OFFICER` role manages USG-owned records only. Although USG covers all students, the `USG_OFFICER` account must not automatically manage SITE, PAFE, or AFPROTECH records.

The `ORG_OFFICER` role is used by course/department organization officer accounts. The organization field determines which records the account can manage.

Examples:

- `role = ORG_OFFICER`, `organization = SITE` manages SITE records only.
- `role = ORG_OFFICER`, `organization = PAFE` manages PAFE records only.
- `role = ORG_OFFICER`, `organization = AFPROTECH` manages AFPROTECH records only.

Organization officers must not access, edit, approve, reject, or delete records owned by another organization.

---

### 6.3 Student Account Governance

Student identity is based on preloaded student master records.

A **student master record** is the official student data already stored in the database before the student creates or activates a mobile account.

Student registration and account activation must follow this rule:

- the student enters the required registration details through the mobile app
- the system checks the submitted Student ID, full name, email, and school ID QR against the preloaded student master record
- if all required checks pass and face registration succeeds, the student account may be automatically approved or activated
- if any required check fails, the registration must be rejected immediately
- the system must prevent duplicate account claims for the same student master record

Student master record and account control must follow this governance rule:

- `SUPER_ADMIN` can add, import, edit, and deactivate student master records and student user accounts where necessary.
- `USG_OFFICER` may be allowed to help review student records only if the system explicitly grants that workflow.
- `ORG_OFFICER` accounts cannot manage official student master records or override student registration matching.

Student registration rejection caused by failed matching does not require manual officer approval. The system rejects the attempt because the submitted identity does not match the stored student master record.

Student course/department information must come from the linked student master record and determines which course/department organization records the student may view in addition to USG records.

---

### 6.4 Signatory Account Governance

Signatory accounts are individual accounts.

Signatory users must register before using the Signatory Web Platform.

Signatory registration must include firstname, middlename, lastname, email, username, password, position, and signature.

The signature may be drawn directly inside the system or uploaded as a signature image. The stored signature should support a transparent background when possible.

Signatory account approval follows this rule:

- `SUPER_ADMIN` can approve or reject signatory registrations.
- `USG_OFFICER` can approve or reject signatory registrations.
- `ORG_OFFICER` accounts cannot approve or reject signatory registrations.

Signatory account status follows:

```text
Pending → Approved → Rejected
```

Rejected signatory registrations must include a rejection reason.

A signatory account must be approved before the user can access assigned event documents or reports.

If a signatory updates their signature later, the updated signature applies only to future documents and must not alter already finalized, signed, or exported documents.

---

### 6.5 Payment QR Governance

Campus Connect uses one global payment QR code for all organizations.

Only `SUPER_ADMIN` can upload or replace the global payment QR code.

The system must keep a history of previous payment QR uploads. The history should support auditability by recording information such as upload date, uploaded-by account, active/inactive status, and file/reference metadata where applicable.

Although the payment QR code is global, payment records must still be organization-owned. Officers must verify payment submissions only under their own organization records.

Examples:

- `USG_OFFICER` verifies USG payment records only.
- `SITE_OFFICER` verifies SITE payment records only.
- `PAFE_OFFICER` verifies PAFE payment records only.
- `AFPROTECH_OFFICER` verifies AFPROTECH payment records only.

---

### 6.6 Signatory Governance

`SIGNATORY` users are outside normal officer management.

A `SIGNATORY` account must not manage events, meetings, announcements, attendance, violations, payments, students, organizations, or dashboards.

A `SIGNATORY` user may only access assigned event documents and reports after the signatory account is approved.

For assigned event documents and reports, the signatory action terms must follow the original document format:

- **For Approval**
- **For Disapproval**
- **Reason/s for Disapproval**

Officers assign signatories when preparing event documents or reports. The backend must prevent signatories from accessing event documents or reports that were not assigned to them.

---

### 6.7 Governance Enforcement Rules

The backend must enforce all governance rules through authentication, authorization, organization ownership checks, workflow validation, and assignment validation.

Required enforcement rules:

- `SUPER_ADMIN` can access all organizations and use organization filters when reviewing records.
- `USG_OFFICER` can manage only USG-owned records.
- `ORG_OFFICER` can manage only records owned by its assigned organization.
- `STUDENT` users can view USG records plus records from their assigned course/department organization.
- `SIGNATORY` users can access only assigned event documents or reports after their accounts are approved.
- Only `SUPER_ADMIN` and `USG_OFFICER` can approve or reject signatory registrations.
- `ORG_OFFICER` accounts must not approve or reject signatory registrations.
- Signatory signature updates must apply only to future documents and must not alter finalized or exported files.
- Only `SUPER_ADMIN` can upload or replace the global payment QR code.
- Payment QR upload history must be retained.
- Student registration must be validated against preloaded student master records before a student account is activated.
- The system must prevent duplicate account claims for the same student master record.
- Event document and report signatory actions must follow the assigned signatory workflow.
- Shared officer accounts must require manually typed real officer names for important actions.

Framework-level administrator access may exist for backend maintenance and development, but it must not replace the official application governance model defined in this section.

## 7. Core Functional Modules

The system must follow the module grouping below.

All major module records must be organization-owned unless the record is explicitly defined as system-wide.

Organization-owned records include events, meetings, announcements, attendance sessions, attendance records, violations, payment records, reports, and notifications.

Global Chats / Messaging records are system-wide records. They are not owned by a single organization, but sender display and moderation rules must still be enforced.

Lost and Found records are USG-managed service records. They are visible to all students but may only be managed by `USG_OFFICER` and `SUPER_ADMIN`.

Access rules for all modules:

- `SUPER_ADMIN` may view and manage records across all organizations, but must not perform event document or report signatory approval actions unless assigned through the signatory workflow.
- `USG_OFFICER` may manage only USG-owned records.
- `ORG_OFFICER` may manage only records owned by its assigned organization, such as SITE, PAFE, or AFPROTECH.
- `STUDENT` users may view USG records and records from their assigned course/department organization.
- `SIGNATORY` users may only access assigned event documents and reports after their account is approved.

If `SUPER_ADMIN` creates or edits an organization-owned record, the target organization must be explicitly selected or clearly assigned by the system.

---

## 7.1 Menu

### Dashboard

The Dashboard is the main landing page for the Officer / Super Admin Web Platform.

The dashboard UI already exists and must be wired to backend data during development.

Dashboard behavior must follow role-based access:

- `SUPER_ADMIN` dashboard may show all organization records by default and must support organization filtering.
- `USG_OFFICER` dashboard must show only USG-owned records.
- `ORG_OFFICER` dashboard must show only records owned by the officer account's assigned organization.
- `SIGNATORY` users do not use the officer dashboard. They use a separate simplified web interface for assigned event documents and reports.
- `STUDENT` users do not use the web dashboard. They use the student mobile application.

The overview does not define exact dashboard cards or charts. Specific dashboard UI and API wiring details should be handled in later development files.

The dashboard should generally support role-appropriate visibility over:

- dashboard calendar for event and meeting schedules
- schedule-only cross-organization calendar visibility for officer accounts
- schedule conflict checking for events and meetings
- events
- meetings
- announcements
- attendance summaries
- student account activations or failed registration monitoring where allowed
- pending violations
- payment submissions
- reports
- notifications
- global payment QR controls for `SUPER_ADMIN` only

### Dashboard Calendar

The Dashboard must include a calendar for viewing scheduled events and meetings.

On the Officer / Super Admin Web Platform, the calendar is shared across organizations for schedule visibility and conflict prevention. Officer accounts may view schedule-only calendar details from other organizations, such as:

- title
- organization
- date/time
- venue

Officer accounts must not access full internal event or meeting details from another organization through the shared calendar.

The system must check scheduling conflicts for both events and meetings. A schedule should be blocked only when another event or meeting uses the same venue at the same time. If the same time is used but the venue is different, the system may allow the schedule.

Internal officer meetings may be shown or hidden from the shared calendar depending on the officer’s selected setting.

The Student Mobile Application may include a calendar that shows approved or published events and meetings from USG and the student’s assigned course/department organization. Selecting a calendar item should open the allowed event or meeting details.

---

## 7.2 Management

### Events

The Events module manages organization-owned event proposals and approved event records.

Event creation must not be treated only as a simple event details form. The system must support event preparation through fixed event-document templates that reflect the organization's actual approval workflow.

Required or supported event-related document templates may include:

- SARF / Student Activity Request Form
- Letter
- Budget Proposal
- Partial Program of Activities

These event document templates must use controlled editable fields. Users may fill in allowed fields, but they must not freely change the document format or structure.

For table-based event documents such as the Budget Proposal and Partial Program of Activities, the system may allow adding rows inside controlled tables while keeping the template structure fixed.

Event documents may require signatory review. Signatories may be assigned per document or per whole event, depending on the original template requirement.

The event workflow should follow:

```text
Draft → For Approval → Approved → Published / Active
```

All required event documents must be approved before the event can be approved and published or activated.

If a signatory marks an event document as **For Disapproval**, the signatory must provide **Reason/s for Disapproval**. The event may remain under **For Approval**, but the specific signatory response must be marked **For Disapproval** until the officer corrects and resubmits the document.

Officer-side and Super Admin features include:

- create event proposals
- fill allowed fields in event document templates
- prepare SARF, Letter, Budget Proposal, and Partial Program of Activities templates where required
- add controlled table rows for budget items or program activities where the template allows it
- assign event ownership to the correct organization
- assign signatories per document or per event, depending on the template
- submit event documents for approval
- correct and resubmit documents marked **For Disapproval**
- approve, publish, or activate events after required documents are approved
- export finalized event documents as DOCX or PDF after required signatories are completed
- view approved event records and related attendance records where applicable

Access rules:

- `SUPER_ADMIN` may manage event proposals, approved events, and finalized event document exports across organizations and filter them by organization.
- `USG_OFFICER` may manage and export only USG event proposals and approved USG event documents.
- `ORG_OFFICER` may manage and export only event proposals and approved event documents owned by its assigned organization.
- `SIGNATORY` users may access only event documents assigned to them after their signatory account is approved. They must not manage event export controls unless a separate signed-copy viewing rule is added.

Student-side features include:

- view published or active events from USG and the student's assigned course/department organization
- view event details that are allowed for student visibility
- participate in attendance when an attendance session is active and visible to the student

Student-facing event records must show the organization label.

Approved events may be linked to attendance sessions. Attendance-related violation settings, such as community service hours and money equivalent values, must be configured in the Attendance session setup rather than inside the event proposal document templates.

Finalized event documents may be exported as **DOCX** or **PDF** after all required signatories are completed. This applies to event documents such as SARF, Letter, Budget Proposal, and Partial Program of Activities.

The exported event document must include the filled-in template fields, completed signatories or signatures, and approval or disapproval records where applicable.

Allowed users should be able to download exported event documents, and the system should keep export history for traceability. Export history should record details such as export format, exported by account, manually entered officer name when applicable, export date/time, and related event/document reference.

Events and Reports are separate modules, but both must follow controlled-template, signatory workflow, and finalized document export rules where documents require formal approval.

### Meetings

The Meetings module is separate from the Events module.

Meetings must support:

- General Assembly-type meetings when applicable
- USG officer/internal meetings
- organization officer/internal meetings

Officer-side and Super Admin features include:

- create meetings
- update meeting details
- assign meeting ownership to the correct organization
- set meeting schedule and venue
- open attendance sessions when needed
- view meeting attendance results

Access rules:

- `SUPER_ADMIN` may manage meetings across organizations and filter them by organization.
- `USG_OFFICER` may manage only USG meetings.
- `ORG_OFFICER` may manage only meetings owned by its assigned organization.

Student-side visibility depends on the meeting type and organization coverage.

General Assembly-type meetings may be visible to covered students. Internal officer meetings may remain officer-side only.

Student-facing meeting records must show the organization label when visible to students.

---

## 7.3 Community

### Announcements

The Announcements module is used for official organization notices and updates.

Officer-side and Super Admin features include:

- create announcements
- update announcements
- publish announcements
- archive announcements where applicable
- assign announcement ownership to the correct organization

Access rules:

- `SUPER_ADMIN` may manage announcements across organizations and filter them by organization.
- `USG_OFFICER` may manage only USG announcements.
- `ORG_OFFICER` may manage only announcements owned by its assigned organization.

Student-side features include:

- view published announcements from USG and the student's assigned course/department organization
- receive notification records for relevant announcements, with mobile push notifications where enabled

Student-facing announcement records must show the organization label.

Students must not create official announcements.

### Chats / Messaging

The Chats / Messaging feature supports global communication between students, officer accounts, and the `SUPER_ADMIN`.

Unlike announcements, Chats / Messaging is a global communication space. It is not separated by organization visibility in the same way as events, meetings, announcements, attendance, payments, or reports.

The system must provide one global chat room for:

- all `STUDENT` users
- `USG_OFFICER`
- `ORG_OFFICER` accounts
- `SUPER_ADMIN`

`SIGNATORY` users must not access Chats / Messaging.

Outside instructors, staff, or administrators must not access Chats / Messaging unless they are official Campus Connect system users with an allowed role.

Allowed chat participants may send and reply to messages:

- students may send and reply to messages
- `USG_OFFICER` may send and reply as `USG Officer`
- `ORG_OFFICER` accounts may send and reply using their organization officer display name, such as `SITE Officer`, `PAFE Officer`, or `AFPROTECH Officer`
- `SUPER_ADMIN` may send, reply, and moderate all chat messages

Officer chat messages should display the organization account identity rather than requiring the real officer name for every message.

Examples:

- `USG Officer`
- `SITE Officer`
- `PAFE Officer`
- `AFPROTECH Officer`
- `Super Admin`
- `Student`

Chat moderation must be controlled by `SUPER_ADMIN`.

Moderation may include reviewing, hiding, or deleting inappropriate messages where supported by the implementation.

Officer accounts may send and reply in chat, but normal officer accounts must not have full moderation authority.

Technical rule for developers:

- Chats / Messaging is a system-wide communication feature.
- It is an exception to the normal organization-scoped visibility rule.
- The backend must still enforce allowed-role access.
- `SIGNATORY` users must be blocked from chat access.
- Chat sender labels must clearly identify the sender type or organization account.
- `SUPER_ADMIN` must be the role responsible for chat moderation.

---

## 7.4 Services

### Attendance

Attendance is a core service module.

Attendance sessions must be organization-owned. Students may attend sessions from USG and from their assigned course/department organization when those sessions are active and visible to them.

Attendance sessions may be linked to an event or meeting.

Attendance must use:

- authenticated student mobile login
- active attendance session selection
- physical school ID QR scanning through the mobile camera
- school ID QR matching against the logged-in student account
- geolocation validation
- facial recognition validation
- separate sign-in and sign-out checkpoint records
- server-side duplicate prevention
- server-side validation of open and close time windows

Attendance requires both sign-in and sign-out.

Both sign-in and sign-out require the full validation process:

```text
school ID QR scan → geolocation check → facial recognition check
```

Sign-in and sign-out must be treated as separate attendance checkpoints. A valid sign-out may still be recorded even if the student missed sign-in, but the missing sign-in must still be detected as a pending violation.

Attendance status must support:

- `PRESENT`
- `INCOMPLETE`
- `ABSENT`

Attendance status must follow this rule:

```text
Valid sign-in + valid sign-out = PRESENT
Valid sign-in + missing sign-out = INCOMPLETE
Missing sign-in + valid sign-out = INCOMPLETE
Missing sign-in + missing sign-out = ABSENT
```

The system must not define a `LATE` attendance status in this overview.

Missing attendance checkpoints may create pending violations.

Violation detection must follow this rule:

```text
Missing sign-in → Pending sign-in violation
Missing sign-out → Pending sign-out violation
Missing both → Two pending violations
```

Each missing checkpoint may have its own community service hour value and money equivalent configured by the officer for the attendance session.

Example:

```text
Missing sign-in = 2 community service hours = ₱100
Missing sign-out = 2 community service hours = ₱100
Missing both = 4 community service hours = ₱200 total
```

Pending violations become official only after officer confirmation.

Students should be able to see which attendance checkpoint they missed, the equivalent community service hours, the money equivalent when applicable, and the violation status.

#### Attendance Session Flow

The required attendance flow is:

```text
Officer or Super Admin opens an organization-owned attendance session
→ Officer or Super Admin sets the required sign-in/sign-out rules, community service hour values, and money equivalent values
→ Student opens mobile app
→ Student selects active attendance session from the visible list
→ Student scans physical school ID QR using mobile camera
→ Backend checks that scanned QR identity matches logged-in student
→ Backend validates geolocation
→ Backend validates facial recognition
→ Sign-in is recorded
→ Student repeats the same validation for sign-out
→ Attendance status is computed as PRESENT, INCOMPLETE, or ABSENT
→ Missing checkpoint violations are prepared as pending violations when applicable
```

If multiple visible attendance sessions are active, the mobile app must show a list and allow the student to manually select the correct session.

The officer or Super Admin sets the attendance session open time and close time.

The backend must reject attendance attempts outside the allowed session time window.

Access rules:

- `SUPER_ADMIN` may manage attendance sessions and records across organizations.
- `USG_OFFICER` may manage only USG attendance sessions and records.
- `ORG_OFFICER` may manage only attendance sessions and records owned by its assigned organization.
- `STUDENT` users may only submit attendance for sessions visible to them.

#### Facial Recognition Rule

Facial recognition is required for attendance validation.

Students register their face during account registration.

Face recognition must primarily rely on **face embeddings** for long-term identity matching.

Raw face images should not be stored permanently by default. The system should use face images only for temporary processing during registration and attendance verification unless permanent face image reference storage is formally approved by the school, adviser, or panel.

If approved, face reference images may be stored through Cloudinary with strict access control. PostgreSQL must store the official Cloudinary reference, such as the `public_id` and secure URL, together with the student face registration record. Firebase must not be used as the official face image database; Firebase remains limited to push notification delivery through FCM.

If the submitted face registration is unclear or unsuitable, the student registration must be rejected immediately because all required registration checks must pass before account activation.

Student registration does not require manual officer approval by default. The system may automatically approve or activate the account only when student master record matching, school ID QR matching, and face registration all succeed.

Facial recognition is only used for attendance validation and face registration setup. It is not used as the main login method.

### Violation

The Violation module tracks attendance-related accountability records.

Violation records must be organization-owned and must be linked to the attendance session or event/meeting that produced the missing checkpoint.

The system may detect missing sign-in and missing sign-out checkpoints from attendance records.

The violation workflow is:

```text
Missing sign-in/sign-out checkpoint → Pending violation → Officer confirms → Official violation
```

The officer confirms pending violations manually before they become official.

Each missing checkpoint may produce its own pending violation.

Examples:

- missing sign-in only may produce a pending sign-in violation
- missing sign-out only may produce a pending sign-out violation
- missing both sign-in and sign-out may produce two pending violations

Community service hours and money equivalent values must come from the values configured by the officer for the attendance session.

Students should be able to view:

- the event or meeting related to the violation
- the missed checkpoint, such as sign-in or sign-out
- the equivalent community service hours
- the money equivalent when applicable
- whether the violation is pending or official

Access rules:

- `SUPER_ADMIN` may view and manage violations across organizations.
- `USG_OFFICER` may confirm only USG-owned pending violations.
- `ORG_OFFICER` may confirm only pending violations owned by its assigned organization.
- `STUDENT` users may view only their own violation records.

After an officer confirms a pending violation, the system may automatically create the related payment obligation based on the configured money equivalent. The system must still keep officer confirmation before a missing attendance checkpoint becomes an official violation or payment obligation.

### Lost and Found

Lost and Found is a **USG-managed service**.

It is not managed separately by SITE, PAFE, or AFPROTECH.

Only `USG_OFFICER` and `SUPER_ADMIN` may manage Lost and Found records.

Allowed management actions include:

- post found item records
- upload or update found item images where applicable
- update found item details
- mark found items as claimed

Lost and Found item images may be stored through Cloudinary. PostgreSQL must store the official Lost and Found record and the Cloudinary image reference, such as the `public_id` and secure image URL. Cloudinary stores the image file only; Django/PostgreSQL remains the source of truth for item status, ownership, visibility, and access control.

`ORG_OFFICER` accounts must not access or manage Lost and Found records.

All students may view posted USG Lost and Found records because USG covers the full student body.

Student-side behavior:

- students can view found item records in the mobile application
- students do not submit lost-item reports inside the system
- students do not submit claim requests inside the system
- students must personally go to the responsible USG office or person to claim an item

The Lost and Found status flow is:

```text
Found → Claimed
```

### Payment

The Payment module supports tracking and verification of student payments, contributions, and payment obligations connected to confirmed violations.

Payment obligations may be created manually by authorized officers or generated from confirmed violations based on the money equivalent configured in the attendance session.

The system must support two payment paths:

1. **System-assisted payment tracking**
   - The student views the global payment QR code in the system.
   - The student pays through an external payment method such as GCash or another accepted payment channel.
   - The student uploads a receipt screenshot as proof of payment.
   - An authorized officer reviews and verifies or rejects the submitted proof.

2. **Manual payment recording**
   - The student pays directly through the accepted manual organization process.
   - The authorized officer records and verifies the payment in the system.
   - The student must not mark their own payment as paid or verified.

The system uses **one global payment QR code** for payment scanning across all organizations.

Only `SUPER_ADMIN` may upload or replace the global payment QR code.

The system must keep a history of old payment QR uploads.

Payment records must still be organization-owned even if one global QR code is used.

The system does not process payments internally.

Students may pay through external methods such as GCash or other accepted payment channels outside the system, or they may pay manually through the organization's accepted process.

The system records and verifies payment evidence and payment status only.

Payment records must include a payment method.

Recommended payment method values include:

```text
QR_RECEIPT_UPLOAD
MANUAL_PAYMENT
OTHER_EXTERNAL_PAYMENT
```

For system-assisted receipt upload, the payment status flow is:

```text
Unpaid → Submitted → Verified / Rejected
```

For manual payment recording, the payment status flow may move directly from:

```text
Unpaid → Verified
```

Student-side features include:

- view payment obligations or records from USG and the student's assigned course/department organization
- view the global payment QR code when payment is required
- upload receipt screenshots as proof of payment when using the system-assisted payment path
- view payment method and payment status
- receive basic in-app notification records for payment verification results

Officer-side and Super Admin features include:

- create or manage payment obligations within the allowed organization scope
- generate payment obligations from confirmed violations based on configured money equivalent values
- view submitted receipt screenshots
- record manual payments received through the accepted manual process
- verify valid payments
- reject invalid, unclear, duplicated, or mismatched receipt submissions
- enter the real verifying officer name during verification or rejection when using an organization shared officer account

Access rules:

- `SUPER_ADMIN` may view and manage payment records across organizations.
- `USG_OFFICER` may verify only USG-owned payment records.
- `ORG_OFFICER` may verify only payment records owned by its assigned organization.
- `STUDENT` users may view their own payment records and submit proof when required.
- `STUDENT` users must not verify their own payments.

Payment verification is an officer-reviewed workflow whether the payment was submitted through uploaded proof or recorded manually by an officer.

---

## 7.5 Reports

The Reports module supports official organization reports through fixed templates.

Report types include:

- Annual Work and Financial Plan (AWFP)
- Financial Report
- Auditor’s Report
- Accomplishment Report

Reports must use a structured-template approach.

Report records must be organization-owned.

Users may only fill allowed fields.

The system must not behave like a full word processor or unrestricted document editor.

Report templates are controlled. The system may support controlled dynamic fields when the original report format requires additional structured input.

Dynamic fields must still follow the controlled-template rule and must not turn the report module into a free-form word processor.

### Report Preparation

Officer-side and Super Admin features include:

- create report records
- fill allowed report fields
- assign the report to the correct organization
- assign required signatory users when preparing the report
- enter manually typed officer names where the original report format requires names such as Prepared by, Checked by, or Approved by
- lock or finalize reports
- unlock reports when editing is needed
- export finalized reports as DOCX or PDF after required signatories are completed

Access rules:

- `SUPER_ADMIN` may view and manage report records across organizations but must not perform report signing unless assigned as a `SIGNATORY`.
- `USG_OFFICER` may prepare, manage, and export only USG-owned reports.
- `ORG_OFFICER` may prepare, manage, and export only reports owned by its assigned organization.
- `SIGNATORY` users may review assigned event documents and reports but do not manage export controls unless a separate signed-copy viewing rule is added.

Because officer accounts are shared, important report actions must require the real officer name to be typed manually when the action is performed by a shared officer account.

### Report Signatory Workflow

Signatory users have individual accounts and use a separate simplified web interface.

A signatory account must be approved before the user can access assigned event documents and reports.

Signatory users may only access assigned event documents and reports.

When an event document or report is assigned to a `SIGNATORY`, the signatory may mark it as:

- **For Approval**
- **For Disapproval**

If the signatory marks an event document or report as **For Disapproval**, the system must require:

- **Reason/s for Disapproval**

Approved signatory signatures must be included in exported DOCX/PDF files when the event document or report requires their signature.

Signatory users must not manage organization records, create reports, edit report contents, verify payments, manage attendance, or access unrelated reports.

### Report Locking

Reports may be locked or finalized.

Locked reports cannot be edited through normal editing behavior.

A locked report may still be edited after it is unlocked.

Any allowed officer account or `SUPER_ADMIN` may unlock a locked report directly.

Unlocking does not require a reason.

### Report Output Direction

The system stores reports as system records.

Finalized reports may be exported as **DOCX** or **PDF** after all required signatories are completed. This applies to reports such as AWFP, Financial Report, Auditor’s Report, and Accomplishment Report.

The exported report must include the filled-in template fields, completed signatories or signatures, and approval or disapproval records where applicable.

Allowed users should be able to download exported reports, and the system should keep export history for traceability. Export history should record details such as export format, exported by account, manually entered officer name when applicable, export date/time, and related report reference.

Report export must preserve the controlled-template rule. Exporting a report must not turn the report module into an unrestricted word processor.

---

## 8. Notifications

Campus Connect includes database-backed in-app notifications and may support mobile push notifications where enabled.

Notifications may appear in the relevant interface based on user role:

- Officer / Super Admin Web Platform
- Signatory Web Platform for assigned event document or report updates
- Student Mobile Application

Notification records must respect access rules. Officer notifications must be limited to the logged-in officer account's organization. Student notifications may come from USG and the student's assigned course/department organization. Signatory notifications must be limited to assigned event documents and reports for the approved signatory account.

In-app notifications must be stored as system records in the database. Mobile push notifications may be delivered through Firebase Cloud Messaging (FCM), but FCM must only be used for push delivery. Django and PostgreSQL remain the main backend and data source for notification rules, recipient selection, and notification history.

Notification records may cover:

- student account activation or rejected registration attempt
- signatory account approval or rejection
- new announcements
- event or meeting updates
- attendance records
- pending or confirmed violations
- payment submission or verification results
- event document/report-related updates where applicable
- signatory assignment, approval, or disapproval updates where applicable

The system may store notification records and show them inside the application interfaces. Push notifications may be sent when enabled, but they must follow the same backend access and recipient rules.

---

## 9. High-Level Workflow Principles

### 9.1 Centralized Backend Enforcement

All important workflows must be validated by the backend.

The client interface must not be trusted as the final authority for:

- student identity
- officer access
- organization visibility
- attendance validity
- face verification result
- geolocation validity
- payment status
- violation status
- event document/report lock status

### 9.2 Organization Visibility Rule

The backend must enforce organization visibility for both officer and student workflows.

Officer-side access rules:

- an officer account may only view and manage records owned by its assigned organization
- officer-created records must be attached to the officer account's organization
- `USG_OFFICER` must not automatically access SITE, PAFE, or AFPROTECH records

Student-side access rules:

- every student may view USG records
- a student may also view records from the assigned course/department organization derived from the student profile
- student-facing records should show the organization label
- students must not manually switch organization context
- Chats / Messaging is a system-wide exception where students, officer accounts, and `SUPER_ADMIN` may participate in one global chat room

### 9.3 Student Identity Rule

Student identity must come from a linked student user account and preloaded student master record.

During student registration, the submitted Student ID, full name, email, and school ID QR must match an existing student master record in the database.

If all required identity checks pass and face registration succeeds, the student account may be automatically approved or activated.

If any required identity check fails, the registration must be rejected immediately and the system must not create an active student account.

The system must prevent duplicate account claims for the same student master record.

During attendance, the scanned school ID QR must match the logged-in student account and the linked student master record.

If the scanned QR belongs to another student, attendance must be rejected.

### 9.4 Attendance Integrity Rule

Attendance must not be recorded unless all required checks pass.

For both sign-in and sign-out, the system must validate:

- active selected attendance session
- student authentication
- school ID QR match
- geolocation
- facial recognition
- time window
- duplicate prevention

### 9.5 Violation Control Rule

The system may detect missing sign-in or sign-out checkpoints, but violations become official only after officer confirmation. Confirmed violations may generate payment obligations based on the configured money equivalent.

### 9.6 Payment Control Rule

Payments are tracked, not processed.

A student-submitted receipt screenshot must be reviewed by an officer before the payment status becomes verified or rejected. For manual payments, an authorized officer records and verifies the payment in the system.

### 9.7 Report Template and Export Rule

Report and event document formats are controlled.

Users may only fill allowed fields inside fixed templates.

Finalized event documents and reports may be exported as DOCX or PDF only after required signatories are completed. Exported files must preserve the official template structure and include completed signatories or signatures where applicable.

### 9.8 Officer Attribution Rule

For important officer actions, the system must request a manually typed real officer name because each organization officer account is shared within that organization.

---

## 10. Summary

Campus Connect is an organization-scoped e-governance and student services platform for USTP-Oroquieta student organization operations.

The first implementation may start with USG, but the system must be designed so SITE, PAFE, and AFPROTECH can be added later without changing the main UI or module structure.

The system uses five application roles:

- `SUPER_ADMIN`
- `USG_OFFICER`
- `ORG_OFFICER`
- `STUDENT`
- `SIGNATORY`

Officer account examples include:

- `USG_OFFICER`
- `SITE_OFFICER`
- `PAFE_OFFICER`
- `AFPROTECH_OFFICER`

Each organization has its own shared officer account. Each officer account may only manage records owned by its organization, while `SUPER_ADMIN` has system-wide access and organization filtering.

Students may view USG records and records from their assigned course/department organization. Signatory users use a separate web platform and may only access assigned event documents and reports after approval.

The system is organized into the following modules:

- Menu: Dashboard
- Management: Events, Meetings
- Community: Announcements, Chats / Messaging
- Services: Attendance, Violation, Lost and Found, Payment
- Reports: AWFP, Financial Report, Auditor’s Report, Accomplishment Report

Lost and Found is a USG-managed service. All students may view USG-posted found items, including item images stored through Cloudinary where applicable, but only `USG_OFFICER` and `SUPER_ADMIN` may manage them.

Attendance is validated through student login, active session selection, physical school ID QR scanning, geolocation, and facial recognition. Both sign-in and sign-out are required, and attendance status may be `PRESENT`, `INCOMPLETE`, or `ABSENT` based on completed checkpoints.

Payments are made externally and tracked through either uploaded receipt screenshots or officer-recorded manual payments. Confirmed violations may connect to payment obligations when required by the organization workflow.

Event documents and reports use fixed templates with controlled editable fields and may support controlled dynamic fields when the original format requires them. Finalized event documents and reports may be exported as DOCX or PDF after required signatories are completed, and the system should keep export history.

The backend is the enforcement boundary for authentication, organization visibility, validation, workflow rules, and record integrity.