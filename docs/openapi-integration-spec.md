# OpenAPI Integration Specification

## WebexPythonSDK — Three-Layer Architecture Conversion

**Status:** Draft  
**Spec source:** https://github.com/webex/webex-openapi-specs  
**Target branch:** `claude/webex-openapi-specs-integration-8MmS7`

---

## 1. Problem Statement

The SDK's 22 API wrapper files are hand-maintained. When Webex adds or changes
parameters, someone has to notice and manually update the code. The
`webex/webex-openapi-specs` repository receives near-daily automated commits
from Webex's internal API spec pipeline, covering all 9 Webex service families.
We currently use none of it.

Known drift already present before this work begins:
- `events.py` — missing `serviceType` parameter; `resource` enum values are stale
- ECM folder linking (`/room/linkedFolders`) — not in SDK
- HDS (`/hds/*`) — not in SDK
- BroadWorks, Cloud Calling, Contact Center, Device, UCM, Wholesale — zero SDK coverage

---

## 2. Goals

- Auto-generate a thin network layer from OpenAPI specs that always reflects the
  current Webex API surface
- Preserve 100% of existing public API behavior (signatures, return types, aliases,
  pagination, file upload, AdaptiveCard handling)
- Make new API parameters available immediately via `**request_parameters` without
  any code change
- Make new endpoints accessible as soon as specs are updated
- Run the generator in CI on a schedule so the SDK cannot fall behind

---

## 3. Non-Goals

- Replacing the ergonomic custom layer (`api/*.py`) with raw generated code
- Changing the `RestSession`, `GeneratorContainer`, `check_type`, or object
  factory — these are unchanged
- Generating typed response models from OpenAPI schemas (out of scope)
- Supporting OpenAPI specs other than `webex/webex-openapi-specs`

---

