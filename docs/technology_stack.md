# Technology Stack

---

## 1. Technology Stack Overview

Campus Connect uses a **web + mobile + API-first architecture** supported by a centralized backend, a relational database, and a separate ML/AI service for facial recognition.

The stack must support the latest Campus Connect system direction:

- organization-scoped records for USG, SITE, PAFE, and AFPROTECH
- five application roles:
  - `SUPER_ADMIN`
  - `USG_OFFICER`
  - `ORG_OFFICER`
  - `STUDENT`
  - `SIGNATORY`
- Officer / Super Admin Web Platform
- Signatory Web Platform
- Student Mobile Application
- centralized backend API enforcement
- preloaded student master record matching for student mobile registration
- PostgreSQL-backed data storage
- PostGIS-backed geolocation validation
- facial recognition through a separate ML/AI service
- DOCX/PDF export for finalized event documents and reports
- database-backed in-app notifications and FCM-based push notification delivery
- Cloudinary-backed image storage for Lost and Found item images, with optional face reference image storage only if formally approved
- local file/media storage for other files first, with cloud storage as a deployment option

The technology stack is divided into the following layers:

- Backend API Layer
- Web Frontend Layer
- Mobile Application Layer
- Database and Geospatial Layer
- ML/AI Face Recognition Layer
- File, Media, and Export Layer
- Notifications Layer
- Deployment and Infrastructure Layer
- Development Tools and Environment Support

The frontend and mobile app guide the user experience, but the backend remains the final authority for authentication, authorization, organization ownership, workflow validation, signatory assignment, attendance validation, payment verification, and document/report export rules.

---

## 2. Backend API Stack

### 2.1 Core Backend Framework

**Framework:** Django  
**API Layer:** Django REST Framework  
**Language:** Python

Django is the primary backend framework for Campus Connect.

The backend is responsible for:

- user authentication
- role-based access enforcement
- organization ownership enforcement
- student master record matching and student account activation rules
- signatory registration and approval rules
- event document workflow rules
- report template workflow rules
- attendance validation rules
- payment verification rules
- violation confirmation rules
- notification record creation
- media/file reference handling
- export history tracking
- centralized API delivery for web and mobile clients

Django is used because it provides:

- strong project structure
- modular app organization
- ORM support
- admin support for development and maintenance
- compatibility with Django REST Framework
- secure authentication foundations
- reliable integration with PostgreSQL

### 2.2 API Framework

**API Framework:** Django REST Framework (DRF)

DRF is used to expose protected REST API endpoints for:

- Officer / Super Admin Web Platform requests
- Signatory Web Platform requests
- Student Mobile Application requests
- authentication and account workflows
- student master record matching and account activation workflows
- organization-scoped record retrieval
- workflow submissions
- file upload handling
- notification retrieval
- payment verification
- attendance submission
- document/report preparation and export actions

DRF must support the project’s API-first architecture.

Backend APIs must enforce:

- role permissions
- organization ownership
- student visibility
- signatory assignment
- workflow status transitions
- secure file access
- attendance validation
- payment verification
- document/report locking and export rules

The web frontend and mobile application must not rely on hidden buttons or client-side checks as the final security layer.

### 2.3 Authentication and Authorization

**Authentication Approach:** Django Authentication + JWT  
**JWT Package:** `djangorestframework-simplejwt`

Authentication should use:

- custom user model
- password-based login
- JWT access tokens
- JWT refresh tokens
- Bearer token authorization for protected API endpoints

JWT is used so the web and mobile clients can authenticate consistently through the same backend.

The user model and authorization layer must support the following technical roles:

```text
SUPER_ADMIN
USG_OFFICER
ORG_OFFICER
STUDENT
SIGNATORY
```

Authorization must also consider:

- organization ownership
- student course/department visibility
- assigned signatory access
- account approval status
- workflow status
- record ownership

### 2.4 Environment Configuration

**Environment Configuration:** `python-dotenv`

Environment-based configuration should be used to avoid hardcoding:

