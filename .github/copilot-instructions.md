# MY-AI-TEAM Workspace Instructions

Welcome to MY-AI-TEAM, a collaborative AI-assisted development environment. These instructions guide how Claude Code agents work within your team's codebase.

## Project Overview

**MY-AI-TEAM** is a Dynamics 365 Business Central (AL/Dynamics NAV) development project with multi-agent collaboration enabled. This workspace uses Claude AI for:
- Code generation and refactoring
- Architecture design and planning
- Test-driven development
- Code review and quality assurance
- Documentation and knowledge management

## Core Development Principles

### 1. **Development Workflow**
All work follows a structured development workflow:
1. **Research & Reuse** - Search GitHub, docs, and package registries before writing new code
2. **Plan First** - Use the planner agent to create implementation plans
3. **TDD Approach** - Write tests first, implement to pass, then refactor
4. **Code Review** - Use code-reviewer agent after all code changes
5. **Commit & Push** - Follow conventional commits with detailed messages

### 2. **Code Quality Standards**
- **Immutability First** - Create new objects, never mutate existing ones (CRITICAL)
- **Keep It Simple** - Prefer simplicity over cleverness; optimize for clarity
- **DRY (Don't Repeat Yourself)** - Extract repeated logic into reusable functions
- **YAGNI (You Aren't Gonna Need It)** - Build features when needed, not speculatively
- **File Organization** - Many small, focused files (200-400 lines typical, max 800)

### 3. **Error Handling & Input Validation**
- **Explicit Error Handling** - Handle errors comprehensively at every level
- **Input Validation** - Always validate at system boundaries
- **User-Friendly Messages** - Provide clear, actionable error messages on UI
- **Fail Fast** - Validate early and explicitly reject bad data

### 4. **Naming Conventions**
- **camelCase** - Variables, functions, and methods
- **PascalCase** - Types, interfaces, classes, and components
- **UPPER_SNAKE_CASE** - Constants and compile-time values
- **Descriptive Names** - Use intention-revealing names that explain purpose

## Testing Requirements

**Minimum Coverage: 80%** across three test types:

1. **Unit Tests** - Individual functions and isolated units
2. **Integration Tests** - API endpoints, database operations, service interactions
3. **E2E Tests** - Critical user-facing workflows

**TDD Methodology** (mandatory for new features):
1. Write test first (RED)
2. Implement minimal code to pass (GREEN)
3. Refactor for clarity (IMPROVE)
4. Verify 80%+ coverage

## Security Standards

Before ANY commit, verify:
- [ ] No hardcoded secrets (API keys, passwords, tokens)
- [ ] All user inputs validated
- [ ] Parameterized queries (SQL injection prevention)
- [ ] Sanitized HTML/output (XSS prevention)
- [ ] CSRF protection enabled
- [ ] Authentication/authorization verified
- [ ] Rate limiting on endpoints
- [ ] Error messages don't leak sensitive data

**Mandatory Security Review** when:
- Authentication or authorization code
- User input handling
- Database queries
- File system operations
- External API calls
- Payment or sensitive operations

## Code Review Standards

Every code change requires review. Use `code-reviewer` agent for:
- General code quality and patterns
- Readability and naming
- Function size (<50 lines ideal)
- File size (<800 lines ideal)
- Deep nesting issues (max 4 levels)
- Error handling completeness
- Test coverage adequacy (80%+)

**Security reviews** use `security-reviewer` agent for sensitive code.

**Severity Levels:**
- **CRITICAL** - Security vulnerability or data loss risk → Must fix
- **HIGH** - Major bug or quality issue → Should fix
- **MEDIUM** - Maintainability concern → Consider fixing
- **LOW** - Style or minor suggestions → Optional

## Agent Usage Guidelines

### Primary Agents (Use Automatically)
- **planner** - Complex features, refactoring, system design
- **code-reviewer** - After writing any code (MANDATORY)
- **tdd-guide** - New features, bug fixes with TDD
- **security-reviewer** - Authentication, user input, sensitive data

### Specialist Agents (Task-Specific)
- **architect** - Architectural decisions and system design
- **performance-optimizer** - Bottleneck identification and optimization
- **refactor-cleaner** - Dead code removal and consolidation
- **doc-updater** - Documentation and codemaps

### Build & Error Resolution
- **build-error-resolver** - Build failures and type errors
- **e2e-runner** - End-to-end test management and execution

## Commit Message Format

Follow Conventional Commits:
```
<type>: <description>

<optional body with reasoning and context>
```

**Types:** `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`

**Example:**
```
feat: add multi-locale support for report headers

- Implement locale resolver in navigation service
- Add translation key mapping for 12 supported languages
- Update test coverage to 87%

Closes #142
```

## File Organization Strategy

```
📁 root/
  📁 src/
    📁 modules/           # Feature modules
      📁 orders/
        orders.al
        orderService.al
        orderValidator.al
      📁 inventory/
    📁 utilities/         # Shared utilities
    📁 interfaces/        # Type definitions
  📁 tests/              # Test files
    📁 unit/
    📁 integration/
    📁 e2e/
  📁 docs/               # Documentation
  📁 .github/            # GitHub and CI/CD config
     copilot-instructions.md
    workflows/
  .gitignore
  README.md
```

**Principle:** Organize by feature/domain, not by type. One responsibility per file.

## Development Checklist

Before marking work complete:
- [ ] Code is readable with intention-revealing names
- [ ] Functions are focused (<50 lines)
- [ ] Files are cohesive (<800 lines)
- [ ] No deep nesting (max 4 levels)
- [ ] Errors are handled explicitly
- [ ] No hardcoded values (use named constants)
- [ ] No console.log or debug statements (except intentional logging)
- [ ] Tests exist and pass (80%+ coverage)
- [ ] Code reviewed by peer agent
- [ ] Security review completed if applicable
- [ ] Commit message follows conventional format
- [ ] All CI/CD checks passing

## Quick Reference: When to Use Which Agent

| Trigger | Agent | Purpose |
|---------|-------|---------|
| Writing code | `code-reviewer` | Quality assurance |
| New feature | `tdd-guide` + `planner` | TDD + planning |
| Bug fix | `tdd-guide` | Test-driven fix |
| System design | `architect` | Architecture review |
| Performance issue | `performance-optimizer` | Bottleneck analysis |
| Build fails | `build-error-resolver` | Error resolution |
| Security-related | `security-reviewer` | Vulnerability check |
| Dead code | `refactor-cleaner` | Code cleanup |
| Tests failing | `tdd-guide` | Test debugging |
| Documentation | `doc-updater` | Docs management |

## Project Communication

- **Primary Work Tracking**: GitHub Issues and Pull Requests
- **Code Changes**: Follow git workflow with meaningful branches
- **Team Decisions**: Document in ARCHITECTURE.md or DECISIONS.md
- **Documentation**: Keep docs in `/docs/` and linked from README

## Continuous Improvement

This workspace evolves. As patterns emerge or new best practices are discovered:
1. Update these instructions with the pattern
2. Create file-specific `.instructions.md` files for complex areas
3. Add custom agents or prompts for specialized workflows
4. Review quarterly for outdated or redundant guidance

---

**Last Updated**: 2026-04-15  
**Version**: 1.0  
**Maintainer**: Team
