# Agent-Agnostic MCP Gateway — Master Build & Configuration Directive

## 1. Goal

Build and configure a lightweight, maintainable, agent-agnostic **MCP Gateway / Agent Control Plane** that provides one centrally governed access layer for Claude Code, Codex, custom agents, and future AI runtimes.

The primary outcome is:

> I manage shared tools, access rules, governance, audit requirements, skills/prompts, and integration policies centrally instead of maintaining equivalent rules separately inside Claude, Codex, and every future agent.

The system must preserve runtime independence.

Claude, Codex, or any future agent must be replaceable without redesigning the shared governance architecture.

Do not create separate parallel governance systems for each runtime.

---

# 2. Core Architecture

Implement this logical architecture:

```text
                         ┌─────────────────────────────┐
                         │        .agents-hub          │
                         │   CANONICAL DESIRED STATE   │
                         │                             │
                         │ Governance • Policies       │
                         │ Skills • Schemas • Registry │
                         └──────────┬───────────┬──────┘
                                    │           │
                      defines /     │           │ read-only governance
                      publishes     │           │ metadata
                      governance    │           ▼
                                    │    ┌───────────────────────┐
                                    │    │        ATRIUM         │
                                    │    │ Visibility / Approval │
                                    │    │ Status / Audit / UX   │
                                    │    └───────────▲───────────┘
                                    │                │
                                    ▼                │ status / audit / approval
┌──────────────────┐      ┌──────────────────────────┴───────────┐
│      AGENTS      │      │              MCP GATEWAY             │
│ Claude │ Codex   │─────►│          SHARED CONTROL PLANE        │
│ Custom │ Future  │ MCP  │                                      │
└────────┬─────────┘      │ Catalog • AuthN/AuthZ • Policy       │
         │                │ Validation • Redaction • Audit       │
         │                │ Routing • Rate Limits • Health       │
         │                └──────────────┬───────────────────────┘
         │                               │ governed calls
         │                               ▼
         │                 ┌─────────────────────────────────────┐
         │                 │             UPSTREAMS               │
         │                 │ GitHub MCP • Notion MCP • Files MCP │
         │                 │ SaaS MCPs • APIs • Scripts • DBs    │
         │                 └─────────────────────────────────────┘
         │
         │ runtime-native capabilities
         ▼
┌──────────────────────────────────────────────┐
│       RUNTIME-NATIVE SECURITY CONTROLS       │
│ Shell • Filesystem • Browser • Native Tools  │
│ Claude/Codex/runtime-specific enforcement    │
└──────────────────────────────────────────────┘
```

The responsibilities must remain clearly separated.

The Gateway is authoritative only for capabilities routed through it or through another explicitly equivalent enforcement path.

Runtime-native capabilities remain subject to the runtime's own unavoidable security controls.

Atrium consumes governance/status information and may participate in approval workflows. It does not sit above `.agents-hub` and does not become the source of governance.

---

# 3. Architectural Responsibilities

## `.agents-hub` = Canonical Source of Truth

`.agents-hub` owns the declarative definition of shared:

- governance
- policies
- roles
- capabilities
- tool classifications
- skills
- prompts
- agent definitions
- schemas
- registries
- runbooks
- templates
- verification rules
- approval requirements
- security classifications

Do not move canonical governance into Claude configuration, Codex configuration, or an opaque Gateway database.

The Gateway should **consume and enforce** centrally defined governance.

It should not become an unrelated second source of truth.

If equivalent assets already exist in `.agents-hub`, reuse and refactor them rather than creating duplicates.

---

## MCP Gateway = Enforcement and Access Layer

The Gateway is responsible for Gateway-routed capabilities, including:

- exposing a unified MCP interface
- aggregating upstream MCP servers
- exposing approved APIs/scripts as governed capabilities
- capability discovery
- catalog aggregation
- authentication
- authorization
- role/capability evaluation
- resource scope evaluation
- policy enforcement
- schema validation
- dangerous parameter validation
- sensitive-data handling
- rate limiting
- auditing
- health monitoring
- upstream routing
- namespace management
- failure handling

Every capability designated as Gateway-governed must pass through the Gateway or another explicitly equivalent enforceable control.

Do not claim the Gateway governs a capability unless that capability actually passes through the Gateway or an equivalent enforcement boundary.

The Gateway does **not** automatically govern runtime-native capabilities such as built-in shell execution, filesystem access, browser functionality, or other tools owned directly by Claude, Codex, or another runtime.

Those capabilities remain protected by the minimum necessary runtime-native controls.

---

## Claude / Codex / Future Agents = Workers

Agents should contain only the minimum runtime-specific configuration required to:

- connect to the Gateway
- authenticate
- identify the appropriate principal/client context
- comply with unavoidable runtime-native security controls
- locate shared bootstrap instructions where necessary

Do not duplicate shared business rules or governance separately into:

- Claude rules
- Codex rules
- custom-agent configurations
- future runtime configurations

Runtime-specific configuration is an adapter, not the canonical governance layer.

---

## Atrium = Human Control and Visibility Layer

Atrium should eventually consume Gateway and `.agents-hub` information for:

- system status
- agent status
- available capabilities
- policy visibility
- approvals
- audit events
- errors
- tool health
- MCP server health
- execution history
- governance status

Atrium must not become another independent source of governance truth.

Design the Gateway so Atrium integration can be added cleanly later.

Do not redesign Atrium during this task unless integration work already exists and a minimal compatible interface is required.

---

# 4. Critical Design Principle

The target is:

```text
DEFINE ONCE
     ↓
ENFORCE CENTRALLY
     ↓
USE FROM MANY AGENTS
```

