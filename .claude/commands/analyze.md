# Analyze
Analyze a source file or Django component for code quality, bugs, security issues, and Django best-practice violations.

$ARGUMENTS

## Instructions

1. Read the file specified in $ARGUMENTS. If no file is given, ask the user which file to analyze.
2. Identify and report issues in the following categories (skip categories with no findings):
   - **Security**: SQL injection, XSS, CSRF gaps, hardcoded secrets, missing authentication/permission checks, unsafe use of `eval`/`exec`.
   - **Django best practices**: Raw SQL where ORM suffices, missing `select_related`/`prefetch_related` causing N+1 queries, business logic in templates, missing `get_object_or_404`, improper use of `save()` without `update_fields`.
   - **Model issues**: Missing `__str__`, fields without appropriate `null`/`blank` settings, no `Meta.ordering`, unbounded `TextField` used where `CharField` fits.
   - **View issues**: Logic that belongs in the model or form, missing permission checks, unused context variables passed to templates.
   - **Form issues**: Missing validation, fields exposed that shouldn't be user-editable.
   - **Error handling**: Bare `except`, swallowed exceptions, missing `try/finally` in code that acquires resources (e.g. Selenium driver).
   - **Code style**: Unused imports, dead code, overly complex logic that could be simplified.
3. For each issue, state:
   - File and line number
   - Severity: **High** / **Medium** / **Low**
   - Description of the problem
   - Suggested fix (code snippet if helpful)
4. Summarize the overall health of the file at the end.
