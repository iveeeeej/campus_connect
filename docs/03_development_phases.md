# Development Phases

This file defines the development roadmap for **Campus Connect: University Student e-Governance and Services Platform**.

The roadmap is written as a clean development plan for an LLM agent or developer. It does not track old implementation progress, completed tasks, or dated updates. Each phase describes what should be built, in what order, and what rules must be followed.

This roadmap must align with the latest project overview. The source of truth for system behavior is:

- organization-scoped Campus Connect design
- five-role access model
- Officer / Super Admin Web Platform
- Signatory Web Platform
- Student Mobile Application
- fixed event document and report templates
- school ID QR + geolocation + facial recognition attendance
- USG-only Lost and Found
- external payment tracking and manual payment recording
- controlled export of finalized event documents and reports

Removed old scope items must not be reintroduced unless formally approved later. These include Borrow Requests, Campus Tour, President’s Report, Resolution Management, and Accomplishment Report analytics.

---

## Roadmap Principles

The development roadmap follows these principles:

- Build the backend foundation before UI-heavy workflows.
- Define roles, organizations, permissions, and ownership rules early.
- Keep business rules enforced by the backend, not only by the frontend.
- Build officer-side workflows before student-side mobile workflows when the officer workflow creates the records students will use.
- Build signatory-related workflows first through event documents, then reuse them for reports.
- Keep external payment processing separate from system payment tracking.
- Keep advanced enhancements separate from the first complete system build.

Each phase uses the following structure:

### Purpose
Explains why the phase exists.

### Build Scope
Lists the major modules or features included in the phase.

### Development Tasks
Defines the implementation work expected in the phase.

### Access and Workflow Rules
Defines role, organization, and workflow restrictions that must be followed.

### Deliverables
Defines the expected output after the phase is completed.

---

## Phase 1 – Foundation, Roles, and Organization Model

### Purpose

Establish the technical foundation, identity model, account rules, organization ownership, and backend access enforcement required by all later phases.

This phase prepares the system to support the five-role model and organization-scoped records before the main modules are built.

### Build Scope

- Backend project structure
- Database configuration
- Authentication foundation
- Five application roles
- Organization model
- Shared officer account model
- Student account model
- Basic authorization and ownership enforcement
- API-first backend structure
- System-wide configuration foundation

### Development Tasks

#### Backend Foundation

- Set up the backend project structure.
- Configure the database layer.
- Configure environment-based settings.
- Establish reusable API routing conventions.
- Establish centralized validation and error response patterns.
- Configure logging for development and production readiness.

#### Authentication and Roles

- Implement authentication for web and mobile clients.
- Define the technical role names:

```text
SUPER_ADMIN
USG_OFFICER
ORG_OFFICER
STUDENT
SIGNATORY
```

- Define the `SIGNATORY` role in the role model early, even if the signatory registration UI is built later in Phase 3.
- Implement role-based authorization helpers.
- Implement protected API access patterns.
- Ensure the frontend is not treated as the final authority for access control.

#### Organization Model

- Create the organization data model.
- Support initial organization values:

```text
USG
SITE
PAFE
AFPROTECH
```

- Define organization ownership fields for records that must belong to an organization.
- Prepare the database design so the first rollout may start with USG, while SITE, PAFE, and AFPROTECH can be added later without redesigning the system.

#### Shared Officer Accounts

- Implement shared organization officer account support.
- Support `USG_OFFICER` as a separate role.
- Support `ORG_OFFICER` with an organization field.
- Prepare officer account examples:

```text
username: USG_OFFICER
role: USG_OFFICER
organization: USG
```

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

#### Student Accounts

- Implement the student account structure.
- Store student identity and profile fields needed by later workflows:
  - student ID
  - password
  - email
  - firstname
  - middlename
  - lastname
  - course
  - year level
  - section
  - account status
  - school ID QR reference or extracted student identity value
  - face embedding registration status
- Implement student status flow:

```text
Pending → Approved → Rejected
```

- Prepare rejection reason support.
- Prepare student visibility rules based on course or department:
  - IT → USG + SITE
  - BTLED → USG + PAFE
  - BFPT → USG + AFPROTECH

#### Super Admin Foundation

- Create the `SUPER_ADMIN` / USG Moderator role.
- Prepare full system-wide access support.
- Prepare organization filtering support for Super Admin views.
- Prepare Super Admin-only capability for global payment QR management, which will be implemented in Phase 5.
- Prepare Super Admin student account management permissions:
  - add students
  - edit students
  - approve students
  - reject students
  - deactivate students

#### Access Enforcement Foundation