- secret keys
- debug settings
- allowed hosts
- database credentials
- media storage paths
- Cloudinary configuration values
- CORS settings
- FCM configuration values
- ML/AI service URL
- log level settings
- environment-specific runtime behavior

The Django backend should use a split settings structure such as:

```text
base.py
dev.py
prod.py
```

This supports cleaner local development and production deployment setup.

### 2.5 Backend Database Driver

**PostgreSQL Driver:** `psycopg2-binary` or a production-appropriate PostgreSQL driver

The PostgreSQL driver enables Django to communicate with the PostgreSQL database.

The exact package may be adjusted depending on the deployment environment, but the main database remains PostgreSQL.

---

## 3. Web Frontend Stack

### 3.1 Core Web Technologies

**Languages / Technologies:**

- HTML5
- CSS3
- JavaScript
- Bootstrap

The web frontend stack is used for:

- Officer / Super Admin Web Platform
- Signatory Web Platform

The web frontend should remain API-driven. It should consume Django REST API endpoints instead of treating the frontend as the source of system rules.

### 3.2 Officer / Super Admin Web Platform

The Officer / Super Admin Web Platform uses the same web UI foundation for:

- `SUPER_ADMIN`
- `USG_OFFICER`
- `ORG_OFFICER`

The UI must show different controls depending on role and organization access.

The web stack must support:

- secure login
- JWT token handling
- dashboard data rendering
- organization filtering for `SUPER_ADMIN`
- officer organization-scoped views
- dashboard calendar and conflict visibility
- events and meeting management
- announcements
- attendance session management
- payment verification
- USG Lost and Found management
- report and event document preparation
- DOCX/PDF export controls
- global payment QR upload controls for `SUPER_ADMIN` only
- global chat/messaging access where allowed

### 3.3 Signatory Web Platform

The Signatory Web Platform uses the same general web technologies, but it must be a separate simplified interface.

It is used by `SIGNATORY` users only after account approval.

The Signatory Web Platform must support:

- signatory login
- assigned event document and report listing
- document/report review
- marking assigned items as **For Approval**
- marking assigned items as **For Disapproval**
- entering **Reason/s for Disapproval**
- drawing or uploading a signature during registration or profile setup, where allowed
- viewing assigned workflow updates

The Signatory Web Platform must not expose officer dashboard features, payment verification, attendance management, student management, organization settings, Lost and Found management, or Chats / Messaging.

### 3.4 UI Framework

**UI Framework:** Bootstrap

Bootstrap is used to support:

- faster UI development
- responsive layouts
- consistent form styling
- dashboard pages
- officer management screens
- signatory review screens
- modal dialogs
- status badges
- form validation feedback

The system does not require a JavaScript frontend framework such as React for the current stack.

### 3.5 Web-to-Backend Communication

The web frontend communicates with the backend using:

- REST API requests
- JSON payloads
- JWT Bearer token authentication
- secure file upload requests where needed

Shared frontend utilities may be used for:

- API base URL configuration
- token storage
- authenticated request headers
- logout handling
- common error handling
- reusable form submission behavior

---

## 4. Mobile Application Stack

### 4.1 Mobile Framework

**Framework:** Flutter  
**Language:** Dart

Flutter is the intended framework for the Student Mobile Application.

The Flutter mobile client may be maintained in a separate repository from the Django backend and web frontend. This document describes the system-wide mobile stack and integration direction, not only the contents of one repository.

The Student Mobile Application is responsible for:

- student registration through preloaded student master record matching
- student login
- profile viewing
- viewing USG and assigned organization records
- viewing events and meetings
- viewing the student calendar
- viewing announcements
- participating in attendance
- scanning the physical school ID QR during registration and attendance
- submitting registration details for matching against preloaded student master records
- capturing face data for registration and attendance validation
- submitting geolocation data for attendance validation
- viewing attendance status
- viewing violations and equivalent community service/payment details
- viewing payment records
- uploading receipt screenshots
- viewing USG Lost and Found records
- viewing notifications
- receiving push notifications where enabled