Not:

```text
Claude governance
Codex governance
Custom-agent governance
Future-agent governance
```

The user should not have to manually synchronize equivalent governance between AI runtimes.

A change to a central Gateway-routed tool policy should not normally require manually rewriting the same policy separately for Claude and Codex.

Centralization applies to shared Gateway-governed capabilities. Runtime-native controls that cannot be centralized remain thin, explicitly documented safety boundaries.

---

# 5. Start With Discovery — Do Not Build Blindly

Before modifying anything:

1. Inspect the existing environment.
2. Locate the current `.agents-hub`.
3. Read its bootstrap, registries, governance, skills, policies, schemas, and related documentation.
4. Identify existing MCP configuration.
5. Identify Claude Code configuration.
6. Identify Codex configuration.
7. Identify existing shared assets.
8. Identify existing tool registries.
9. Identify existing scripts/APIs that may eventually be exposed.
10. Identify existing authentication or secrets mechanisms.
11. Identify existing audit/logging mechanisms.
12. Identify duplicated governance already present across runtimes.
13. Identify runtime-native capabilities that remain outside Gateway authority.
14. Identify direct-access paths that could bypass Gateway governance.

Create an evidence-based current-state map.

Do not assume filenames or architecture merely from names.

Read actual contents before deciding their purpose.

Do not overwrite functioning architecture merely because this directive proposes a cleaner theoretical structure.

Integrate with what exists.

---

# 6. Verify Current Official Standards Before Implementation

Before implementing MCP-specific behavior, verify current documentation from authoritative sources.

At minimum verify:

- Model Context Protocol current specification
- MCP transport specification
- MCP authorization specification
- MCP security best practices
- MCP tools
- MCP resources
- MCP prompts
- current Codex MCP documentation
- current Codex configuration documentation
- current Claude Code MCP documentation
- current Claude Code settings/security documentation

Prefer current official documentation over remembered behavior.

If this directive conflicts with a newer official protocol requirement, follow the current official requirement and document the difference.

Do not silently make assumptions about current MCP behavior.

Verify which MCP protocol versions and optional capabilities are actually supported by each client and upstream server used by the implementation.

---

# 7. Transport

For the unified remote Gateway interface, use the current supported **MCP Streamable HTTP transport** unless discovery establishes a material reason not to.

The desired logical result is one Gateway endpoint such as:

```text
http(s)://<gateway-host>/mcp
```

Agents connect to that Gateway instead of individually managing every upstream integration.

Local STDIO MCP servers may still exist behind the Gateway where appropriate.

The Gateway may act as a client to upstream:

- STDIO MCP servers
- Streamable HTTP MCP servers
- approved APIs
- approved local scripts

Do not expose unnecessary services directly.

## Protocol Compatibility

Do not hard-code behavior that assumes one specific MCP revision.

Implement protocol-version negotiation and compatibility according to the current MCP specification and the actual versions supported by:

- Claude Code
- Codex
- other connected clients
- upstream MCP servers

Do not assume protocol-level sessions, GET streams, SSE behavior, or any other transport behavior unless required by the negotiated protocol version.

Where client and upstream versions differ, handle compatibility explicitly and test it.

Document any required compatibility adapter or unsupported protocol behavior.

## Streamable HTTP Security

Implement the security requirements of the negotiated MCP Streamable HTTP specification rather than treating HTTP transport as a generic untrusted POST endpoint.

At minimum:

- validate permitted `Origin` values according to the applicable MCP transport specification
- reject invalid or disallowed origins where the protocol requires origin validation
- for local-only Gateway services, bind to loopback by default rather than exposing the service on all network interfaces
- require appropriate authentication for protected remote Gateway access
- do not rely on network location alone as authentication
- apply appropriate request-size, timeout, concurrency, and resource protections
- protect against DNS-rebinding and equivalent browser-origin abuse where applicable

If the negotiated MCP version exposes or mirrors method, capability, tool, resource, prompt, routing, or other request metadata into HTTP headers for routing, policy, authorization, metering, logging, or intermediary processing:

1. Treat those headers as untrusted until validated according to the applicable MCP protocol version.
2. Validate required consistency between mirrored header metadata and the underlying MCP request/body where the protocol requires it.
3. Reject, ignore, or safely fail requests containing invalid or conflicting metadata.
4. Never authorize a sensitive action solely from unvalidated mirrored header values.
5. Ensure an intermediary cannot authorize one operation while an upstream server executes a different operation represented in the body.

The intended security property is:

```text
HTTP metadata
      +
MCP request/body
      ↓
protocol validation
      ↓
policy / routing / authorization
```

not:

```text
unvalidated HTTP metadata
      ↓
authorization
      ↓
different MCP operation executes
```

---

# 8. Catalog and Discovery

Create a normalized catalog representing available capabilities.

The Gateway must be able to discover and identify:

- upstream MCP servers
- MCP tools
- MCP resources
- MCP prompts
- approved custom tools
- approved scripts
- approved APIs

Store enough metadata to determine:

- canonical name
- provider
- capability type
- description
- input schema
- risk classification
- required role/capability
- resource scopes
- approval requirement
- upstream origin
- availability
- version where relevant
- runtime compatibility where relevant

Prevent naming collisions.

Prefer namespaced capability identifiers when necessary, for example:

```text
github.issue.create
github.repository.read
notion.page.read
notion.database.query
filesystem.file.read
```

Do not allow two upstream capabilities with the same effective identity to silently overwrite one another.

Do not assume every connected runtime supports every MCP capability type identically.

---

# 9. Skills and Prompts

Do not force every skill into an MCP tool.

Maintain canonical skills in `.agents-hub`.