## 4. Target Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  webexpythonsdk/api/*.py            CUSTOM LAYER             │
│                                                              │
│  Hand-maintained. Owns all Pythonic ergonomics:              │
│  • @generator_container (reusable pagination)                │
│  • check_type() validation on every parameter                │
│  • AdaptiveCard → dict serialization (messages)              │
│  • Local file → multipart/form-data upload (messages)        │
│  • Python keyword workarounds (_from parameter in events)    │
│  • **request_parameters forward-compat escape hatch          │
│  • Method aliases (edit = update)                            │
│  • Sub-resource methods (me, list_direct, get_meeting_info)  │
│                                                              │
│  Calls into ↓                                                │
├──────────────────────────────────────────────────────────────┤
│  webexpythonsdk/_generated/*.py     GENERATED LAYER          │
│                                                              │
│  Auto-generated from OpenAPI JSON specs. Never hand-edited.  │
│  • One module per spec file (messaging, meeting, admin, …)   │
│  • One function per OpenAPI operationId                      │
│  • Knows endpoint URLs, HTTP methods, parameter placement    │
│  • Calls session.get_items() for list ops (paginated)        │
│  • Calls session.get/post/put/delete for single-object ops   │
│  • Handles Python reserved word conflicts (from → from_)     │
│  • **extra on every function for immediate new-param access  │
│                                                              │
│  Calls into ↓                                                │
├──────────────────────────────────────────────────────────────┤
│  webexpythonsdk/restsession.py      SESSION LAYER (unchanged)│
│                                                              │
│  • Auth, retries, rate limiting, RFC5988 Link pagination     │
│  • get() / get_items() / post() / put() / delete()          │
└──────────────────────────────────────────────────────────────┘
```

### 4.1 Generated Layer Contract

Each function in `_generated/*.py` must satisfy:

1. First argument is always `session` (a `RestSession` instance)
2. Remaining arguments match the OpenAPI spec parameter names exactly, except
   Python reserved words which get a trailing underscore (`from` → `from_`)
3. All optional parameters default to `None`
4. `**extra` accepted on every function; merged into params/body before the call
5. List operations call `session.get_items(url, params=params)` and return its
   generator directly
6. Single-object operations call the appropriate `session.*` method and return
   the JSON dict
7. The module header includes the spec filename and the commit SHA it was
   generated from

### 4.2 Custom Layer Contract

Each class in `api/*.py` must satisfy:

1. All existing public method signatures are preserved exactly (including
   default values and parameter order)
2. List methods are decorated with `@generator_container` and yield SDK objects
3. Custom logic (file upload, AdaptiveCard, `_from` rename) lives entirely in
   this layer
4. Methods delegate the HTTP call to the corresponding `_generated` function
5. `**request_parameters` is accepted and passed through as `**extra`

---

## 5. Repository Layout After Conversion

```
webexpythonsdk/
├── _generated/
│   ├── __init__.py
│   ├── _utils.py            # shared _compact() helper, reserved word map
│   ├── messaging.py         # from webex-messaging.json
│   ├── meeting.py           # from webex-meeting.json
│   ├── admin.py             # from webex-admin.json
│   ├── cloud_calling.py     # from webex-cloud-calling.json
│   ├── broadworks.py        # from webex-broadworks.json
│   ├── contact_center.py    # from webex-contact-center.json
│   ├── device.py            # from webex-device.json
│   ├── ucm.py               # from webex-ucm.json
│   └── wholesale.py         # from webex-wholesale.json
├── api/                     # unchanged in structure, updated internals
│   ├── messages.py
│   ├── rooms.py
│   └── ...
generator/
├── openapi_to_generated.py  # new: reads specs → writes _generated/*.py
├── specs/                   # new: local copies of OpenAPI JSON files
│   ├── webex-messaging.json
│   ├── webex-meeting.json
│   └── ...
├── models/                  # existing YAML descriptors (kept for meetings)
└── templates/               # existing Jinja2 templates (kept for meetings)
tests/
├── unit/                    # new: mock-based, no credentials needed
│   ├── __init__.py
│   ├── test_generated_layer.py
│   └── test_custom_layer.py
├── api/                     # existing integration tests — unchanged
└── ...
.github/
└── workflows/
    └── sync-openapi-specs.yml  # new: scheduled spec sync + generation
```

---

## 6. Conversion Phases

### Phase 0 — Baseline: Test Before Touching Anything

**Goal:** Lock down the current behavior so regressions are impossible to miss.

#### 6.0.1 Document the public API surface

Run the following to snapshot every public method and its signature before any
changes. Commit this output as `docs/api-surface-baseline.txt`.

```bash
python - <<'EOF'
import inspect, webexpythonsdk
api = object.__new__(webexpythonsdk.WebexAPI)
for attr_name in sorted(dir(api)):
    attr = getattr(type(api), attr_name, None) or getattr(api.__class__, attr_name, None)
    sub = getattr(webexpythonsdk, attr_name.title().replace('_',''), None)
    if hasattr(sub, '__init__'):
        for method_name in sorted(dir(sub)):
            if not method_name.startswith('_'):
                method = getattr(sub, method_name, None)
                if callable(method):
                    try:
                        sig = inspect.signature(method)
                        print(f"{attr_name}.{method_name}{sig}")
                    except (ValueError, TypeError):
                        print(f"{attr_name}.{method_name}(?)")
EOF
```

After Phase 3 completes, run this again and diff. Zero diff is the acceptance
criterion.

#### 6.0.2 Run existing integration tests, record baseline

```bash
# Requires WEBEX_ACCESS_TOKEN and related env vars
pytest tests/ -v --tb=short 2>&1 | tee docs/test-baseline.txt
```

Note which tests are currently marked `xfail` or skipped — these are not
regressions if they remain that way after conversion.

#### 6.0.3 Write unit tests (no credentials required)

Create `tests/unit/test_generated_layer.py` and
`tests/unit/test_custom_layer.py`. These are the primary regression gate
during the conversion — they run in CI without any Webex account.

**`tests/unit/test_generated_layer.py`** must cover:

| Test | What it verifies |
|---|---|
| `test_list_messages_calls_get_items` | `list_messages()` calls `session.get_items('messages', params=…)` |
| `test_list_messages_correct_params` | All non-None params appear in the params dict |
| `test_list_messages_omits_none_params` | None-valued params are excluded from the dict |
| `test_create_message_calls_post` | `create_message()` calls `session.post('messages', json=…)` |
| `test_get_message_constructs_url` | `get_message(session, 'abc')` calls `session.get('messages/abc')` |
| `test_delete_message_constructs_url` | `delete_message(session, 'abc')` calls `session.delete('messages/abc')` |
| `test_update_message_constructs_url` | `update_message(session, 'abc', …)` calls `session.put('messages/abc', …)` |
| `test_list_direct_messages_url` | Uses `'messages/direct'` as the endpoint |
| `test_list_events_renames_from` | `from_` parameter is sent as `'from'` key in params dict |
| `test_list_events_serviceType_param` | `serviceType` is included when provided (the current drift) |
| `test_extra_kwargs_forwarded` | `**extra` kwargs appear in the outgoing params/body |

**`tests/unit/test_custom_layer.py`** must cover:

| Test | What it verifies |
|---|---|
| `test_list_returns_generator_container` | `api.messages.list(roomId='x')` returns `GeneratorContainer` |
| `test_list_is_reusable` | Iterating the container twice both produce results (new generator each time) |
| `test_list_yields_message_objects` | Items are `Message` SDK objects, not raw dicts |
| `test_create_with_url_uses_json_post` | URL in `files` → delegates to generated `create_message` |
| `test_create_with_local_file_uses_multipart` | Local path in `files` → uses `MultipartEncoder`, not generated layer |
| `test_create_closes_file_on_error` | File handle is closed even if multipart post raises |
| `test_create_adaptive_card_object_converted` | `AdaptiveCard` in attachments → converted to dict before send |
| `test_create_adaptive_card_dict_unchanged` | Plain dict in attachments → passed through unmodified |
| `test_edit_is_alias_for_update` | `messages.edit` is the same object as `messages.update` |
| `test_events_accepts_underscore_from` | `events.list(_from='2024-01-01')` sends `from` key to API |
| `test_check_type_error_propagates` | Wrong type raises `TypeError` before any HTTP call |
| `test_request_parameters_forwarded` | `**request_parameters` are passed to the generated function |
| `test_rooms_get_meeting_info` | Calls the right sub-resource URL, returns `room_meeting_info` object |
| `test_people_me` | Calls `people/me` URL |
| `test_messages_list_direct` | Calls `messages/direct` endpoint |

Both test files must run with `pytest tests/unit/ -v` with no environment
variables set.

**Checkpoint:** All unit tests pass before Phase 1 begins.

---

### Phase 1 — Build `generator/openapi_to_generated.py`

**Goal:** A script that reads OpenAPI JSON → writes `_generated/*.py`.

#### 6.1.1 Spec file handling

The generator reads from `generator/specs/`. Add a companion script
`generator/fetch_specs.py` that downloads the 9 JSON files from
`https://raw.githubusercontent.com/webex/webex-openapi-specs/main/public-spec/`
and writes them to `generator/specs/`. Store the commit SHA it fetched from
in `generator/specs/SPECS_VERSION` for traceability.

```
generator/specs/
├── SPECS_VERSION            # "sha: abc123  fetched: 2026-05-21"
├── webex-messaging.json
├── webex-meeting.json
├── webex-admin.json
├── webex-cloud-calling.json
├── webex-broadworks.json
├── webex-contact-center.json
├── webex-device.json
├── webex-ucm.json
└── webex-wholesale.json
```

#### 6.1.2 Generator logic

`openapi_to_generated.py` processes each spec file:

1. **Parse `paths`**: For each path, for each HTTP method, extract:
   - `operationId` (becomes the function name, snake_cased)
   - `parameters` array (query params, path params)
   - `requestBody.content['application/json'].schema.properties` (body params)
   - Response schema: if `items` array type → list endpoint; otherwise → single

2. **Determine session call**:
   - `GET` + array response → `session.get_items(url, params=params)`
   - `GET` + object response → `session.get(url)`
   - `POST` → `session.post(url, json=body)`
   - `PUT` → `session.put(url, json=body)`
   - `DELETE` → `session.delete(url)`

3. **Handle Python reserved words**: Maintain a map of conflicting names:
   ```python
   RESERVED = {'from': 'from_', 'type': 'type_', 'id': 'id_', 'input': 'input_'}
   ```
   In the generated function: accept the safe name, rename to the wire name
   before building the params/body dict.

4. **Path parameter substitution**: Convert `{messageId}` style paths to
   f-strings. Path params are positional (no default), listed first after
   `session`.

5. **Output format** per generated module:
   ```python
   # webexpythonsdk/_generated/messaging.py
   # AUTO-GENERATED — do not edit
   # Source: webex-messaging.json
   # Spec version: {sha from SPECS_VERSION}
   # Generated: {timestamp}

   def _compact(**kw):
       return {k: v for k, v in kw.items() if v is not None}

   # operationId: listMessages
   # GET /messages
   def list_messages(session, roomId, parentId=None, ..., **extra):
       params = _compact(roomId=roomId, parentId=parentId, ..., **extra)
       return session.get_items('messages', params=params)

   # operationId: createMessage
   # POST /messages
   def create_message(session, roomId=None, ..., **extra):
       body = _compact(roomId=roomId, ..., **extra)
       return session.post('messages', json=body)
   ```

6. **Conflict resolution between specs**: Some endpoints appear in multiple
   spec files (e.g., `/rooms` may appear in messaging and admin). The generator
   should put them in the module matching the spec file, not deduplicate. The
   custom layer decides which generated module to import from.

#### 6.1.3 Generator tests

Add `tests/unit/test_generator.py` to test `openapi_to_generated.py` in
isolation using small synthetic OpenAPI JSON fixtures (not the real spec files).
Cover:

| Test | What it verifies |
|---|---|
| `test_get_array_response_uses_get_items` | List endpoints use `get_items` |
| `test_get_object_response_uses_get` | Single-item GET uses `get` |
| `test_post_uses_post` | POST endpoints use `session.post` |
| `test_path_params_are_positional` | Path params appear before optional params |
| `test_reserved_word_renamed` | `from` parameter → `from_` with rename in body |
| `test_none_values_excluded` | `_compact` removes None values |
| `test_extra_kwargs_in_params` | `**extra` merged into outgoing dict |
| `test_module_header_contains_sha` | Generated file includes spec SHA |
| `test_operationid_snake_cased` | `listMessages` → `list_messages` |

**Checkpoint:** Generator unit tests pass. Generator runs end-to-end against
the real spec files and produces syntactically valid Python (`python -m py_compile`
on each output file).

---

### Phase 2 — Generate and Review `_generated/`

**Goal:** Produce the initial generated files and verify they're correct before
touching `api/`.

```bash
python generator/fetch_specs.py          # pull latest specs
python generator/openapi_to_generated.py # write _generated/*.py
python -m py_compile webexpythonsdk/_generated/*.py   # syntax check
```

**Manual review checklist** (do this once, before Phase 3):

- [ ] `list_messages` has `roomId` as required (no default), rest optional
- [ ] `list_direct_messages` uses `'messages/direct'` URL
- [ ] `list_events` has `from_` parameter renamed to `from` in params dict
- [ ] `list_events` includes `serviceType` (currently missing from SDK)
- [ ] `get_message` builds `f'messages/{messageId}'`
- [ ] `list_ecm_folders` exists (currently missing from SDK entirely)
- [ ] `list_rooms` has `teamId`, `type`, `sortBy`, `max`
- [ ] `get_room_meeting_info` exists with path `rooms/{roomId}/meetingInfo`
- [ ] Generated functions contain no `from webexpythonsdk` imports (they're
      standalone; they only receive `session`)

Commit the generated files with message:
`feat: add auto-generated network layer from OpenAPI specs`

---

### Phase 3 — Refactor `api/` to Use the Generated Layer

Refactor one file at a time. After each file: run unit tests. Run integration
tests if credentials are available.

**Order** (simplest → most complex):

| Step | File | Complexity | Special handling |
|---|---|---|---|
| 3.1 | `roles.py` | Low | Pure CRUD, no special cases |
| 3.2 | `organizations.py` | Low | Pure CRUD |
| 3.3 | `licenses.py` | Low | Pure CRUD |
| 3.4 | `events.py` | Low | `_from`/`from` rename, add `serviceType` |
| 3.5 | `webhooks.py` | Low | Pure CRUD |
| 3.6 | `teams.py` | Low | Pure CRUD |
| 3.7 | `attachment_actions.py` | Low | No list, just create + get |
| 3.8 | `team_memberships.py` | Medium | CRUD with query params |
| 3.9 | `memberships.py` | Medium | CRUD with query params |
| 3.10 | `room_tabs.py` | Medium | CRUD with sub-resource |
| 3.11 | `rooms.py` | Medium | `get_meeting_info` sub-resource |
| 3.12 | `admin_audit_events.py` | Medium | Admin scope |
| 3.13 | `recordings.py` | Medium | Optional params on get/delete |
| 3.14 | `people.py` | Medium-High | `me()`, many params, mixed query+body |
| 3.15 | `messages.py` | High | File upload, AdaptiveCard, `list_direct` |
| 3.16 | `meetings.py` and family | Medium | Already generated; wire to `_generated` |
| 3.17 | `guest_issuer.py` | Low | Simple, verify against admin spec |
| 3.18 | `access_tokens.py` | Low | Verify against admin spec |

#### Refactoring pattern for a simple file (e.g., `roles.py`):

**Before:**
```python
def list(self, **request_parameters):
    params = dict_from_items_with_values(request_parameters)
    items = self._session.get_items(API_ENDPOINT, params=params)
    for item in items:
        yield self._object_factory(OBJECT_TYPE, item)
```

**After:**
```python
from .._generated import admin as _gen   # or whichever spec owns roles

def list(self, **request_parameters):
    for item in _gen.list_roles(self._session, **request_parameters):
        yield self._object_factory(OBJECT_TYPE, item)
```

The `check_type`, `@generator_container`, and `object_factory` wrapping stay
exactly as they are. Only the internal HTTP call changes.

#### Refactoring pattern for `events.py` (keyword conflict):

**Before:**
```python
params = dict_from_items_with_values(..., _from=_from, ...)
if _from:
    params["from"] = params.pop("_from")
items = self._session.get_items(API_ENDPOINT, params=params)
```

**After:**
```python
# _gen.list_events handles the from_→from rename internally
for item in _gen.list_events(
    self._session,
    resource=resource, type=type, actorId=actorId,
    from_=_from, to=to, max=max, **request_parameters
):
    yield self._object_factory(OBJECT_TYPE, item)
```

#### Refactoring pattern for `messages.py` (file upload — generated layer not used for multipart):

```python
def create(self, ..., files=None, ...):
    # AdaptiveCard handling stays here
    if attachments:
        ...
    # Branch on file type — stays here
    if files and is_local_file(files[0]):
        # Multipart path — bypass generated layer, call session directly
        try:
            post_data = _gen._compact(roomId=roomId, ...)
            post_data['files'] = open_local_file(files[0])
            multipart_data = MultipartEncoder(post_data)
            headers = {'Content-type': multipart_data.content_type}
            json_data = self._session.post(
                'messages', headers=headers, data=multipart_data
            )
        finally:
            post_data['files'].file_object.close()
    else:
        # Normal path — delegate to generated layer
        json_data = _gen.create_message(
            self._session, roomId=roomId, ..., **request_parameters
        )
    return self._object_factory(OBJECT_TYPE, json_data)
```

The multipart path calls `self._session.post` directly because the generated
layer can only handle JSON bodies. This is by design — the custom layer owns
this complexity.

**Checkpoint after each step:** `pytest tests/unit/ -v` — zero failures.

**Checkpoint after Phase 3 complete:**
1. `pytest tests/unit/ -v` — zero failures
2. Public API surface diff against `docs/api-surface-baseline.txt` — zero diff
3. `pytest tests/` with credentials — same pass/fail pattern as baseline

---

### Phase 4 — Expose New Endpoints

With the generated layer in place, endpoints that exist in the specs but not
in the SDK are now one step away. Add thin custom wrappers for the highest-value
gaps.

**Priority order:**

| Endpoint group | Spec file | Action |
|---|---|---|
| ECM folder linking (`/room/linkedFolders`) | messaging | Add `RoomLinkedFoldersAPI` in `api/room_linked_folders.py` |
| HDS (`/hds/*`) | messaging | Add `HdsAPI` in `api/hds.py` |
| Cloud Calling basics | cloud_calling | Add `CloudCallingAPI` with list/get ops |
| Admin APIs missing from SDK | admin | Audit against `webex-admin.json`, fill gaps |
| BroadWorks, Contact Center, UCM, Wholesale | respective specs | Add API classes as bandwidth allows |

Each new API class follows the exact same pattern as existing classes — thin
ergonomic wrapper over the generated function. Register it in `WebexAPI.__init__`
and in `webexpythonsdk/__init__.py`.

Add integration tests for new endpoints in `tests/api/` following the existing
pattern (fixture creates resource, test asserts validity, fixture tears down).

---

### Phase 5 — Automated Spec Sync (CI/CD)

Create `.github/workflows/sync-openapi-specs.yml`:

```yaml
name: Sync OpenAPI Specs

on:
  schedule:
    - cron: '0 6 * * *'   # 06:00 UTC daily
  workflow_dispatch:        # allow manual trigger

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install requests

      - name: Fetch latest specs
        run: python generator/fetch_specs.py

      - name: Run generator
        run: python generator/openapi_to_generated.py

      - name: Syntax check generated files
        run: python -m py_compile webexpythonsdk/_generated/*.py

      - name: Check for changes
        id: changes
        run: |
          git diff --quiet generator/specs/ webexpythonsdk/_generated/ \
            && echo "changed=false" >> $GITHUB_OUTPUT \
            || echo "changed=true" >> $GITHUB_OUTPUT

      - name: Open PR if specs changed
        if: steps.changes.outputs.changed == 'true'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          BRANCH="openapi-sync/$(date +%Y-%m-%d)"
          git checkout -b "$BRANCH"
          git add generator/specs/ webexpythonsdk/_generated/
          git commit -m "chore: sync OpenAPI specs $(date +%Y-%m-%d)"
          git push origin "$BRANCH"
          gh pr create \
            --title "chore: OpenAPI spec sync $(date +%Y-%m-%d)" \
            --body "Automated spec sync. Review _generated/ diff for new/changed endpoints." \
            --base main \
            --head "$BRANCH"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

The PR diff of `_generated/*.py` is the human review artifact. Any new
function in the generated layer is a new Webex endpoint. Any changed parameter
list signals an API change. Reviewers decide whether to promote the change to
a named parameter in the custom layer.

---

## 7. Testing Strategy

### 7.1 Test categories

| Category | Location | Credentials needed | When run |
|---|---|---|---|
| Generator unit tests | `tests/unit/test_generator.py` | No | Every commit |
| Generated layer unit tests | `tests/unit/test_generated_layer.py` | No | Every commit |
| Custom layer unit tests | `tests/unit/test_custom_layer.py` | No | Every commit |
| Integration tests | `tests/api/test_*.py` | Yes | Pre/post conversion, PRs with credentials |
| API surface snapshot | `docs/api-surface-baseline.txt` | No (offline) | Phase 0 and Phase 3 end |

### 7.2 Mocking approach for unit tests

All unit tests use `unittest.mock.MagicMock` for `RestSession`. The mock
`get_items` should return a configurable list of raw JSON dicts. The mock
`get/post/put/delete` return a configurable JSON dict.

```python
# Canonical test fixture used across unit tests
@pytest.fixture
def mock_session():
    session = MagicMock()
    session.get_items.return_value = iter([
        {"id": "msg1", "roomId": "room1", "text": "hello"},
        {"id": "msg2", "roomId": "room1", "text": "world"},
    ])
    session.get.return_value = {"id": "msg1", "roomId": "room1", "text": "hello"}
    session.post.return_value = {"id": "msg_new", "roomId": "room1", "text": "new"}
    session.put.return_value = {"id": "msg1", "roomId": "room1", "text": "edited"}
    return session

@pytest.fixture
def object_factory():
    from webexpythonsdk.models.simple import simple_data_factory
    return simple_data_factory
```

### 7.3 Acceptance criteria for each phase

**Phase 0:** All unit tests in `tests/unit/` pass. Baseline snapshot committed.

**Phase 1:** `test_generator.py` passes. Generator produces valid Python for
all 9 spec files.

**Phase 2:** Generated files committed. Manual review checklist complete.

**Phase 3:** After each step — `tests/unit/` passes. After all steps —
API surface diff is empty. Integration tests show same pass/fail as baseline.

**Phase 4:** New endpoint tests added and passing in integration suite.

**Phase 5:** Workflow runs successfully on first scheduled trigger. PR
opened when a real spec change is detected.

### 7.4 What a passing run looks like after conversion

```
pytest tests/unit/ -v
# ✓ test_generator.py          — 9 tests
# ✓ test_generated_layer.py    — 11 tests
# ✓ test_custom_layer.py       — 15 tests

pytest tests/ -v   # with credentials
# Same pass/fail as docs/test-baseline.txt
# Zero new failures
# xfail tests remain xfail
```

---

## 8. Behaviors Preserved — Traceability Matrix

| Behavior | Where before | Where after | Test coverage |
|---|---|---|---|
| `@generator_container` reusable generator | `api/*.py` | `api/*.py` (unchanged) | `test_list_is_reusable` |
| `check_type()` type validation | `api/*.py` | `api/*.py` (unchanged) | `test_check_type_error_propagates` |
| AdaptiveCard → dict conversion | `api/messages.py` | `api/messages.py` (unchanged) | `test_create_adaptive_card_object_converted` |
| Local file → multipart POST | `api/messages.py` | `api/messages.py` (unchanged) | `test_create_with_local_file_uses_multipart` |
| File handle closed on error | `api/messages.py` | `api/messages.py` (unchanged) | `test_create_closes_file_on_error` |
| `_from` → `from` param rename | `api/events.py` | `_generated/messaging.py` | `test_list_events_renames_from` |
| `**request_parameters` escape hatch | `api/*.py` | `api/*.py` → `_gen` `**extra` | `test_request_parameters_forwarded` |
| `edit = update` alias | `api/messages.py` | `api/messages.py` (unchanged) | `test_edit_is_alias_for_update` |
| `people.me()` | `api/people.py` | `api/people.py` (unchanged) | `test_people_me` |
| `messages.list_direct()` | `api/messages.py` | `api/messages.py` → `_gen` | `test_messages_list_direct` |
| `rooms.get_meeting_info()` | `api/rooms.py` | `api/rooms.py` → `_gen` | `test_rooms_get_meeting_info` |
| RFC5988 pagination via `get_items` | `api/*.py` calls session | `_generated/*.py` calls session | `test_list_returns_generator_container` |
| Rate limiting / retries | `restsession.py` | `restsession.py` (unchanged) | Existing `test_restsession.py` |

---

## 9. Rollback Plan

The generated layer is purely additive — `_generated/` is a new directory,
nothing in `api/` or `restsession.py` is deleted during Phase 3 (only
internal call sites change). If a step in Phase 3 breaks integration tests:

1. `git revert` the single-file commit for that step
2. That API file reverts to calling `self._session.*` directly
3. Other already-refactored files are unaffected
4. Investigation can proceed without blocking the SDK

The generated files themselves can be deleted without consequence — they can
be regenerated at any time from the specs.

---

## 10. Open Questions

- **Meetings family**: Meetings already have a YAML-based generator. Evaluate
  whether to replace `generator/models/meetings.yaml` with the OpenAPI spec or
  keep both pipelines running in parallel.

- **`dict_from_items_with_values` vs `_compact`**: They do the same thing
  (drop Nones). Decide whether to consolidate or keep both (recommendation:
  keep both; `_compact` lives in `_generated/_utils.py`, DIFWV stays in
  `utils.py` for custom layer).

- **Response model generation**: OpenAPI schemas could generate typed response
  classes. Not in scope here, but the generated layer makes this possible as
  a follow-on.

- **Spec discrepancies**: Some parameters in the SDK don't appear in the spec
  (e.g., `access_token` on some endpoints). Document these in a
  `generator/SPEC_DISCREPANCIES.md` as they're discovered rather than silently
  dropping them.