### 4.2 Mobile Capabilities

The Flutter mobile app must support the following device capabilities:

- camera access for school ID QR scanning
- camera access for face capture
- geolocation access for attendance validation
- secure token storage
- image/file upload for payment receipts
- push notification token registration
- network status handling
- retry-safe submission behavior

Possible Flutter capability areas include:

- QR scanning plugin
- geolocation plugin
- camera plugin
- secure storage plugin
- image/file picker or upload support
- Firebase Cloud Messaging integration for push notifications

The exact Flutter packages may be selected during implementation, but the required capabilities must remain aligned with the system workflows.

### 4.3 Mobile-to-Backend Communication

**Communication Style:** REST API using JSON  
**Authentication:** JWT Bearer Token

The mobile app communicates with the same centralized Django backend used by the web interfaces.

This supports:

- consistent authentication
- backend-enforced permissions
- organization visibility rules
- attendance validation
- payment verification
- student record retrieval
- notification delivery
- single-source-of-truth data handling

The mobile app must not decide final attendance status, payment status, violation status, or record visibility without backend confirmation.

---

## 5. Database and Geospatial Stack

### 5.1 Primary Database

**DBMS:** PostgreSQL

PostgreSQL is the primary database system for Campus Connect.

It is used because it supports:

- strong relational integrity
- reliable transactions
- structured schema management
- indexing
- JSON-compatible fields where needed
- production-grade reliability
- compatibility with Django ORM

The database must support records such as:

- accounts
- roles
- organizations
- preloaded student master records
- linked student user accounts
- student profiles
- signatory profiles
- signatures
- events
- event documents
- meetings
- announcements
- chat messages
- attendance sessions
- attendance records
- violations
- payment records
- payment QR history
- Lost and Found records
- reports
- export history
- notifications
- file/media references

Student master records are the official preloaded student data used to validate student mobile registration. A student user account should be linked to exactly one student master record after successful identity matching. The backend must prevent duplicate account claims for the same student master record.

### 5.2 Geospatial Support

**Extension / GIS Support:** PostGIS

PostGIS supports location-aware attendance validation.

It may be used for:

- storing attendance session coordinates
- storing allowed attendance areas
- validating student-submitted coordinates
- center-radius validation
- polygon-based geospatial validation if needed

Attendance geolocation validation should be enforced by the backend.

The mobile app may capture and submit location data, but the backend must decide whether the submitted location is valid.

---

## 6. ML/AI Face Recognition Stack

### 6.1 Service Architecture

Campus Connect requires facial recognition for attendance validation, but the exact face recognition library/model will be selected later.

Use a separate ML/AI service for facial recognition. **FastAPI is the preferred service framework**, but the exact face recognition library/model may be selected later.

High-level flow:

```text
Student mobile app captures face
→ Django backend receives attendance request
→ Django backend asks the ML/AI service to process/verify the face
→ ML/AI service returns verification result
→ Django backend records or rejects the attendance attempt
```

This separation keeps the main Django backend focused on business rules and allows the face recognition component to evolve independently.

### 6.2 Face Embedding and Face Image Storage Rule

Face recognition must primarily rely on **face embeddings** for long-term identity matching.

Raw face images should not be stored permanently by default. Temporary face images may be processed only as needed for face embedding generation or verification, subject to secure handling and deletion rules defined during implementation.

If the school, adviser, or panel formally approves storing face reference images for registration review or audit support, the image may be stored through Cloudinary with strict access control. PostgreSQL must store the official Cloudinary reference, such as the `public_id` and secure URL, together with the student face registration record.

Firebase must not be used as the official face image database. Firebase remains limited to push notification delivery through FCM.

### 6.3 ML/AI Service Responsibilities

The ML/AI service may be responsible for:

- receiving face capture input from the backend
- detecting a face in the submitted image/frame
- generating face embeddings
- comparing embeddings
- returning match / no match results
- returning validation errors when the face capture is unclear or unsuitable

The service must not override Django’s final attendance decision.

