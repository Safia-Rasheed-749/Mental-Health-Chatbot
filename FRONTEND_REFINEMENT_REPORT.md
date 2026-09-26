# MindCare AI — Frontend Refinement and 403 Resolution Report

## Report status

The dashboard 403 error after signup/login was diagnosed and fixed in the
backend access-control layer.

## Cause of the error

The dashboard called:

```text
get_messages_by_user(user_id)
```

The HTTP compatibility layer translated this to:

```text
GET /admin/messages?user_id=1
```

The endpoint required `admin_claims`, so normal users correctly received:

```text
403 Forbidden
```

This was not a database failure or signup failure. It was an authorization
mismatch between shared dashboard functions and admin-only routes.

## Fix implemented

`backend/app/api/application_routes.py` now uses a scoped authorization rule:

```text
User may access their own records
Administrator may access selected users' records
User may not access another user's records
```

The following endpoints were updated:

- `/admin/messages`
- `/admin/moods`
- `/admin/journals`
- `/admin/activity`

The endpoint names are retained for frontend compatibility, but access is now
controlled by the authenticated JWT user ID and `is_admin` claim.

## Expected behavior after restarting FastAPI

Normal user:

```text
GET /admin/messages?user_id=<own_id>  → 200 OK
GET /admin/moods?user_id=<own_id>     → 200 OK
GET /admin/journals?user_id=<own_id>  → 200 OK
```

Normal user attempting another user's data:

```text
→ 403 Forbidden
```

Administrator accessing another user's data:

```text
→ 200 OK
```

## Required restart

Stop the old backend process and restart it so the route changes are loaded:

```powershell
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Then restart Streamlit if necessary:

```powershell
streamlit run frontend/app.py
```

## Frontend professional refinement recommendations

## Implemented visual refinement

The first frontend refinement pass is now implemented in the shared styling
layer:

- strengthened `frontend/layout_utils.py` with one shared widget design system;
- standardized page width, spacing, typography, cards, metrics, buttons,
  inputs, alerts, expanders, tables, charts, and focus states;
- added responsive behavior for tablet and mobile widths;
- improved sidebar surfaces and navigation-button alignment;
- fixed the invalid navbar gradient declaration and added responsive navbar
  rules in `frontend/components/navbar.py`;
- corrected the authentication input text color from bright red to an
  accessible dark text color;
- kept page-specific functionality unchanged.

### Chat UX correction pass

- Fixed the exercise recommendation navigation by adding authenticated
  `Exercises` routing and synchronized query/session state.
- Replaced the large default Streamlit disclaimer alert with a compact,
  branded wellness notice.
- Added a calmer exercise recommendation card instead of a generic alert.
- Added extra bottom spacing and a translucent input dock so the fixed chat
  bar does not cover the final messages.
- Strengthened automatic scroll-to-latest-message behavior after reruns and
  typewriter responses.
- Added `Exercises` and `History` to the authenticated sidebar navigation.
- Fixed sidebar/navbar CSS errors that prevented some declarations from being
  applied.

Validation after the visual changes:

```text
Frontend compileall: PASS
git diff --check: PASS
```

### Global design system

- Centralize colors, typography, spacing, buttons, cards, and alerts.
- Reduce repeated page-level CSS.
- Avoid unstable selectors such as `:has()` and `nth-child()` wherever
  possible.
- Use consistent responsive breakpoints.
- Keep one maximum content width across authenticated pages.

### Dashboard

- Use consistent summary cards for mood, journal, chat, and activity.
- Keep the PDF export below the primary wellness summary.
- Add proper loading and empty states.
- Avoid presenting model outputs as clinical measurements.

### Chat

- Keep the response area visually dominant.
- Put model prediction chips inside a collapsible “Model insights” section.
- Keep crisis messages visually distinct.
- Use a single persistent disclaimer near the chat header.
- Keep the trajectory chart labelled as a model-signal visualization.

### Authentication

- Remove all debug OTP output.
- Move OTP generation and delivery fully to the backend.
- Do not retain raw passwords in Streamlit session state.
- Add password-strength feedback and accessible labels.

### Mood, journal, and exercises

- Standardize page headers and card spacing.
- Add date filters to mood analytics.
- Add character count and privacy reminders to journal entries.
- Use one consistent exercise-card design with clear start controls.

## Verification checklist

After restarting FastAPI:

1. Sign up or log in.
2. Open the dashboard.
3. Confirm the dashboard loads without HTTP 403.
4. Add a mood and confirm it appears.
5. Add a journal entry and confirm it appears.
6. Open chat history and confirm it loads.
7. Confirm an ordinary user cannot access another user's records.
