# CARESYNC
### Because caring should be connected, simple and secure.

**AI-Powered Elderly Assistance and Family Coordination Platform**

CARESYNC is an AI-assisted platform designed to simplify everyday activities for elderly users while enabling secure coordination with family members and caregivers.

## 1. Problem Statement

Elderly individuals often manage multiple daily responsibilities, including medicines, appointments, household essentials and important documents. Families and caregivers may find it difficult to coordinate these responsibilities consistently.

## 2. Our Solution

CARESYNC aims to provide a unified, accessible platform for elderly users and their families.

### Key Features

- Medicine stock tracking and estimated refill dates.
- Medicine and appointment reminders.
- Appointment scheduling and management.
- Voice-based interaction.
- Multilingual interface: English and Hindi initially.
- Family coordination and approval requests.
- Controlled medical document access.
- AI-powered application assistance.
- Activity logs for important actions.

## 3. Core Innovation: ALLOW / ASK / BLOCK

CARESYNC uses a backend-enforced permission gateway.

| Decision | Function |
|---|---|
| ALLOW | Execute authorized and permitted actions. |
| ASK | Hold actions until required family approval. |
| BLOCK | Reject prohibited or unauthorized actions. |

The AI assistant cannot bypass backend authorization. Approval cannot override a BLOCK decision.

## 4. MCP Integration

CARESYNC uses the Model Context Protocol (MCP) to connect AI-assisted interactions with application tools.

Planned tools include:
- `create_reminder`
- `get_medicine_stock`
- `calculate_refill_date`
- `schedule_appointment`
- `get_upcoming_appointments`
- `create_approval_request`
- `get_pending_approvals`
- `approve_request`
- `reject_request`
- `get_activity_logs`

All tool actions must pass authentication and permission checks.

## 5. Technology Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI
- **Database:** SQLite, SQLAlchemy
- **AI Tool Integration:** Official Python MCP SDK
- **Transport:** Streamable HTTP
- **Authentication:** JWT and Argon2
- **Testing:** Pytest

## 6. Architecture

User Interface → AI Assistant → MCP Client → Backend Permission Gateway → Application Services → Database.

Approval-dependent actions require authorization and permission revalidation before execution.

## 7. Project Status

CARESYNC is under development as a hackathon prototype.

Features will be marked as implemented only after development and testing. Some capabilities described here are planned features.

The prototype uses fabricated demonstration data. It does not diagnose medical conditions, prescribe medicines or replace professional medical advice.

## 8. Team Details

- **Team:** BUG BUSTERS
- **Institution:** M. S. Ramaiah Institute of Technology
- **Hackathon:** wHACKiest 2026
- **Track:** Make MCP Matter

## 9. Repository Contents

This repository will contain:
- Application source code
- MCP implementation
- Automated tests
- Architecture and technical documentation
- Demonstration screenshots and materials

---

**CARESYNC — Because caring should be connected, simple and secure.**