Django remains the final enforcement layer for:

- authenticated student identity
- attendance session validity
- school ID QR match
- geolocation validity
- duplicate prevention
- sign-in/sign-out checkpoint rules
- attendance status computation
- violation preparation

### 6.4 Future ML/AI Enhancement Boundary

Face liveness detection / anti-spoofing is not part of the main build.

It belongs to the Future Enhancements phase.

---

## 7. File, Media, and Export Stack

### 7.1 File and Media Storage

Campus Connect must handle several file and media types:

- global payment QR code
- student receipt screenshots
- signatory signature images
- Lost and Found item images stored through Cloudinary
- optional face reference images stored through Cloudinary only if formally approved
- generated DOCX event documents
- generated PDF event documents
- generated DOCX reports
- generated PDF reports
- optional event/report attachment files if allowed later

The system should use **Cloudinary** for Lost and Found item images. Cloudinary may also be used for face reference images only if permanent face image storage is formally approved by the school, adviser, or panel.

For other files, the system may use local server storage first for capstone/demo implementation unless a cloud storage option is specifically selected.

Possible storage options for other files may include:

- local server media storage
- AWS S3
- Google Cloud Storage
- Azure Blob Storage
- other equivalent object storage services

Cloudinary stores selected image files only. Django/PostgreSQL remains the source of truth for official records, ownership, status, visibility, and access control.

### 7.2 Cloudinary Image Storage Rules

Cloudinary may be used as the image storage service for:

- Lost and Found item images
- optional face reference images only if formally approved

For each Cloudinary-stored image, PostgreSQL should store the official record and the Cloudinary reference, such as:

- `public_id`
- secure image URL
- upload timestamp
- related record reference
- uploaded-by account where applicable
- active/inactive or replaced status where applicable

Cloudinary must not replace the main database. The backend must still enforce all access, ownership, workflow, and visibility rules.

Firebase must not be used as the official image reference database. Firebase remains limited to FCM push notification delivery.

### 7.3 Secure File Handling Rules

The backend must control file access.

The system must not expose raw server file paths directly to unauthorized users.

File handling must enforce:

- allowed file types
- file size limits
- secure upload endpoints
- Cloudinary `public_id` / secure URL reference handling where applicable
- role-based access
- organization ownership
- signatory assignment access
- student ownership for personal files
- export history tracking where applicable

### 7.4 DOCX Export Support

Finalized event documents and reports may be exported as DOCX after all required signatories are completed.

Possible replaceable DOCX tools include:

- `python-docx`
- `docxtpl`

These tools are examples only. The final library may be adjusted during implementation.

DOCX export must preserve:

- official template structure
- filled-in controlled fields
- controlled table rows
- completed signatories/signatures where required
- approval/disapproval records where applicable

### 7.5 PDF Export Support

Finalized event documents and reports may also be exported as PDF after all required signatories are completed.

Possible replaceable PDF options include:

- `WeasyPrint`
- `xhtml2pdf`
- LibreOffice-based conversion
- other Python-compatible PDF generation or conversion tools

The selected PDF approach must preserve official formatting as closely as possible.

PDF export must not turn the document/report module into a free-form word processor.

### 7.6 Export History

The backend should record export history for finalized event documents and reports.

Export history should track:

- exported file type
- exported by account
- manually entered officer name where applicable
- export date/time
- related event document or report
- file reference
- active/finalized status where applicable

---

## 8. Notifications Stack

### 8.1 In-App Notifications

Campus Connect must support database-backed in-app notifications.

In-app notification records should be stored in PostgreSQL and retrieved through the backend API.

In-app notifications may appear in:

- Officer / Super Admin Web Platform
- Signatory Web Platform
- Student Mobile Application

Notification visibility must follow:

- role permissions
- organization ownership
- student visibility rules
- signatory assignment rules
- personal record ownership

### 8.2 Push Notifications

**Mobile Push Delivery:** Firebase Cloud Messaging (FCM)

Push notifications may use Firebase Cloud Messaging for mobile notification delivery.