Where useful, expose shared agent instructions through appropriate MCP mechanisms such as:

- prompts
- resources
- server instructions
- governed retrieval

The canonical version must remain traceable to `.agents-hub`.

Avoid creating copies that can drift.

The architecture must distinguish:

```text
Tool
= something that performs or invokes an operation

Resource
= context/data made available to a client

Prompt
= reusable prompt/workflow definition

Skill
= our broader reusable procedural capability, potentially backed by one or more of the above
```

Do not collapse these concepts into one generic category.

Each runtime adapter must identify which MCP primitives it currently supports and degrade cleanly when an optional capability is unavailable.

A missing optional MCP capability must never silently create a security bypass.

---

# 10. Identity Model

Do not rely on an untrusted request field saying:

```text
agent = claude
```

or:

```text
agent = codex
```

as the security boundary.

Authentication must establish trustworthy identity and credential context.

Model identity approximately as:

```text
Authenticated Identity
├── User or Service Principal
├── Client Identity where supported
└── Credential Context
        ↓
Assigned Role(s)
        ↓
Capabilities
        ↓
Resource Scopes
        ↓
Policy Decision
```

Keep policy/audit context distinct from authenticated identity:

```text
Policy / Audit Context
├── runtime: Claude / Codex / Custom
├── project
├── workspace
├── session
└── request metadata
```

Runtime, project, workspace, session, or agent labels may inform policy and auditing, but must not independently create privilege merely because the caller supplied them.

## Authorization Token Trust Boundary

Treat the Gateway and every upstream protected resource as separate authorization trust boundaries.

For HTTP MCP authorization:

- validate inbound credentials according to the current MCP authorization specification
- validate required issuer, signature, expiry, scope, audience/resource binding, and other applicable token claims
- ensure an inbound access token is actually intended for the Gateway resource before accepting it
- reject tokens intended for another MCP server, API, or resource
- never treat possession of a valid token for one protected resource as authorization for another

A client credential presented to the Gateway must **not** automatically become an upstream credential.

The required model is:

```text
Claude / Codex / Client
        │
        │ Gateway-specific credential/token
        ▼
     MCP Gateway
        │
        │ separately authorized upstream credential
        ▼
GitHub / Notion / Other Upstream
```

Do not implement:

```text
Client
   │
   │ Gateway token
   ▼
Gateway
   │
   └──────── forwards same token ────────► Upstream
```

unless a current authoritative protocol and the specific upstream explicitly define a secure delegation/token-exchange mechanism that makes that token valid for the upstream resource.

Never perform raw token passthrough merely for convenience.

When an upstream operation requires authorization:

- obtain or use credentials specifically intended for that upstream resource
- use a supported OAuth delegation/token-exchange flow where legitimate delegated user authorization is required
- preserve the distinction between inbound client identity and outbound upstream authorization
- request only the minimum upstream scopes required
- do not expose upstream credentials to the model unless the operation specifically and safely requires it
- do not log inbound or outbound raw access tokens

The Gateway must not become a confused deputy that converts a client's access to one resource into unintended access to another.

---

# 11. Central Authorization Model

Implement centrally managed authorization.

Support at minimum:

- principals
- roles
- capabilities
- resource scopes
- tool/action policies
- approval requirements
- explicit denies

Example roles may include:

```text
read-only
auditor
project-executor
maintainer
administrator
```

These are examples, not mandatory names.

Do not hard-code policy around Claude versus Codex unless a genuine runtime-specific exception is required.

Prefer:

```text
authenticated identity + trusted context
                ↓
principal → role → capability → scope
```

over:

```text
claude_allowed_tools
codex_allowed_tools
```

The latter may be generated as a compatibility artifact if a runtime requires it, but it must not become the canonical policy model.

---

# 12. Policy Decisions

A governed operation should resolve to one of:

```text
ALLOW
REQUIRE_APPROVAL
DENY
```

Policies should support conditions including:

- principal
- role
- capability
- provider
- operation
- project
- workspace
- resource
- resource scope
- environment
- destructive classification
- credential sensitivity
- external side effect
- network destination where relevant

Explicit DENY must override ALLOW.

Default behavior for unknown sensitive operations should be fail-safe rather than permissive.

`REQUIRE_APPROVAL` represents a policy decision. It must not be treated as proof that a usable or enforceable approval mechanism already exists.

---

# 13. Approval Controls

Central governance must be able to classify operations requiring approval.

Examples may include:

```text
production changes
destructive actions
credential-sensitive operations
external publishing
deployment
database deletion
repository deletion
large-scale file deletion
security-policy changes
privilege escalation
```

Do not duplicate these classifications individually in every agent.

Separate the central policy decision from the mechanism that obtains approval:

```text
Central Policy Engine
        ↓
REQUIRE_APPROVAL
        ↓
Approval Broker / Adapter
     ↙        ↓        ↘
 Codex     Claude     Atrium / Future
```

Where a runtime has unavoidable native approval mechanisms, configure them as a compatibility/safety layer while preserving the central classification as the canonical policy.

Do not claim centralized approval is implemented until the approval path is actually enforceable for that runtime and capability.

The long-term objective is:

```text
central policy definition
        ↓
Gateway enforcement
        ↓
approval broker / runtime-native protection where required
```

not independently maintained governance systems.

---

# 14. Schema Validation and Input Protection

Do not rely on generic "sanitization" alone.

For every tool invocation:

1. Validate the tool exists.
2. Validate the caller is authorized to discover/use it.
3. Validate parameters against the declared schema.
4. Reject unexpected parameters where appropriate.
5. Validate values against policy constraints.
6. Apply scope restrictions.
7. Protect filesystem paths.
8. Protect command execution.
9. Protect URLs/network destinations.
10. Protect against path traversal.
11. Protect against shell/command injection where applicable.
12. Protect against unsafe argument expansion.
13. Reject malformed requests.
14. Enforce size/resource limits where appropriate.

Never concatenate untrusted parameters directly into shell commands.

Prefer structured process invocation over shell-string construction.

---

# 15. Sensitive Data Protection

Implement sensitive-data controls for both:

```text
tool output → agent
```

and:

```text
execution data → logs
```

At minimum detect and protect obvious:

- API keys
- access tokens
- bearer tokens
- passwords
- private keys
- authorization headers
- connection strings containing credentials
- secrets loaded from environment/configuration

Where appropriate, support configurable sensitive-data patterns.

Redaction must not destroy values internally when they are genuinely required to perform an authorized operation.

The principle is:

```text
Use secret internally when authorized
        ↓
Never unnecessarily expose it to model context
        ↓
Never unnecessarily write it to logs
```

Do not log raw secrets.

---

# 16. Secrets Management

Do not put secrets directly in:

- policy files
- source-controlled configuration
- agent definitions
- skills
- prompts
- audit logs
- documentation

Use an appropriate secrets mechanism for the actual environment.

For the initial local implementation, prefer a secure and maintainable mechanism compatible with the operating environment.

Separate:

```text
configuration
```

from:

```text
credentials
```

Document secret references, not secret values.

Inbound Gateway credentials and outbound upstream credentials must be stored, resolved, rotated, and audited as separate authorization contexts.

Do not store or reuse a Gateway client token as though it were a generic credential for upstream systems.

---

# 17. Audit Logging

Create centralized structured audit events.

Do not make a single unstructured text file the only audit system.

A lightweight initial implementation may use append-oriented JSONL with rotation.

Suggested logical categories:

```text
audit/
  executions
  policy-decisions
  authentication
  configuration
  errors
```

This does not mandate separate physical files if a cleaner structured implementation exists.

Each execution event should be capable of recording:

```text
timestamp
request_id
correlation_id
authenticated_principal
client identity where available
runtime/client metadata
project/workspace if known
tool/provider
operation
policy decision
approval state
result status
duration
error classification
```

Sensitive values must be redacted.

Audit authorization outcomes without storing raw access tokens.

Where an upstream call uses separate authorization, records should allow tracing:

```text
authenticated client identity
        ↓
Gateway authorization decision
        ↓
upstream resource selected
        ↓
upstream authorization context/reference
        ↓
execution result
```

without recording raw credentials.

Audit records must allow an execution to be traced through:

```text
client
  ↓
Gateway
  ↓
policy evaluation
  ↓
approval where required
  ↓
upstream execution
  ↓
result
```

Design the event schema so Atrium can consume it later.

---

# 18. Rate Limiting and Resource Controls

Support centrally configurable protections including:

- per-principal limits
- per-role limits
- per-tool limits
- upstream-provider limits
- concurrency limits where appropriate
- request-size limits
- timeout limits
- retry limits

Do not create retry storms.

Respect upstream limits.

Prevent layered retry behavior across clients, the Gateway, and upstream services from multiplying requests unexpectedly.

Dangerous or expensive operations may have stricter limits.

---

# 19. Upstream MCP Management

Treat every upstream MCP server as a dependency.

Track:

- identifier
- transport
- endpoint/command
- authentication method
- enabled state
- available capabilities
- trust classification
- health
- timeout
- retry policy
- version where available
- protocol compatibility where relevant

The Gateway must not silently expose every tool provided by a newly connected upstream server.

New capabilities should be subject to central policy/catalog classification before unrestricted use.

For protected upstreams, track the upstream authorization mechanism separately from the authentication mechanism used by clients to access the Gateway.

---

# 20. Direct-Access Bypass

The architecture should prevent governance from being meaningless.

If a governed tool is supposed to pass through the Gateway, agents should not simultaneously receive unrestricted direct access to the same sensitive upstream integration unless explicitly justified.

Identify existing bypass paths.

Do not automatically break them during discovery.

Document them and migrate safely.

For managed capabilities, the desired state is:

```text
Agent
 ↓
Gateway
 ↓
Upstream
```

rather than:

```text
Agent ──────────────→ Upstream
  └→ Gateway
```

for the same governed capability.

Runtime-native capabilities that cannot be routed through the Gateway must be documented separately along with the native control protecting them.

---

# 21. Fail-Safe Behavior

Implement explicit failure behavior.

## Invalid policy reload

If a new policy/configuration cannot be validated:

- reject the new version
- preserve the last known valid configuration when safely possible
- emit an audit/error event
- do not partially apply the invalid configuration

## Cold start with unusable policy

Fail closed for protected capabilities.

## Gateway unavailable

Managed agents must not silently bypass the Gateway to sensitive upstream systems.

## Upstream unavailable

Return a clear dependency failure.

Do not represent the operation as successful.

## Timeout

Terminate or safely abandon the request according to tool semantics and record the failure.

## Unsupported Runtime Capability

If a runtime does not support an optional MCP capability needed for a non-critical feature:

- report the incompatibility clearly
- degrade only the affected optional feature
- do not weaken authorization or approval requirements
- do not substitute a less-governed direct-access path

## Invalid Authorization Context

If an access token or credential is:

- expired
- invalid
- issued by an untrusted issuer
- intended for another audience/resource
- insufficiently scoped
- otherwise invalid according to the applicable authorization mechanism

reject the request.

Do not fall back to another credential, broader service credential, or direct upstream access merely to make the operation succeed.

---