- Implement backend rules for:
  - authenticated user identity
  - technical role
  - organization ownership
  - student course/department visibility
  - workflow status
  - record ownership
- Prepare assignment-scoped access for `SIGNATORY`, even if the signatory workflow is built later.

### Access and Workflow Rules

- `SUPER_ADMIN` must have system-wide access.
- `USG_OFFICER` must manage only USG-owned records.
- `ORG_OFFICER` must manage only records owned by its assigned organization.
- `STUDENT` must only access their own personal records and visible USG + assigned organization records.
- `SIGNATORY` must be defined as a role but should not have active document access until the signatory workflow is built.
- Officer position names such as president, treasurer, auditor, or adviser must not be used as login roles or authorization roles.
- Student registration approval must be handled only by allowed roles.
- Backend authorization must be enforced even if the UI hides restricted buttons.

### Deliverables

- Backend foundation ready for module development.
- Five technical roles defined.
- Organization model created.
- Shared officer account model prepared.
- Student account model and status flow defined.
- Initial backend authentication and authorization rules implemented.
- API-first foundation ready for officer web, signatory web, and student mobile clients.

---

## Phase 2 – Officer / Super Admin Web Platform Core

### Purpose

Build the first officer-facing web platform foundation used by `SUPER_ADMIN`, `USG_OFFICER`, and `ORG_OFFICER` users.

This phase establishes the main administrative interface, dashboard, organization filtering, announcements, and calendar-based scheduling visibility.

### Build Scope

- Officer / Super Admin web layout
- Login and protected web access
- Dashboard foundation
- Super Admin organization filtering
- Officer organization-scoped dashboard views
- Dashboard calendar
- Schedule conflict checking
- Announcements
- Notification foundation for officer web users

### Development Tasks

#### Officer Web Platform Base

- Build the officer web login flow.
- Connect authenticated web sessions to backend APIs.
- Create shared web layout components:
  - sidebar navigation
  - topbar/header
  - dashboard container
  - table/list views
  - form dialogs
  - notification area
- Support role-aware menu visibility.

#### Super Admin Controls

- Add Super Admin-only controls for system-wide management.
- Add organization filter controls for `SUPER_ADMIN`.
- Ensure `SUPER_ADMIN` can view all organization records while normal officer accounts remain organization-scoped.

#### Dashboard

- Connect the existing dashboard UI to backend data.
- Show role-appropriate dashboard summaries.
- Support organization-scoped dashboard data for:
  - `USG_OFFICER`
  - `ORG_OFFICER`
- Support cross-organization dashboard visibility for `SUPER_ADMIN`.

#### Dashboard Calendar

- Add a dashboard calendar for events and meetings.
- Allow all officer accounts to view schedule-only calendar items across organizations.
- Schedule-only details should include:
  - title
  - organization
  - date/time
  - venue
- Prevent officer accounts from accessing full internal event or meeting details of another organization through the calendar.
- Add organization filtering for `SUPER_ADMIN`.

#### Schedule Conflict Checking

- Implement conflict checking for events and meetings.
- Block scheduling only when another event or meeting uses the same venue at the same time.
- Allow same-time schedules if the venue is different.
- Allow internal officer meetings to be shown or hidden from the shared calendar based on officer settings.

#### Announcements

- Build organization-owned announcements.
- Allow `SUPER_ADMIN` to create and manage announcements across organizations.
- Allow `USG_OFFICER` to create and manage USG announcements.
- Allow `ORG_OFFICER` to create and manage announcements for its assigned organization.
- Allow student-visible announcement records to be prepared for mobile integration later.

#### Officer Notification Foundation

- Prepare notification records for officer-facing actions.
- Include notification support for:
  - announcements
  - schedule conflicts
  - pending approvals
  - payment submissions
  - report or event document updates

### Access and Workflow Rules

- `SUPER_ADMIN` may view all dashboard data and filter by organization.
- `USG_OFFICER` may view only USG dashboard data, except shared calendar schedule-only visibility.
- `ORG_OFFICER` may view only its organization dashboard data, except shared calendar schedule-only visibility.
- Shared calendar visibility must not bypass organization access rules for full event or meeting details.
- Announcements are organization-owned and must follow organization visibility rules.
- Students must not create official announcements.

### Deliverables

- Working Officer / Super Admin Web Platform foundation.
- Dashboard connected to backend data.
- Super Admin organization filtering foundation.
- Officer dashboard with organization-scoped data.
- Dashboard calendar with schedule-only cross-organization visibility.
- Schedule conflict checking for events and meetings.
- Organization-owned announcements.
- Officer notification foundation.

---

