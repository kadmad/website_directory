# Add View
Scaffold a new Django CBV (class-based view) for a given model, register the URL, and create the template.

$ARGUMENTS

## Instructions

1. Parse $ARGUMENTS for the model name and view type (List, Detail, Create, Update, Delete). Example: `Directory Create`. If not provided, ask the user.
2. Read the following files before making any changes:
   - `sitelike/directory/views.py` — understand existing view patterns
   - `sitelike/sitelike/urls.py` — understand URL naming conventions
   - `sitelike/directory/models.py` — understand the model fields
   - `sitelike/directory/forms.py` — check if a ModelForm already exists for this model
3. Add the new view class to `sitelike/directory/views.py` following CBV conventions:
   - Use `reverse_lazy` for `success_url` in create/update/delete views.
   - Import the model and form at the top of the file.
   - Follow the existing naming pattern: `<Model><ViewType>View`.
4. Register the URL in `sitelike/sitelike/urls.py`:
   - URL pattern: `/websites/<model-slug>/` for list, `/websites/<model-slug>/<pk>/` for detail, etc.
   - URL name: `<model-kebab>-<action>` (e.g. `tag-list`, `tag-detail`).
5. Create the template at `sitelike/directory/templates/directory/<model>_<action>.html`:
   - Extend the base template if one exists, otherwise use a minimal Bootstrap 4 structure.
   - For list views, iterate over the context object list.
   - For detail views, display all relevant model fields.
   - For form views, render `{{ form|crispy }}` and include `{% csrf_token %}`.
6. If a `ModelForm` does not yet exist for this model and the view requires one (Create/Update), add it to `sitelike/directory/forms.py`.
7. Summarize what was created and list any manual steps remaining (e.g. linking from nav).