# 22. Configuration Reload

Where practical, support validated configuration reload without requiring complete manual reconfiguration of every client.

Reload must be:

- validated
- atomic
- auditable
- reversible to last known good state

Do not permit partially loaded policy state.

---

# 23. Health and Diagnostics

Provide diagnostics capable of showing:

- Gateway status
- loaded configuration version
- policy status
- registered upstream servers
- upstream health
- catalog health
- failed integrations
- authentication failures
- authorization/audience failures
- policy failures
- protocol/runtime compatibility failures
- Streamable HTTP validation failures
- recent errors

Do not reveal credentials or sensitive configuration through diagnostics.

Provide a simple verification command/script for local troubleshooting.

---

# 24. Runtime Integration — Codex

Configure Codex to use the Gateway through the currently supported MCP configuration mechanism.

Keep Codex-specific configuration minimal.

Codex configuration should primarily establish:

- Gateway connection
- required authentication reference
- minimal runtime-native safety configuration
- bootstrap pointer where necessary
- any unavoidable runtime-native approval configuration

Do not reproduce the entire shared policy set manually inside Codex.

Document exactly which settings remain Codex-specific and why they cannot be centralized.

Detect and document which required and optional MCP capabilities are supported by the installed/current Codex runtime.

Do not treat an unsupported optional MCP capability as permission to bypass the Gateway.

---

# 25. Runtime Integration — Claude Code

Configure Claude Code to use the same Gateway through the currently supported MCP configuration mechanism.

Keep Claude-specific configuration minimal.

Claude configuration should primarily establish:

- Gateway connection
- required authentication reference
- minimal runtime-native safety configuration
- bootstrap pointer where necessary
- any unavoidable runtime-native approval configuration

Do not reproduce the entire shared policy set manually inside Claude.

Document exactly which settings remain Claude-specific and why they cannot be centralized.

Detect and document which required and optional MCP capabilities are supported by the installed/current Claude Code runtime.

Do not treat an unsupported optional MCP capability as permission to bypass the Gateway.

---

# 26. Future Runtime Requirement

Adding a future agent should ideally require:

```text
1. Establish authenticated principal/client context
2. Assign role/capabilities
3. Configure Gateway connection
4. Add minimal runtime adapter
5. Identify unavoidable native controls
6. Detect supported MCP capability subset
7. Run compatibility and security tests
```

It should **not** require rebuilding:

- tool policies
- permissions architecture
- audit system
- redaction logic
- catalog
- upstream integrations
- shared skills
- governance

Those remain centralized.

A future runtime may support a different subset of MCP capabilities.

The adapter must document those differences and degrade optional functionality cleanly without weakening governance.

Do not design the shared architecture solely around the temporary feature intersection of Claude and Codex.

---

# 27. Implementation Technology

Use either:

- Node.js / TypeScript
- Python

Choose based on:

- existing workspace technology
- maintained MCP SDK support
- compatibility with current upstream integrations
- maintainability
- operational simplicity
- testing support

Do not select a language merely because this directive lists it first.

Document the selection rationale briefly.

Do not require Docker.

The implementation must work cleanly on the existing Windows environment.

Do not introduce unnecessary infrastructure.

---

# 28. Repository / Directory Integration

Do not create a new disconnected configuration universe.

First inspect the existing `.agents-hub` organization.

Then place new components where they logically belong.

A conceptual organization might include:

```text
.agents-hub/
  governance/
  policies/
  registry/
  skills/
  schemas/
  gateway/
  tests/
```

This is illustrative only.

If equivalent canonical locations already exist:

**use them.**

Do not create:

```text
policies/
gateway-policies/
security-policies/
shared-policies/
```

when they contain the same concept.

Fold semantically equivalent rules together.

Avoid bloating the hub.

Every canonical file must have a clear owner/purpose and be registered according to the existing registry system.

---

# 29. Preserve Bootstrap Behavior

The existing agent bootstrap architecture must continue working.

After implementation verify:

- Claude can bootstrap correctly.
- Codex can bootstrap correctly.
- `.agents-hub` remains discoverable.
- canonical registries remain valid.
- existing references are not broken.
- shared skills remain discoverable.
- Gateway configuration can be found from the canonical architecture.
- no required runtime configuration was accidentally removed.

Do not sacrifice existing bootstrapping merely to make the Gateway cleaner.

---

# 30. Governance Compilation / Generation

Where runtime-specific derived configuration is unavoidable, prefer generation from the central canonical policy.

Example:

```text
.agents-hub canonical governance
              ↓
       validated compiler
        ↙             ↘
Codex adapter       Claude adapter
```

Generated compatibility artifacts must clearly identify themselves as generated and not canonical.

Do not manually maintain equivalent policies in multiple destinations if they can be generated.

---

# 31. Canonical Configuration vs Runtime Operational State

Keep canonical desired state separate from Gateway operational state.

`.agents-hub` and its governed repositories own declarative desired state such as:

```text
policies
roles
capabilities
schemas
registries
skills
templates
```

The Gateway owns operational/runtime state such as:

```text
active connections
health state
request state
runtime cache
ephemeral session state
token/session material where required
audit events
operational metrics
```

Do not use `.agents-hub` or Git as a runtime database.

The Gateway may load, compile, or cache canonical configuration, but it must not write operational noise back into canonical governance files merely because those files are convenient.

Operational state must not silently become a competing source of governance truth.

Secrets and ephemeral credentials must remain outside canonical source-controlled configuration.

---

# 32. Policy Validation

Create machine-verifiable policy schemas.

Validate at minimum:

- unknown roles
- unknown capabilities
- invalid tool references
- duplicate identifiers
- contradictory definitions
- invalid scopes
- malformed rules
- unreachable/unused policies where detectable
- unsafe permissive defaults
- references to nonexistent upstream capabilities

Configuration errors must be visible.

Do not silently ignore invalid policy entries.

---

# 33. Security Tests

Build tests proving enforcement rather than merely checking configuration files exist.

At minimum test:

### Authorization

- allowed operation succeeds
- denied operation fails
- approval-required operation cannot bypass approval
- read-only principal cannot perform write action
- privilege change is respected
- unknown principal cannot gain access

### Identity

- caller cannot gain privileges by changing an `agent` or `runtime` string
- caller cannot gain privileges by changing untrusted project/workspace/session metadata
- credentials map to intended principal
- client identity is validated where supported
- invalid credentials fail

### Authorization Token Boundary

Verify:

- a valid token intended for the Gateway is accepted only according to its scopes and policy
- a token with the wrong audience/resource is rejected
- an expired token is rejected
- a token with an invalid issuer or invalid signature is rejected where those checks apply
- an insufficiently scoped token is rejected
- a client token presented to the Gateway is not forwarded unchanged to an upstream protected resource
- upstream calls use credentials or delegated tokens intended specifically for the upstream resource
- if OAuth delegation or token exchange is used, the resulting upstream token has the correct intended resource/audience and scope
- failure to obtain valid upstream authorization does not trigger use of a broader fallback credential
- inbound and outbound raw access tokens do not appear in model-visible output, audit logs, error logs, or diagnostics

### Schema/input

- malformed arguments fail
- unexpected fields fail where appropriate
- path traversal attempt fails
- command-injection attempt fails where command execution exists
- unauthorized resource scope fails

### Streamable HTTP Security

Verify, according to the negotiated MCP transport version:

- valid permitted origins behave correctly
- invalid/disallowed origins are rejected where origin validation is required
- local-only services bind to loopback by default
- protected remote Gateway access requires appropriate authentication
- request limits and timeouts are enforced
- mirrored MCP HTTP metadata used for routing, metering, policy, or authorization is validated before trust
- conflicting or forged mirrored metadata cannot cause the Gateway to authorize one operation while an upstream executes another
- header/body consistency requirements are enforced where the applicable MCP version requires them
- invalid transport metadata fails safely rather than bypassing governance

### Redaction

Inject test secrets and verify they do not appear in:

- agent-visible output where prohibited
- audit logs
- error logs
- diagnostics

### Audit

Verify successful and failed operations produce traceable events.

### Catalog

Verify:

- duplicate tool names are handled
- disabled tools are unavailable
- unauthorized tools are filtered or rejected
- upstream failure is represented correctly

### Rate limits

Verify configured limits actually enforce.

Verify retry behavior does not multiply into retry storms across client, Gateway, and upstream layers.

### Configuration

Verify:

- invalid configuration cannot partially load
- last known valid configuration survives rejected reload
- changes to central policy affect both Claude and Codex without independently rewriting the policy in each runtime
- operational Gateway state does not overwrite canonical `.agents-hub` governance

### Protocol / Runtime Compatibility

Verify:

- actual supported MCP protocol versions are compatible
- negotiation behaves correctly
- required capabilities work for each target runtime
- unsupported optional capabilities degrade cleanly
- missing capabilities do not create a security or governance bypass

---

# 34. Cross-Agent Acceptance Test

This is a critical acceptance requirement.

Using appropriate authorized identities:

1. Connect Codex to the Gateway.
2. Connect Claude Code to the Gateway.
3. Confirm both can access a shared allowed **Gateway-routed** capability.
4. Change its policy centrally.
5. Confirm the changed policy is enforced for both without manually recreating the policy in both runtimes.
6. Confirm audit records identify the separate authenticated callers and relevant runtime context.
7. Confirm forbidden Gateway-routed operations remain forbidden even if the model explicitly requests them.
8. Document any runtime-native capabilities that remain outside Gateway authority and the controls protecting them.
9. Confirm optional MCP capability differences do not create bypass paths.
10. Confirm client-to-Gateway authorization and Gateway-to-upstream authorization remain separate trust boundaries.
11. Confirm neither runtime causes Gateway credentials to be passed through to an upstream protected resource.

This proves the shared control-plane architecture is actually agent-agnostic.

---

# 35. Security Boundary Test

Do not accept:

```text
"The prompt tells the agent not to use the tool."
```

as proof of governance.

A prohibited Gateway-routed operation must be rejected by the enforcement layer even if the requesting model attempts it.

Governance must exist outside the model's willingness to obey instructions.

For runtime-native capabilities outside Gateway authority, verify the applicable runtime-native control separately.

Do not claim the Gateway governs a capability that does not cross its enforcement boundary.

Do not accept successful authentication to the Gateway as proof of authorization to any upstream resource.

---

# 36. Observability for Atrium

Design a stable read interface that Atrium can eventually use for:

```text
gateway health
upstream health
capability catalog
policy status
execution history
approval state
errors
agent/runtime activity
runtime capability compatibility
```

Do not tightly couple the Gateway implementation to the current Atrium UI.

Expose stable structured data instead.

Atrium should consume the control plane rather than become the control plane.

Atrium may later provide a unified human approval interface, but UI state alone must not replace enforceable policy and approval-broker behavior.

---

# 37. Documentation

Create or update documentation sufficient for another agent to understand:

## Architecture

- what `.agents-hub` owns
- what the Gateway owns
- what agents own
- what runtime-native controls remain outside the Gateway
- what Atrium owns
- what upstream MCP servers own
- what is canonical desired state versus runtime operational state
- where the client-to-Gateway authorization boundary ends
- where Gateway-to-upstream authorization begins