## Phase 3 – Event Proposal and Event Document Workflow

### Purpose

Build the Events module as an event proposal, document preparation, signatory review, approval, publication, and export workflow.

This phase also builds the reusable Signatory registration and signature system because event documents require signatories.

### Build Scope

- Events module
- Event proposal workflow
- Event document templates
- SARF / Student Activity Request Form
- Letter
- Budget Proposal
- Partial Program of Activities
- Controlled editable fields
- Controlled table rows
- Signatory registration
- Signatory approval/rejection
- Signature drawing/upload
- Signatory assignment
- For Approval / For Disapproval workflow
- Event approval and publication
- Event document DOCX/PDF export
- Event document export history

### Development Tasks

#### Event Proposal Records

- Create event proposal data models.
- Attach event proposals to an organization.
- Support event status flow:

```text
Draft → For Approval → Approved → Published / Active
```

- Store event schedule fields needed for calendar and conflict checking:
  - title
  - organization
  - date/time
  - venue
  - schedule visibility setting
  - status
- Link approved events to attendance sessions later in Phase 4.

#### Event Document Templates

- Build fixed-template support for event documents:
  - SARF / Student Activity Request Form
  - Letter
  - Budget Proposal
  - Partial Program of Activities
- Allow users to fill only controlled editable fields.
- Prevent free-form editing of template layout and structure.
- Add controlled table-row support where needed:
  - budget items
  - program activities
  - schedule rows
  - expense rows
- Keep basic controlled rows/fields in this phase.
- Leave advanced dynamic field builder behavior for Phase 10.

#### Signatory Registration and Signature Setup

- Build Signatory registration.
- Collect signatory registration fields:
  - firstname
  - middlename
  - lastname
  - email
  - username
  - password
  - position
  - signature
- Allow signature creation by:
  - drawing the signature directly inside the system
  - uploading a signature image
- Store signatures with transparent background support when possible.
- Apply signatory account status flow:

```text
Pending → Approved → Rejected
```

- Allow only `SUPER_ADMIN` and `USG_OFFICER` to approve or reject signatory registrations.
- Require rejection reason when a signatory registration is rejected.
- Prevent pending or rejected signatory accounts from accessing assigned event documents.

#### Signatory Assignment for Event Documents

- Allow officers to assign signatories per event or per event document, depending on the template.
- Prevent signatories from assigning themselves.
- Notify signatories when an event document is assigned.
- Allow approved signatories to review assigned event documents only.

#### Signatory Action Workflow

- Allow assigned signatories to mark event documents as:

```text
For Approval
For Disapproval
```

- Require `Reason/s for Disapproval` when `For Disapproval` is selected.
- Keep event proposals under `For Approval` when a specific signatory marks a document as `For Disapproval`.
- Allow officers to correct and resubmit disapproved event documents.
- Track signatory actions for traceability.

#### Event Approval and Publication

- Require all required event documents to be approved before the event can be approved.
- Allow authorized officers or `SUPER_ADMIN` to publish or activate approved events.
- Ensure published or active events can be visible to covered students later in the mobile app.

#### Event Document Export

- Allow finalized event documents to be exported as DOCX or PDF after required signatories are completed.
- Include in exported files:
  - filled-in template fields
  - completed signatories or signatures
  - approval/disapproval records where applicable
- Keep export history:
  - export format
  - exported by account
  - manually entered officer name when applicable
  - export date/time
  - related event/document reference

### Access and Workflow Rules

- `SUPER_ADMIN` may manage event proposals and event documents across organizations.
- `USG_OFFICER` may manage only USG event proposals and event documents.
- `ORG_OFFICER` may manage only event proposals and event documents owned by its assigned organization.
- `SIGNATORY` may access only assigned event documents after account approval.
- `SIGNATORY` may not manage event records, edit document contents, or export documents unless a signed-copy viewing rule is later added.
- Event documents and reports must share the same controlled-template and signatory workflow principles.
- Event document export must not turn the system into an unrestricted word processor.

### Deliverables

- Event proposal workflow.
- Fixed event document templates.
- Controlled editable fields and controlled table rows.
- Signatory registration, approval, and signature setup.
- Signatory assignment and approval/disapproval workflow for event documents.
- Event approval and publication flow.
- DOCX/PDF export for finalized event documents.
- Event document export history.

---

## Phase 4 – Attendance, Face Verification, Violations, and Accountability

### Purpose

Build the attendance and accountability system using authenticated student access, school ID QR scanning, geolocation validation, facial recognition, sign-in/sign-out checkpoints, and officer-confirmed violations.

