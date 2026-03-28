# Migrate
Safely create and apply Django database migrations after model changes.

$ARGUMENTS

## Instructions

1. Read `sitelike/directory/models.py` to understand what changed (or use $ARGUMENTS as a description of the change).
2. Check for unapplied migrations before creating new ones:
   ```bash
   cd sitelike && python manage.py showmigrations directory
   ```
3. Generate the migration:
   ```bash
   cd sitelike && python manage.py makemigrations directory
   ```
   - If $ARGUMENTS contains a descriptive name (e.g. `add_tag_field`), use it: `python manage.py makemigrations directory --name $ARGUMENTS`
4. Read the generated migration file and confirm it looks correct (right fields added/removed/altered, no unexpected changes).
5. Apply the migration:
   ```bash
   cd sitelike && python manage.py migrate
   ```
6. Verify by running `showmigrations` again and confirming the new migration is marked `[X]`.
7. If the migration fails, report the error and suggest a fix. Do NOT delete migration files — use `migrate directory <previous>` to roll back if needed.
8. Remind the user to commit both the model changes and the new migration file together.
