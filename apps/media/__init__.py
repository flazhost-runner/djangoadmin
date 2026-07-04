# PLACEHOLDER MODULE — apps.media
#
# The real media module was never committed: the .gitignore pattern `media/`
# also matches `apps/media/`, so the module is missing from the repository
# while still being referenced by INSTALLED_APPS (config/settings/base.py)
# and config/urls.py — without this stub the app cannot boot.
#
# Upstream fix: change the .gitignore pattern to `/media/` (root-anchored) or
# add `!apps/media/`, commit the real module, and delete this stub package.