This phase creates official violations, but payment obligations connected to violations are handled in Phase 5.

### Build Scope

- Attendance sessions
- Attendance records
- Event/meeting-linked attendance
- School ID QR scanning
- Geolocation validation
- Facial recognition
- Face registration support
- Face embedding storage
- Sign-in and sign-out checkpoint records
- Attendance status computation
- Community service hour configuration
- Money equivalent configuration
- Pending violation detection
- Officer violation confirmation

### Development Tasks

#### Attendance Session Setup

- Create attendance session data models.
- Link attendance sessions to events or meetings.
- Attach attendance sessions to an organization.
- Allow authorized officers or `SUPER_ADMIN` to set:
  - open time
  - close time
  - venue/location boundary
  - sign-in checkpoint rules
  - sign-out checkpoint rules
  - community service hours for missing sign-in
  - community service hours for missing sign-out
  - money equivalent for missing sign-in
  - money equivalent for missing sign-out
- Allow values for missing sign-in and missing sign-out to be the same or different.

#### School ID QR Validation

- Implement school ID QR scanning through the student mobile camera.
- Extract or match the student identity value from the existing school ID QR format.
- Validate that the scanned QR identity matches the logged-in student account.
- Reject attendance attempts when the scanned QR belongs to another student.

#### Geolocation Validation

- Capture student geolocation during sign-in and sign-out.
- Validate whether the student is within the allowed event or meeting location boundary.
- Reject attempts outside the allowed location.

#### Facial Recognition

- Implement face registration during student account registration.
- Store face embeddings only.
- Do not store raw face images as permanent records.
- Require facial recognition during both sign-in and sign-out.
- Reject attendance validation when face verification fails.

#### Sign-In and Sign-Out Checkpoints

- Treat sign-in and sign-out as separate attendance checkpoints.
- Allow a valid sign-out to be recorded even if sign-in was missed.
- Apply this attendance status rule:

```text
Valid sign-in + valid sign-out = PRESENT
Valid sign-in + missing sign-out = INCOMPLETE
Missing sign-in + valid sign-out = INCOMPLETE
Missing sign-in + missing sign-out = ABSENT
```

- Do not implement a `LATE` status in this roadmap.

#### Violation Detection

- Detect missing attendance checkpoints.
- Prepare pending violations using this rule:

```text
Missing sign-in → Pending sign-in violation
Missing sign-out → Pending sign-out violation
Missing both → Two pending violations
```

- Store community service hours and money equivalent values from the attendance session setup.
- Allow students to view:
  - missed checkpoint
  - equivalent community service hours
  - money equivalent when applicable
  - pending or official violation status

#### Violation Confirmation

- Allow authorized officers to review pending violations.
- Convert pending violations into official violations only after officer confirmation.
- Do not create payment obligations in this phase; payment connection is handled in Phase 5.

### Access and Workflow Rules

- `SUPER_ADMIN` may manage attendance sessions and records across organizations.
- `USG_OFFICER` may manage only USG attendance sessions and records.
- `ORG_OFFICER` may manage only attendance sessions and records owned by its assigned organization.
- `STUDENT` may submit attendance only for sessions visible to them.
- `STUDENT` may view only their own attendance and violation records.
- `SIGNATORY` has no access to attendance workflows.
- Attendance validation must be enforced server-side.
- Missing checkpoints must remain pending until officer confirmation.

### Deliverables

- Organization-owned attendance sessions.
- Student attendance validation using school ID QR, geolocation, and facial recognition.
- Separate sign-in and sign-out checkpoint tracking.
- `PRESENT`, `INCOMPLETE`, and `ABSENT` status computation.
- Configurable community service hours and money equivalents.
- Pending violation detection.
- Officer-confirmed official violations.

---

## Phase 5 – Payment and USG Lost and Found Services

### Purpose

Build payment tracking, receipt verification, manual payment recording, violation-generated payment obligations, global payment QR management, and the USG-only Lost and Found service.

### Build Scope

- Global payment QR
- Payment QR upload history
- Payment obligations
- System-assisted payment tracking
- Receipt screenshot upload
- Manual payment recording
- Officer payment verification/rejection
- Violation-generated payment obligations
- USG Lost and Found

### Development Tasks

#### Global Payment QR

- Allow only `SUPER_ADMIN` to upload or replace the global payment QR code.
- Store active payment QR metadata.
- Keep history of old payment QR uploads:
  - uploaded by
  - upload date/time
  - active/inactive status
  - file/reference metadata

#### Payment Obligations

