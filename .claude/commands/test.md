# Test
Run the Django test suite for the directory app, optionally scoped to a specific test case or method.

$ARGUMENTS

## Instructions

1. The working directory for all test commands is `sitelike/`. Always prefix commands with `cd sitelike &&`.
2. If $ARGUMENTS is empty, run the full app test suite:
   ```bash
   cd sitelike && python manage.py test directory --verbosity=2
   ```
3. If $ARGUMENTS names a specific test class or method (e.g. `MyTestCase` or `MyTestCase.test_something`), scope the run:
   ```bash
   cd sitelike && python manage.py test directory.tests.$ARGUMENTS --verbosity=2
   ```
4. Report the output — number of tests run, failures, errors.
5. If any tests fail, read the relevant test file (`sitelike/directory/tests.py`) and the source file under test to diagnose the failure. Explain what went wrong and suggest a fix.
6. If the test file is empty or tests don't exist yet for the area, note that and offer to write tests.