## Operation

- starting the Gateway
- stopping the Gateway
- checking status
- validating configuration
- viewing audit information
- adding an upstream MCP
- disabling an upstream MCP
- adding a capability
- changing a role
- changing policy
- connecting an additional agent
- checking protocol/runtime compatibility
- handling approval-required operations
- validating Gateway and upstream authorization contexts

## Recovery

- revert configuration
- recover from invalid configuration
- disable a broken upstream
- disable the Gateway safely
- find logs/errors
- restore last known valid policy

Keep documentation concise and operational.

Do not duplicate information already canonical elsewhere; link/reference it.

---

# 38. Build Verification Script

Provide one straightforward verification entry point.

It should be able to check, as applicable:

```text
Gateway running
configuration valid
policy valid
registry valid
upstreams reachable
catalog loads
authentication works
basic authorization works
Gateway token audience/resource validation works
upstream authorization boundary is separate
token passthrough is not occurring
approval path works where required
audit writable
runtime adapters configured
protocol compatibility valid
Streamable HTTP transport security valid
required runtime capabilities supported
canonical state not contaminated by runtime state
```

Return clear PASS / FAIL results.

A nontechnical operator should be able to run it and understand whether the system is healthy.

---

# 39. Do Not Overengineer Version One

Version one should be production-minded but lightweight.

Prefer:

```text
one Gateway service
structured configuration
central policies
central catalog
structured audit logs
strong tests
minimal runtime adapters
```

over immediately introducing:

```text
Kubernetes
microservices
distributed databases
service mesh
large observability stacks
complex message queues
```

unless the existing environment genuinely requires them.

Build clean extension points instead.

---

# 40. Non-Goals

Do not:

- replace `.agents-hub`
- rebuild Atrium
- create a new agent framework
- lock the architecture to Claude
- lock the architecture to Codex
- duplicate governance per runtime
- pretend the Gateway governs runtime-native capabilities that bypass it
- hide policy inside application code when it belongs in declarative configuration
- put secrets into source control
- expose all upstream MCP tools automatically
- trust caller-provided agent names as authentication
- trust caller-provided runtime/project/workspace metadata as independent authorization
- reuse or forward Gateway client tokens as generic upstream credentials
- accept tokens intended for another protected resource
- authorize from unvalidated mirrored HTTP metadata
- rely only on prompts for security
- unnecessarily containerize the solution
- create duplicate documentation
- create duplicate registries
- create duplicate skills
- create duplicate policies
- use `.agents-hub` or Git as a runtime database
- weaken controls because an optional MCP capability is unsupported
- break existing bootstrapping
- perform destructive cleanup merely to achieve a prettier directory structure

---

# 41. Migration Strategy

Do not switch everything at once without verification.

Use controlled migration:

```text
DISCOVER
   ↓
MAP
   ↓
VERIFY CURRENT PROTOCOL / RUNTIME CAPABILITIES
   ↓
DESIGN AGAINST EXISTING STATE
   ↓
BUILD GATEWAY
   ↓
TEST TRANSPORT + AUTHORIZATION BOUNDARIES
   ↓
CONNECT ONE SAFE CAPABILITY
   ↓
VERIFY
   ↓
CONNECT CODEX
   ↓
VERIFY
   ↓
CONNECT CLAUDE
   ↓
VERIFY
   ↓
MIGRATE ADDITIONAL CAPABILITIES
   ↓
VERIFY
   ↓
IDENTIFY OBSOLETE DUPLICATE CONFIG
   ↓
RETIRE SAFELY
```

Do not delete old configuration until replacement behavior is proven.

Archive/deprecate safely according to existing workspace governance.

Do not remove runtime-native protection unless an equivalent or stronger enforceable control has been proven.

Do not migrate a protected upstream behind the Gateway until its inbound and outbound authorization boundaries have been verified.

---

# 42. Required Deliverables

The task is not complete with only a design document.

Deliver a functioning implementation plus:

1. Gateway service
2. central configuration
3. policy model
4. policy schemas
5. capability/catalog registry
6. upstream MCP configuration
7. authorization implementation
8. authentication implementation
9. approval broker/adapters where required
10. inbound Gateway authorization validation
11. separate upstream authorization handling
12. sensitive-data protections
13. structured auditing
14. rate/resource controls
15. Streamable HTTP security controls
16. health/diagnostic interface
17. Codex adapter/configuration
18. Claude Code adapter/configuration
19. runtime/protocol compatibility record
20. automated tests
21. verification script
22. concise architecture documentation
23. operator runbook
24. migration record
25. implementation report

Do not generate placeholder files merely to satisfy this list.

Only create artifacts that have a real functional purpose.

---

# 43. Completion Criteria

This project is DONE only when the following have been verified:

- [ ] `.agents-hub` remains the canonical governance source.
- [ ] Canonical governance/configuration is separated from runtime operational state.
- [ ] A functioning MCP Gateway exists.
- [ ] The Gateway exposes a unified MCP interface.
- [ ] Gateway governance scope is explicitly limited to Gateway-routed capabilities or equivalent enforceable paths.
- [ ] At least one real upstream capability works through the Gateway.
- [ ] Authentication works.
- [ ] Central authorization works.
- [ ] Inbound Gateway tokens/credentials are validated for the correct protected resource.
- [ ] Wrong-audience/resource credentials are rejected.
- [ ] Gateway client credentials are not passed through as generic upstream credentials.
- [ ] Upstream authorization uses credentials or delegated tokens intended for the actual upstream resource.
- [ ] ALLOW / REQUIRE_APPROVAL / DENY behavior is enforceable for supported Gateway-routed capabilities.
- [ ] Approval classification is separated from the mechanism that obtains approval.
- [ ] Approval-required operations cannot bypass the enforceable approval path.
- [ ] Unauthorized Gateway-routed tool execution is rejected outside the model.
- [ ] Streamable HTTP Origin validation is implemented according to the negotiated protocol.
- [ ] Local-only Gateway exposure defaults to loopback.
- [ ] Mirrored MCP HTTP metadata is not trusted for policy/routing/authorization until validated.
- [ ] Header/body or equivalent metadata consistency requirements are enforced where required by the negotiated protocol.
- [ ] Sensitive output/log redaction is tested.
- [ ] Structured audit events are generated.
- [ ] Policy/configuration validation works.
- [ ] Invalid configuration cannot partially apply.
- [ ] Gateway/upstream health can be checked.
- [ ] Actual MCP protocol compatibility is verified for supported clients/upstreams.
- [ ] Codex connects successfully.
- [ ] Claude Code connects successfully.
- [ ] Required MCP capabilities are verified for both runtimes.
- [ ] Unsupported optional capabilities degrade safely.
- [ ] Shared policy can govern both agents for Gateway-routed capabilities.
- [ ] A central policy change does not require manually duplicating the equivalent rule in both agents.
- [ ] Runtime-native capabilities outside Gateway authority are explicitly documented with the controls protecting them.
- [ ] Existing `.agents-hub` bootstrap behavior still works.
- [ ] Runtime operational state does not overwrite canonical governance.
- [ ] No unnecessary duplicate governance was introduced.
- [ ] No secrets were committed.
- [ ] Verification tests pass.
- [ ] Recovery/rollback instructions exist.
- [ ] Architecture is documented.
- [ ] Remaining runtime-specific controls are explicitly documented with the reason each must remain runtime-specific.

---

# 44. Required Final Report

When implementation is complete, provide a concise final report containing:

## A. Verdict

State whether the Gateway is operational.

## B. Architecture Implemented

Show the final actual architecture, not merely the proposed architecture.

Clearly identify:

- Gateway-routed capabilities
- runtime-native capabilities outside Gateway authority
- canonical desired state
- runtime operational state
- client-to-Gateway authorization boundary
- Gateway-to-upstream authorization boundary

## C. Files Changed

List:

- created
- modified
- retired/archived

Explain why each exists.

## D. Integrations

State which upstream MCP servers/tools are actually connected.

## E. Runtime Status

Report separately:

```text
Codex: PASS / FAIL / PARTIAL
Claude Code: PASS / FAIL / PARTIAL
```

Also state the tested MCP protocol/capability compatibility of each.

## F. Governance Tests

Report:

```text
Authentication
Authorization
Token audience/resource validation
Token passthrough prevention
Upstream authorization separation
RBAC/capabilities
Approval enforcement
Input validation
Streamable HTTP Origin validation
HTTP metadata/header integrity
Secret redaction
Audit logging
Rate limiting
Configuration validation
Protocol compatibility
Runtime capability compatibility
Canonical/runtime-state separation
```

with PASS / FAIL / NOT TESTED.

## G. Cross-Agent Test

State whether a central policy was successfully enforced across both Claude and Codex for a Gateway-routed capability.

## H. Remaining Runtime-Specific Configuration

List only controls that genuinely must remain runtime-specific and explain why.

Include runtime-native capabilities that remain outside Gateway authority.

## I. Risks / Unknowns

Clearly mark anything not verified.

## J. Operator Instructions

Give the shortest possible instructions for:

```text
Start
Stop
Verify
View health
View audit
Change policy
Add an MCP
Disable an MCP
Handle approval
Check compatibility
Check authorization boundaries
Rollback
```

---

# 45. Execution Rules

You are responsible for implementing and verifying the system, not merely describing how it could be implemented.

Proceed autonomously through discovery, design, implementation, configuration, testing, refactoring, and documentation.

Use evidence from the existing environment and current official documentation.

Do not ask the user to make technical architecture decisions that can be resolved through inspection, testing, or authoritative documentation.

When multiple implementation choices are viable, choose the option that best supports:

1. agent independence
2. centralized management
3. reliability
4. security
5. maintainability
6. automation
7. low operational burden
8. extensibility
9. observability
10. minimal duplication

Do not make destructive changes without explicit approval.

Do not expose or print secrets.

Do not silently weaken existing security.

Do not delete functioning legacy configuration until its replacement has been tested.

Do not claim centralized enforcement, approval, authorization, or governance unless the relevant path has actually been tested.

Do not treat successful client authentication to the Gateway as proof that the client is authorized to any upstream resource.

If credentials or external authorization are required, complete all work possible without them first, then identify precisely what remains blocked.

---

# 46. Governing Principle

The final system should make this statement true:

> I configure shared agent governance and capabilities centrally. The MCP Gateway enforces that governance for capabilities routed through it. Claude, Codex, and future agents connect through thin adapters rather than requiring me to recreate the same shared tools, permissions, policies, and safety controls separately for every runtime. Unavoidable runtime-native controls remain minimal, explicit, and documented. Client-to-Gateway authorization and Gateway-to-upstream authorization remain separate, enforceable trust boundaries.

The architecture must therefore optimize for:

```text
ONE GOVERNANCE SOURCE
ONE SHARED CONTROL PLANE
MANY AGENTS
MANY CAPABILITIES
MINIMAL DUPLICATION
CENTRAL AUDITABILITY
EXPLICIT SECURITY BOUNDARIES
SEPARATE AUTHORIZATION TRUST BOUNDARIES
```

Build and verify that system.