- Create payment obligation records.
- Attach payment records to the correct organization.
- Allow authorized officers to create or manage payment obligations within their allowed organization scope.
- Generate payment obligations from confirmed violations using the money equivalent configured in Phase 4 attendance sessions.

#### System-Assisted Payment Tracking

- Show the global payment QR code when a student needs to pay.
- Allow students to upload receipt screenshots after paying externally.
- Support payment method value:

```text
QR_RECEIPT_UPLOAD
```

- Apply receipt upload status flow:

```text
Unpaid → Submitted → Verified / Rejected
```

- Require officer review before verification or rejection.
- Require rejection reason or notes where appropriate.

#### Manual Payment Recording

- Allow students to pay manually through the accepted organization process.
- Allow authorized officers to record and verify manual payment.
- Support payment method value:

```text
MANUAL_PAYMENT
```

- Allow manual payment status flow:

```text
Unpaid → Verified
```

- Prevent students from marking themselves as paid or verified.

#### Other External Payment Methods

- Support method value:

```text
OTHER_EXTERNAL_PAYMENT
```

- Keep the same verification principle: students may submit proof, but officers verify.

#### Payment Verification

- Allow officers to verify valid payment submissions.
- Allow officers to reject invalid, unclear, duplicate, or mismatched receipts.
- Require real officer name entry for verification or rejection when using a shared officer account.
- Create student notifications for payment verification results.

#### USG Lost and Found

- Build Lost and Found as a USG-managed service.
- Allow only `USG_OFFICER` and `SUPER_ADMIN` to manage found item records.
- Support actions:
  - post found item
  - update found item details
  - mark found item as claimed
- Apply status flow:

```text
Found → Claimed
```

- Allow all students to view USG-posted found items.
- Do not allow students to submit lost-item reports or claim requests inside the system.
- Make it clear that students must personally go to the responsible USG office or person to claim an item.

### Access and Workflow Rules

- `SUPER_ADMIN` may view and manage payment records across organizations.
- `SUPER_ADMIN` is the only role that can upload or replace the global payment QR.
- `USG_OFFICER` may verify only USG-owned payment records.
- `ORG_OFFICER` may verify only payment records owned by its assigned organization.
- Payment records remain organization-owned even if one global QR code is used.
- `STUDENT` may view only their own payment records and submit proof when required.
- `STUDENT` must not verify their own payments.
- Lost and Found is visible to all students but managed only by `USG_OFFICER` and `SUPER_ADMIN`.
- `ORG_OFFICER` must not access or manage Lost and Found.
- `SIGNATORY` has no access to Payment or Lost and Found workflows.

### Deliverables

- Global payment QR management and upload history.
- Payment obligations and organization-owned payment records.
- Receipt upload and verification workflow.
- Manual payment recording workflow.
- Payment obligations generated from confirmed violations.
- Student payment status visibility.
- USG-only Lost and Found module.

---

## Phase 6 – Reports, Templates, Signatories, and Export

### Purpose

Build the official reports system using controlled templates, signatory workflows, locking/finalization, DOCX/PDF export, and export history.

This phase reuses the Signatory registration, signature, and approval foundation built in Phase 3.

### Build Scope

- Reports module
- AWFP
- Financial Report
- Auditor’s Report
- Accomplishment Report
- Fixed report templates
- Controlled editable fields
- Basic controlled rows/fields
- Signatory assignment for reports
- For Approval / For Disapproval workflow
- Report locking and finalization
- DOCX/PDF export
- Export history

### Development Tasks

#### Report Records

- Create report models.
- Attach reports to the correct organization.
- Support report types:
  - Annual Work and Financial Plan (AWFP)
  - Financial Report
  - Auditor’s Report
  - Accomplishment Report
- Do not include President’s Report unless formally added later.
- Do not include Resolution Management unless formally added later.
- Do not include Accomplishment Report analytics.

#### Report Templates

- Implement fixed report templates.
- Allow users to fill only controlled editable fields.
- Prevent unrestricted document editing.
- Support controlled table rows where the original report format requires structured rows.
- Keep basic controlled rows/fields in this phase.
- Leave advanced dynamic field builder behavior for Phase 10.

#### Report Preparation

- Allow authorized officers to create reports.
- Allow report ownership assignment to the correct organization.
- Allow manually typed officer names where the original format requires:
  - Prepared by
  - Checked by
  - Approved by
- Allow signatory users to be assigned when preparing reports.

#### Report Signatory Workflow

- Reuse signatory account approval and signature logic from Phase 3.
- Allow approved signatories to access assigned reports only.
- Allow assigned signatories to mark reports as:

```text
For Approval
For Disapproval
```

