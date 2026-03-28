# Add Model
Scaffold a new Django model in the `directory` app, wire it up with admin registration, and create the migration.

$ARGUMENTS

## Instructions

1. Parse $ARGUMENTS for the model name and any field descriptions (e.g. `Tag name:CharField slug:SlugField`). If none are provided, ask the user for the model name and fields before proceeding.
2. Read `sitelike/directory/models.py` to understand existing patterns (TimestampedModel base class, CATEGORY_CHOICES style).
3. Add the new model to `sitelike/directory/models.py`:
   - Extend `TimestampedModel` from `directory.base_models` unless there is a good reason not to.
   - Add a `__str__` method returning a meaningful string.
   - Add a `class Meta` with `app_label = 'directory'` and `ordering` if appropriate.
4. Register the model in `sitelike/directory/admin.py` with `@admin.register(ModelName)`.
5. Create and apply the migration:
   ```bash
   cd sitelike && python manage.py makemigrations directory
   cd sitelike && python manage.py migrate
   ```
6. Show the generated migration file path and confirm the migration applied successfully.
7. If the model needs to be exposed in views/URLs, note what still needs to be done (view, URL pattern, template) but do not add those automatically unless asked.
