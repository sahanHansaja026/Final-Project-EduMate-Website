# Pull Request

## Description

**What does this PR do?**

<!-- Briefly describe the changes implemented in this PR. -->

**Why is this change needed?**

<!-- Explain the problem being solved or the feature being introduced. -->

**Related Issues:**
- Fixes #
- Related to #

---

## Type of Change

- [ ] Bug Fix
- [ ] New Feature
- [ ] Enhancement / Improvement
- [ ] Code Refactoring
- [ ] Database Change / Migration
- [ ] Security Improvement
- [ ] Test Improvement
- [ ] Documentation Update
- [ ] CI/CD or Configuration Change

---

## Implementation Details

### Backend (FastAPI / Python)

- [ ] API endpoints added or modified
- [ ] Business logic implemented or updated
- [ ] Request validation and error handling implemented
- [ ] Authentication and authorization handled correctly
- [ ] Database interactions implemented correctly
- [ ] API documentation updated (if applicable)

**Files / Components Changed:**

<!-- List the important backend files or components. -->

### Frontend (Next.js / React / TypeScript)

- [ ] UI components created or updated
- [ ] API integration implemented or updated
- [ ] Form validation and error handling implemented
- [ ] Loading and empty states handled
- [ ] Responsive design verified
- [ ] User permissions and access restrictions handled

**Files / Components Changed:**

<!-- List the important frontend files or components. -->

### Database (PostgreSQL)

- [ ] Database schema changed
- [ ] Migration added or updated
- [ ] Relationships and constraints verified
- [ ] Queries and indexes reviewed
- [ ] Existing data compatibility considered

**Database Changes:**

<!-- Describe database changes or write N/A. -->

---

## Testing and Verification

### Backend Tests

- [ ] New tests added where necessary
- [ ] Existing tests pass
- [ ] API endpoints tested
- [ ] Validation and error scenarios tested

**Command:**
```bash
cd backend
python -m pytest
```

### Frontend Tests

- [ ] New tests added where necessary
- [ ] Existing tests pass
- [ ] Components and user interactions tested
- [ ] API integration verified

**Command:**
```bash
cd client
npm test
```

### Manual Verification

- [ ] Main functionality verified
- [ ] Edge cases checked
- [ ] Error scenarios verified
- [ ] No unexpected regressions identified

**Testing Evidence:**

<!-- Include actual test results, test counts, and relevant verification details. -->

---

## CI/CD and Code Quality

- [ ] GitHub Actions workflows pass
- [ ] Backend linting and formatting checks pass (if configured)
- [ ] Frontend linting passes (if applicable)
- [ ] Frontend production build passes (if applicable)
- [ ] No unresolved CI failures
- [ ] No unintended merge conflicts

**Verification Commands:**
```bash
cd client
npm run lint
npm run build
```

---

## Security and Configuration

- [ ] No API keys, passwords, tokens, or sensitive information committed
- [ ] Environment variables handled securely
- [ ] Authentication and authorization verified (if applicable)
- [ ] User input validated and sanitized
- [ ] Sensitive data exposure considered
- [ ] Dependencies reviewed (if changed)

**Security Notes:**

<!-- Describe relevant security considerations or write N/A. -->

---

## Documentation

- [ ] README updated (if necessary)
- [ ] API documentation updated (if necessary)
- [ ] Environment configuration documented (if necessary)
- [ ] Technical documentation updated (if necessary)

---

## Screenshots / Demo

<!-- Add screenshots, GIFs, or recordings for UI-related changes. -->

**Before:**

<!-- Screenshot or N/A -->

**After:**

<!-- Screenshot or N/A -->

---

## Breaking Changes and Additional Notes

**Breaking Changes:**

<!-- Describe breaking changes or write None. -->

**Additional Notes:**

<!-- Mention dependencies, deployment requirements, known limitations, or reviewer considerations. -->

---

## Final Checklist

- [ ] PR title is descriptive and follows the project naming convention (e.g., `feat: add student attendance management`)
- [ ] Changes are focused on the related issue
- [ ] Code follows project conventions
- [ ] No unnecessary files or unrelated changes included
- [ ] Tests and verification results are accurately reported
- [ ] Documentation updated where necessary
- [ ] Ready for review use this