- Require `Reason/s for Disapproval` when a report is marked `For Disapproval`.
- Track signatory actions for traceability.
- Include approved signatory signatures in exported DOCX/PDF files when required.

#### Report Locking and Finalization

- Allow reports to be locked or finalized.
- Prevent normal editing after locking.
- Allow authorized officers or `SUPER_ADMIN` to unlock directly.
- Do not require an unlock reason unless added later.
- Require completed signatories before final export.

#### Report Export

- Export finalized reports as DOCX or PDF after required signatories are completed.
- Include:
  - filled-in template fields
  - completed signatories or signatures
  - approval/disapproval records where applicable
- Keep report export history:
  - export format
  - exported by account
  - manually entered officer name when applicable
  - export date/time
  - related report reference
- Preserve controlled-template structure in exported files.

### Access and Workflow Rules

- `SUPER_ADMIN` may manage report records across organizations but must not perform signatory approval unless assigned through the signatory workflow.
- `USG_OFFICER` may prepare, manage, and export only USG-owned reports.
- `ORG_OFFICER` may prepare, manage, and export only reports owned by its assigned organization.
- `SIGNATORY` may access only assigned reports after account approval.
- `SIGNATORY` must not create reports, edit report contents, verify payments, manage attendance, or access unrelated reports.
- Reports and event documents must follow the same controlled-template, signatory, finalization, export, and export-history principles.

### Deliverables

- Reports module with AWFP, Financial Report, Auditor’s Report, and Accomplishment Report.
- Fixed report templates with controlled fields.
- Report signatory assignment and approval/disapproval workflow.
- Report locking and finalization.
- DOCX/PDF export for finalized reports.
- Report export history.

---

## Phase 7 – Chats / Messaging, Notifications, and Student Records

### Purpose

Build the communication and notification layer that connects students, officer accounts, and `SUPER_ADMIN`, and provide consolidated student-facing record visibility.

This phase builds simple near-real-time chat using polling or timed refresh. Full real-time chat upgrade is reserved for Phase 10.

### Build Scope

- Chats / Messaging
- Simple near-real-time chat behavior
- Super Admin chat moderation
- Basic notifications
- Student-facing record views
- Officer-facing notification records
- Signatory notification records

### Development Tasks

#### Chats / Messaging

- Build one global chat room for:
  - all `STUDENT` users
  - `USG_OFFICER`
  - `ORG_OFFICER` accounts
  - `SUPER_ADMIN`
- Exclude `SIGNATORY` users from chat access.
- Exclude outside instructors, staff, or administrators unless they are official Campus Connect users with an allowed role.
- Support simple near-real-time behavior using polling or timed refresh.
- Allow participants to send and reply to messages.
- Display sender labels clearly:
  - `Student`
  - `USG Officer`
  - `SITE Officer`
  - `PAFE Officer`
  - `AFPROTECH Officer`
  - `Super Admin`
- Do not require manually typed real officer names for every chat message.
- Allow `SUPER_ADMIN` to moderate chat messages.
- Support moderation actions such as hiding or deleting messages where implemented.

#### Notifications

- Build notification records for:
  - officer web platform
  - student mobile application
  - signatory web platform
- Support notifications for:
  - student account approval/rejection
  - signatory account approval/rejection
  - new announcements
  - event or meeting updates
  - attendance records
  - pending or confirmed violations
  - payment submission or verification results
  - event document/report assignment
  - signatory approval/disapproval updates
  - finalized export availability where applicable

#### Student Records

- Build consolidated student-facing record views.
- Allow students to view:
  - profile details
  - attendance records
  - violation records
  - payment records
  - notifications
  - USG + assigned organization events and meetings
  - USG Lost and Found records
- Ensure students only access their own personal records.

### Access and Workflow Rules

- Chats / Messaging is system-wide and is an exception to normal organization-scoped visibility.
- `SUPER_ADMIN` moderates chat.
- Normal officer accounts may send/reply but must not have full moderation authority.
- `SIGNATORY` users must not access chat.
- Notification records must respect access scope:
  - officers see organization-relevant notifications
  - students see their own and visible organization notifications
  - signatories see assigned event document/report notifications only
- Student records must remain personal and must not expose another student’s data.

### Deliverables

- Global near-real-time Chats / Messaging.
- Super Admin chat moderation.
- Basic notifications for officer web, student mobile, and signatory web.
- Consolidated student-facing record views.
- Access-safe student record visibility.

---

## Phase 8 – Student Mobile Integration

### Purpose

Build and connect the Student Mobile Application to the backend workflows created in earlier phases.

This phase focuses on student-facing usability, mobile attendance participation, student records, payment proof submission, and mobile visibility of USG + assigned organization content.