FCM is used only for push notification delivery. It does not replace the main backend or database.

Django and PostgreSQL remain the primary backend and data source for Campus Connect.

The backend should decide:

- who receives a notification
- what notification type is created
- whether the notification is organization-scoped, personal, or assignment-scoped
- whether a push message should be sent to the mobile device

FCM should only deliver the notification to the device after the backend determines the correct recipient.

### 8.3 Notification Examples

Notification records may support:

- student account activation or rejected registration attempt
- signatory account approval or rejection
- new announcements
- event or meeting updates
- attendance result updates
- pending or confirmed violation updates
- payment submission or verification results
- event document/report assignment
- event document/report approval or disapproval
- export-related updates where applicable

---

## 9. Chats / Messaging Stack

### 9.1 Main Build Chat Approach

The main build should use **REST API polling / timed refresh** for Chats / Messaging.

This means the client checks for new messages at a set interval.

This approach is simpler than full WebSocket-based real-time chat and fits the staged development plan.

The chat stack must support:

- one global chat room
- student messages
- officer account messages
- `SUPER_ADMIN` messages
- `SUPER_ADMIN` moderation
- sender labels such as `Student`, `USG Officer`, `SITE Officer`, `PAFE Officer`, `AFPROTECH Officer`, or `Super Admin`
- blocking `SIGNATORY` users from chat access

### 9.2 Future Real-Time Upgrade

WebSocket-based real-time chat belongs to the Future Enhancements phase.

If added later, possible tools may include:

- Django Channels
- ASGI-based WebSocket support
- Redis as a channel layer if needed

These are not required for the main build.

---

## 10. Deployment and Infrastructure Stack

### 10.1 Expected Deployment Environment

The expected deployment stack may include:

- Ubuntu server
- Django backend application
- separate FastAPI ML/AI service
- PostgreSQL database
- PostGIS extension
- local media storage
- Nginx or Apache as the web server / reverse proxy
- Gunicorn or another WSGI/ASGI-compatible application server for Django
- HTTPS/TLS configuration for secure access

The exact web server may be chosen during deployment.

The stack should mention **Nginx or Apache** without locking the project to one option too early.

### 10.2 Deployment Responsibilities

The deployment setup must support:

- serving the backend API
- serving the web frontend
- serving protected media/export files through controlled backend access
- connecting Django to PostgreSQL/PostGIS
- connecting Django to the ML/AI face recognition service
- managing environment variables securely
- logging errors and important system events
- supporting production security settings

### 10.3 Local Development Environment

The development environment may include:

- Python
- PostgreSQL
- PostGIS
- pgAdmin
- VS Code
- Android Studio
- Flutter SDK
- Dart SDK
- Git
- web browser developer tools

Exact version numbers should be recorded in setup documentation or environment setup files.

This technology stack guide defines the selected technologies and architectural direction, not the final locked version numbers for every local machine.

---

## 11. Development and Maintenance Tools

### 11.1 Version Control

**Version Control:** Git

The project should use Git for:

- source code tracking
- branching
- collaboration
- rollback safety
- version history

### 11.2 Logging

The backend should support logging for:

- authentication events
- permission failures
- attendance validation failures
- payment verification actions
- signatory actions
- export actions
- system errors
- deployment troubleshooting

Logging may include:

- console logging during development
- rotating file logs
- production log files
- future monitoring tools if needed

### 11.3 Testing Support

The stack should support backend, web, mobile, and integration testing.

Testing should cover:

- role-based access
- organization ownership
- student visibility
- signatory assignment access
- attendance validation
- face service integration
- payment verification
- document/report export
- notification delivery
- mobile API integration
- file upload handling

---

## 12. Important Non-Dependencies

The main Campus Connect build does **not** depend on the following as primary technologies:

- Supabase or Firebase as the primary backend, database, or official face image database
- internal payment gateway processing
- direct payment gateway callbacks
- face liveness detection / anti-spoofing
- advanced dynamic field builder
- WebSocket-based real-time chat
- full multi-campus deployment

