# EduMate Backend Refactoring Plan

## Overview
This plan outlines the step-by-step refactoring of the EduMate FastAPI backend to improve architecture, separate concerns, and prepare for future scaling.

---

## Phase 1: Foundation (Days 1-3)

### 1.1 Consolidate Security Module
**Action**: Remove `backend/security.py`, keep `backend/core/security.py`
- `core/security.py` already uses `os.getenv("SECRET_KEY", "SUPER_SECRET_KEY")`
- Update all route imports to use `from core.security import ...`
- Remove the duplicate `backend/security.py` file

### 1.2 Fix Naming Inconsistencies
**Action**: Rename misspelled files (no code changes during audit)
| Current Name | Correct Name |
|---|---|
| `models/chaneel_modules.py` | `models/channel_modules.py` |
| `routes/chaneel_modules.py` | `routes/channel_modules.py` |
| `routes/video_acess_contolle.py` | `routes/video_access_control.py` |
| `routes/assignemnt_quota.py` | `routes/assignment_quota.py` |
| `routes/student_enrolle_count_channal.py` | `routes/student_enrollment_count_channel.py` |

### 1.3 Create Configuration Module
**Action**: Create `backend/config/settings.py`
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY")
    ALGORITHM = "HS256"
    AWS_BUCKET = os.getenv("AWS_BUCKET_NAME")
    AWS_REGION = os.getenv("AWS_REGION")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    
settings = Settings()
```

### 1.4 Backup Existing Files
**Action**: Copy entire `backend/` directory before any modifications
- Critical for rollback if refactoring introduces bugs

---

## Phase 2: Service Layer Creation (Days 4-10)

### 2.1 Create `services/quiz_service.py`
**Move logic from**:
- `routes/quiz_quota.py` - quiz quota checking
- `routes/module_quota.py` - module quota (indirectly quiz-related)
- `routes/assignemnt_quota.py` - assignment quota (related)
- `routes/quiz_score.py` - score creation with attempt validation
- `routes/quiz_attempt_controller.py` - attempt access checking
- `routes/quiz.py` - quiz CRUD with attempt counting

**New service should handle**:
- Quiz creation with attempt limit validation
- Quiz score creation with attempt number control
- Quiz attempt access checking
- Quiz deletion with cascade

### 2.2 Create `services/module_service.py`
**Move logic from**:
- `routes/module.py` - module CRUD, access checks
- `routes/module_routes.py` - module search/filtering
- `routes/module_quota.py` - module creation limits
- `routes/module_quiz_access_controller.py` - quiz access by module

**New service should handle**:
- Module creation with skills parsing and image handling
- Module retrieval by user/id
- Module update operations
- Module access checks (owner/public)
- Module search and formatting

### 2.3 Create `services/assignment_service.py`
**Move logic from**:
- `routes/assignment.py` - assignment CRUD with S3
- `routes/submission.py` - assignment submissions with S3
- `routes/assignemnt_quota.py` - assignment quota checking

**New service should handle**:
- Assignment creation with file upload
- Assignment update with file replacement
- Assignment deletion with S3 cleanup
- Assignment submission with file upload
- Assignment quota checking

### 2.4 Create `services/access_service.py`
**Move logic from**:
- `routes/access_control.py` - plan-based access rules
- `routes/video_access_control.py` - video creation/access rules
- `routes/channel_module_access_controller.py` - student enrollment access
- `routes/channel_content_access_controller.py` - content access for channels

**New service should handle**:
- Subscription status checking (active/expired/cancelled)
- Plan-based access determination (free/premium/edu)
- Video creation quota per plan type
- Channel module student enrollment access
- Channel content access control

### 2.5 Create `services/quota_service.py`
**Move logic from**:
- `routes/quiz_quota.py` - free plan: 3 quizzes
- `routes/module_quota.py` - free plan: 1 module
- `routes/assignemnt_quota.py` - free plan: 5 assignments

**New service should handle**:
- Module creation quota per subscription plan
- Quiz creation quota per subscription plan
- Assignment creation quota per subscription plan
- Remaining quota calculation
- Can-create determination

### 2.6 Create `services/subscription_service.py`
**Move logic from**:
- `routes/subscription_routes.py` - subscription management, plan upgrades

**New service should handle**:
- Subscription retrieval by user
- Plan upgrade/downgrade with date calculations
- Subscription status management
- Free subscription automatic creation

---

## Phase 3: Controller Refactoring (Days 11-20)

### 3.1 Convert Routes to Controllers
**Pattern**: Each route file becomes a thin controller that:
1. Imports services from `services/`
2. Imports schemas from `schemas/`
3. Imports database dependency `get_db`
4. Defines endpoint handlers that call services
5. Returns service results

**Example Transformation**:

**Before** (`routes/quiz.py`):
```python
@router.post("/")
def create_quiz(module_id: int = Form(...), ...):
    new_quiz = Quiz(...)
    db.add(new_quiz)
    db.commit()
    ...