### Build Scope

- Student mobile authentication
- Student registration
- Face registration
- Student profile
- Mobile calendar
- Events and meetings view
- Announcements view
- Attendance participation
- Violation records
- Payment records
- Receipt upload
- USG Lost and Found view
- Notifications
- Student record dashboard

### Development Tasks

#### Mobile Authentication and Registration

- Build student registration screens.
- Capture required student identity and profile data.
- Support school ID QR reference or extracted identity value.
- Support face registration for attendance verification.
- Show account status:
  - Pending
  - Approved
  - Rejected
- Show rejection reason when applicable.
- Build login, logout, token storage, and token refresh behavior.

#### Mobile Calendar

- Build student mobile calendar.
- Show only approved or published events and meetings from:
  - USG
  - student’s assigned course/department organization
- Allow selecting a calendar item to open event or meeting details.

#### Events, Meetings, and Announcements

- Show published or active events from USG and assigned organization.
- Show visible meetings when applicable.
- Show announcements from USG and assigned organization.
- Display organization labels on student-facing records.

#### Attendance Participation

- Allow students to select active visible attendance sessions.
- Support mobile camera scanning of the physical school ID QR.
- Capture geolocation.
- Run facial recognition validation.
- Support sign-in and sign-out.
- Show attendance result:
  - `PRESENT`
  - `INCOMPLETE`
  - `ABSENT`
- Show missed checkpoint information and pending violation details where applicable.

#### Payments

- Show payment obligations.
- Show payment method and status.
- Show global payment QR when payment is required.
- Allow receipt screenshot upload for system-assisted payment.
- Show manual payment records entered by officers.
- Show verification or rejection results.

#### Lost and Found

- Show USG-posted found item records.
- Show found item details and claimed status.
- Do not allow students to submit lost-item reports or claim requests in the app.

#### Notifications and Student Records

- Show basic notifications.
- Show consolidated student records:
  - profile
  - attendance
  - violations
  - payments
  - notifications

### Access and Workflow Rules

- Student mobile access must be limited to approved student accounts for protected features.
- Student-visible records must include USG records plus records from the student’s assigned course/department organization.
- Students must not manually switch organization context.
- Students must not verify their own payments.
- Students must not access officer, Super Admin, or Signatory web features.
- Mobile UI must not be trusted as the final authority for access control.

### Deliverables

- Student Mobile Application connected to backend APIs.
- Student registration and login flow.
- Mobile calendar, events, meetings, announcements, attendance, payments, Lost and Found, notifications, and student records.
- Mobile attendance flow using school ID QR, geolocation, and facial recognition.
- Student-facing visibility aligned with organization rules.

---

## Phase 9 – Testing, Hardening, and Deployment Preparation

### Purpose

Validate the complete Campus Connect system across backend, officer web, signatory web, and student mobile clients before deployment.

This phase focuses on correctness, security, reliability, performance, and deployment readiness.

### Build Scope

- Security testing
- Role and permission testing
- Organization visibility testing
- Attendance validation testing
- Face verification testing
- Signatory workflow testing
- Event document and report export testing
- Payment workflow testing
- Mobile integration testing
- Deployment preparation

### Development Tasks

#### Security and Access Testing

- Test authentication flows.
- Test token handling and expiration.
- Test role restrictions for:
  - `SUPER_ADMIN`
  - `USG_OFFICER`
  - `ORG_OFFICER`
  - `STUDENT`
  - `SIGNATORY`
- Test that hidden UI controls are not the only protection.
- Test backend authorization for every protected endpoint.

#### Organization Visibility Testing

- Verify `USG_OFFICER` cannot access SITE, PAFE, or AFPROTECH records.
- Verify `ORG_OFFICER` accounts cannot access records outside their assigned organization.
- Verify `SUPER_ADMIN` can access records across organizations and filter by organization.
- Verify students see USG + assigned organization records only.
- Verify Chats / Messaging remains a controlled system-wide exception.

#### Attendance and Face Verification Testing

- Test school ID QR matching.
- Test geolocation validation.
- Test facial recognition validation.
- Test sign-in and sign-out checkpoint behavior.
- Test `PRESENT`, `INCOMPLETE`, and `ABSENT` computation.
- Test missing checkpoint violation creation.
- Test duplicate attendance prevention.
- Test time window enforcement.

#### Signatory Workflow Testing

- Test signatory registration.
- Test signatory approval and rejection.
- Test signature drawing and upload.
- Test assignment-scoped document access.
- Test `For Approval` and `For Disapproval`.
- Test required `Reason/s for Disapproval`.
- Test that pending or rejected signatories cannot access assigned documents.