Clarifications:

- Firebase Cloud Messaging may be used only for push notification delivery.
- Cloudinary may be used for selected image storage, especially Lost and Found item images and optional approved face reference images, but it does not replace Django/PostgreSQL as the source of truth.
- Payments are made externally and tracked inside Campus Connect.
- Django and PostgreSQL remain the primary backend and data source.
- FastAPI is preferred only for the separate ML/AI face recognition service.
- WebSocket chat may be added later as a future enhancement.
- Basic controlled rows/fields are allowed where templates require them, but a full advanced dynamic field builder is not part of the main build.

---

## 13. Stack Summary by Layer

### Backend API

- Django
- Django REST Framework
- Python
- Django Authentication
- SimpleJWT
- `python-dotenv`
- PostgreSQL driver such as `psycopg2-binary`

### Web Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap
- API-driven rendering
- JWT-authenticated requests

### Mobile Application

- Flutter
- Dart
- REST API communication
- JWT Bearer token authentication
- camera / QR scanning capability
- geolocation capability
- face capture capability
- secure token storage
- receipt image upload
- FCM push notification support

### Database and Geospatial

- PostgreSQL
- PostGIS

### ML/AI Face Recognition

- separate ML/AI service
- FastAPI as preferred service framework
- exact face recognition library/model to be selected later
- face embeddings only for persistent biometric data

### File, Media, and Export

- local server storage first
- cloud storage optional for deployment
- signature image storage
- payment QR and receipt storage
- DOCX export options such as `python-docx` or `docxtpl`
- PDF export options such as `WeasyPrint`, `xhtml2pdf`, or LibreOffice-based conversion
- export history records

### Notifications

- PostgreSQL-backed in-app notification records
- Firebase Cloud Messaging for mobile push delivery

### Chats / Messaging

- REST API polling / timed refresh in the main build
- WebSocket upgrade as future enhancement

### Deployment

- Ubuntu server
- Nginx or Apache
- Gunicorn or equivalent application server
- PostgreSQL/PostGIS
- Django backend
- FastAPI ML/AI service
- local media storage first
- HTTPS/TLS for secure deployment

---

## 14. Why This Stack Fits Campus Connect

This stack fits Campus Connect because it supports:

- centralized backend control
- API-first web and mobile integration
- five-role access enforcement
- organization-scoped records
- shared officer accounts
- student mobile workflows
- signatory web workflows
- facial recognition through a replaceable ML/AI service
- geolocation-aware attendance
- controlled document/report templates
- DOCX/PDF exports
- payment tracking without internal payment processing
- local-first capstone deployment
- future growth without replacing the primary backend

The stack also avoids unnecessary dependency on backend-as-a-service platforms. Django and PostgreSQL remain the official backend and data foundation, while tools such as FCM, FastAPI, Cloudinary, document export libraries, and optional cloud storage support specific system capabilities without replacing the core architecture.

---

## 15. Summary

Campus Connect uses a practical, modular, API-first technology stack.

The main stack is:

- Django + Django REST Framework for the backend API
- PostgreSQL + PostGIS for relational and geospatial data
- JWT / SimpleJWT for authenticated web and mobile access
- HTML, CSS, JavaScript, and Bootstrap for the Officer / Super Admin Web Platform and Signatory Web Platform
- Flutter + Dart for the Student Mobile Application
- a separate ML/AI service, preferably FastAPI-based, for facial recognition
- Cloudinary for Lost and Found item images and optional approved face reference images
- local server storage first for other files and exports unless another storage option is selected
- replaceable DOCX/PDF generation tools for finalized event documents and reports
- database-backed notifications with FCM for mobile push delivery
- REST API polling / timed refresh for the main chat implementation
- Nginx or Apache with an Ubuntu-based deployment environment

This stack is aligned with the latest Campus Connect overview and development direction. It supports the current system vision while keeping future enhancements, such as face liveness detection, WebSocket-based real-time chat, and advanced dynamic fields, clearly separated from the main build.