```

**After** (`api/v1/controllers/quizzes.py`):
```python
from services.quiz_service import create_quiz

@router.post("/")
def create_quiz(module_id: int = Form(...), ...):
    result = create_quiz(module_id=module_id, title=title, ...)
    return result
```

### 3.2 Update `main.py`
**Action**: Replace the 67+ import/include pattern with selective inclusion
```python
# Instead of importing all routes individually
from api.v1.controllers import auth, users, modules, content, quizzes, ...

# Include only what's needed
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
# etc.
```

### 3.3 Fix Import Patterns
**Action**: Update all route files to import from new service layer
- Replace direct `models.*` imports with service calls
- Replace direct `database.*` imports where services provide deps
- Keep schema imports as they are (thin layer)

---

## Phase 4: Testing (Days 21-25)

### 4.1 Set Up pytest
**Action**: Create `tests/conftest.py` with fixtures:
- Database session fixture (in-memory or test DB)
- Auth token fixture
- Service dependencies

### 4.2 Write Service Tests
**Action**: Test new service layer
```python
def test_quiz_service_creation():
    """Test quiz creation with attempt validation"""
    ...

def test_quiz_service_attempt_limits():
    """Test quiz attempt limits per plan type"""
    ...
```

### 4.3 Write Controller/Route Tests
**Action**: Test endpoints still work after refactoring
```python
def test_create_quiz_endpoint(client):
    """Test quiz creation via API"""
    ...
```

### 4.3 Remove Ad-Hoc Tests
**Action**: Delete or integrate:
- `check.py` - S3 test script
- `test_env.py` - connection test
- `test_conn.py` - connection test
- `test_db.py` - database test

---

## Phase 5: Cleanup (Days 26-30)

### 5.1 Remove Duplicate Files
- Delete `backend/security.py` (consolidated into `core/security.py`)
- Remove any empty/duplicate files identified during audit

### 5.2 Rename All Misspelled Files
- `chaneel_modules` → `channel_modules` (models and routes)
- `video_acess_contolle` → `video_access_control`
- `assignemnt_quota` → `assignment_quota`
- `student_enrolle_count_channal` → `student_enrollment_count_channel`

### 5.3 Update All Imports
- Run `grep` to find and update all references to renamed files
- Update all import statements across the codebase

### 5.4 Final Application Test
- Run `uvicorn main:app` or `python main.py`
- Test all existing endpoints still work
- Verify no regressions

### 5.5 Documentation
- Update README or API documentation
- Document the new folder structure
- List new service layer endpoints

---

## Success Criteria

✅ All route files are thin controllers (no business logic)
✅ All business logic centralized in `services/` directory
✅ No duplicate security implementations
✅ All naming conventions consistent (no misspellings)
✅ pytest test suite with >80% critical path coverage
✅ Application starts and all endpoints functional
✅ No breaking changes to existing API contracts
✅ S3 operations centralized in `services/s3_service.py`
✅ Quota/access logic centralized in `services/quota_service.py` and `services/access_service.py`

---

## Risk Mitigation

| Risk | Mitigation |
|---|---|
| Broken imports | Backup before Phase 1, use `grep` to verify all imports |
| Missing functionality | Test each endpoint after each phase |
| S3 credential issues | Test S3 operations last, use mocking if needed |
| Database schema drift | Use `Base.metadata.create_all()` with careful migrations |
| Team disruption | Document each phase, communicate changes clearly |

---
*Refactoring Plan Generated: Sun Nov 08 2026*
*Based on audit of 120+ Python files across 8 directories*