#### Event Document and Report Export Testing

- Test fixed template field preservation.
- Test controlled table rows.
- Test DOCX export.
- Test PDF export.
- Test completed signature inclusion.
- Test export history.
- Test that exports cannot be generated before required signatories are completed.

#### Payment Testing

- Test global payment QR access.
- Test receipt upload.
- Test manual payment recording.
- Test payment verification and rejection.
- Test violation-generated payment obligations.
- Test that students cannot verify their own payments.
- Test organization ownership of payment records.

#### Web, Mobile, and Backend Integration Testing

- Test Officer / Super Admin Web Platform workflows.
- Test Signatory Web Platform workflows.
- Test Student Mobile Application workflows.
- Test notification behavior.
- Test chat behavior.
- Test calendar and schedule conflict checking.
- Test end-to-end flows across web, mobile, API, and database layers.

#### Deployment Preparation

- Review production environment settings.
- Review database migration readiness.
- Review file storage for signatures, receipts, and exports.
- Review logging and auditability.
- Review backup and restore strategy.
- Review deployment checklist.
- Prepare rollback plan.
- Prepare final user acceptance testing checklist.

### Access and Workflow Rules

- Deployment must not proceed until role access, organization visibility, and assignment-scoped access pass testing.
- Export features must preserve official document/report formats.
- Payment features must remain tracking and verification workflows, not internal payment processing.
- Student mobile workflows must be tested on real devices where possible.
- Face verification must be tested with privacy and security considerations.

### Deliverables

- Tested backend, web, signatory, and mobile workflows.
- Verified access control and organization visibility.
- Verified attendance and payment workflows.
- Verified event document/report signatory and export workflows.
- Deployment-ready configuration.
- Deployment checklist and rollback plan.

---

## Phase 10 – Future Enhancements

### Purpose

Document advanced features that may be added after the first complete Campus Connect build is stable.

These items must not block the first complete system implementation unless formally moved into an earlier phase.

### Build Scope

- Face liveness detection / anti-spoofing
- Real-time chat upgrade
- Advanced dynamic fields
- Additional enhancements after panel or adviser feedback

### Development Tasks

#### Face Liveness Detection / Anti-Spoofing

- Add liveness detection to strengthen facial recognition.
- Detect possible spoofing attempts such as printed photos, screens, or static images.
- Add challenge-based face verification if needed.
- Keep face embedding privacy rules.
- Avoid storing raw face images as permanent records unless formally approved.

#### Real-Time Chat Upgrade

- Upgrade simple near-real-time Chats / Messaging to full real-time messaging.
- Consider WebSocket or another real-time communication approach.
- Improve message delivery state.
- Improve moderation tooling.
- Preserve existing allowed-role access rules.

#### Advanced Dynamic Fields

- Add a more flexible controlled dynamic field builder for templates.
- Keep fixed-template boundaries.
- Prevent unrestricted document editing.
- Ensure dynamic fields remain structured and validated.
- Apply only to event documents or reports where the original format requires it.

#### Feedback-Based Enhancements

- Add more enhancement items only after panel, adviser, or stakeholder feedback.
- Document each added enhancement clearly before implementation.
- Avoid expanding the current build without updating the project overview and roadmap.

### Access and Workflow Rules

- Enhancements must preserve the five-role access model.
- Enhancements must preserve organization-scoped ownership unless formally changed.
- Enhancements must not weaken backend access enforcement.
- Enhancements must not turn reports or event documents into unrestricted word processors.
- Enhancements must be documented before development begins.

### Deliverables

- A controlled enhancement backlog.
- Face liveness / anti-spoofing plan or implementation.
- Full real-time chat upgrade plan or implementation.
- Advanced dynamic field plan or implementation.
- Updated roadmap items after panel or adviser feedback.

---

## Roadmap Summary

The revised Campus Connect development order is:

1. **Foundation, Roles, and Organization Model**
2. **Officer / Super Admin Web Platform Core**
3. **Event Proposal and Event Document Workflow**
4. **Attendance, Face Verification, Violations, and Accountability**
5. **Payment and USG Lost and Found Services**
6. **Reports, Templates, Signatories, and Export**
7. **Chats / Messaging, Notifications, and Student Records**
8. **Student Mobile Integration**
9. **Testing, Hardening, and Deployment Preparation**
10. **Future Enhancements**

This roadmap builds the system from the backend and access-control foundation first, then proceeds through officer workflows, event documents, attendance, services, reports, communication, student mobile integration, testing, and controlled enhancements.
