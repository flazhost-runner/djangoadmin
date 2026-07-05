"""Frontend (landing) template catalog — curated from opentailwind
(https://github.com/lindoai/opentailwind, MIT). Mirrors NodeAdmin's
src/config/feTemplates.ts. Each template is self-contained (HTML + Tailwind v4
CDN) and downloaded on-demand when the admin selects it (see
apps.home.services.fe_template_service).

Special slug 'default' renders the local Django landing view (fe/default)
instead of a downloaded raw HTML file.
"""
import re

# Raw GitHub base URL for on-demand template downloads.
FE_TEMPLATE_BASE_URL = 'https://raw.githubusercontent.com/lindoai/opentailwind/master/landings'

# GitHub API tree (recursive) listing all 640 landings.
FE_TEMPLATE_TREE_URL = 'https://api.github.com/repos/lindoai/opentailwind/git/trees/master?recursive=1'

# Local cache folder (relative to BASE_DIR). Lives under storage/ (the runtime
# writable dir, same root as MEDIA_ROOT) — NOT under static/, so collectstatic
# and WhiteNoise never touch it and the cache survives without a re-collect.
FE_TEMPLATE_DIR = 'storage/fe/templates'

# Catalog disk cache (the 640 list) from the GitHub tree fetch.
FE_TEMPLATE_CATALOG_FILE = 'storage/fe/templates/_catalog.json'

# opentailwind slug pattern: `{category}-{NNN}-{name}` (category may contain
# hyphens, e.g. `agency-consulting`). Used by the validator (anti-SSRF: fixed
# charset a-z0-9- + fixed structure) and to derive display metadata.
FE_TEMPLATE_SLUG_RE = re.compile(r'^([a-z]+(?:-[a-z]+)*)-(\d{3})-([a-z0-9-]+)$')

# Special slug: render the bundled Django landing view (fe/default, landing v6)
# instead of serving a cached opentailwind HTML file.
FE_TEMPLATE_DEFAULT_VIEW = 'default'

# Default active template (matches NodeAdmin DEFAULT_FE_TEMPLATE).
DEFAULT_FE_TEMPLATE = 'agency-consulting-002-creative-agency'


def _titleize(value: str) -> str:
    """Title-case hyphen segments: `digital-marketing` -> `Digital Marketing`."""
    return ' '.join(w.capitalize() for w in value.split('-') if w)


def derive_fe_template(slug: str) -> dict:
    """Derive display metadata from an opentailwind slug. If the slug does not
    match the pattern, use the slug as-is with category 'Other'."""
    m = FE_TEMPLATE_SLUG_RE.match(slug)
    if not m:
        return {'slug': slug, 'name': _titleize(slug), 'category': 'Other'}
    category, _, name = m.groups()
    return {'slug': slug, 'name': _titleize(name), 'category': _titleize(category)}


# Curated catalog (~15 of 640 opentailwind landings) — offline fallback.
FE_TEMPLATES = [
    {'slug': 'agency-consulting-002-creative-agency', 'name': 'Creative Agency', 'category': 'Agency'},
    {'slug': 'agency-consulting-001-digital-marketing-agency', 'name': 'Digital Marketing Agency', 'category': 'Agency'},
    {'slug': 'technology-saas-001-hero-focused-conversion-page', 'name': 'SaaS — Hero Focused', 'category': 'Technology'},
    {'slug': 'technology-saas-002-feature-rich-multi-section', 'name': 'SaaS — Feature Rich', 'category': 'Technology'},
    {'slug': 'ecommerce-retail-001-fashion-boutique', 'name': 'Fashion Boutique', 'category': 'E-commerce'},
    {'slug': 'ecommerce-retail-002-luxury-fashion-brand', 'name': 'Luxury Fashion', 'category': 'E-commerce'},
    {'slug': 'portfolio-creative-001-creative-portfolio', 'name': 'Creative Portfolio', 'category': 'Portfolio'},
    {'slug': 'portfolio-creative-002-minimal-portfolio', 'name': 'Minimal Portfolio', 'category': 'Portfolio'},
    {'slug': 'professional-services-001-law-firm', 'name': 'Law Firm', 'category': 'Professional'},
    {'slug': 'real-estate-property-001-real-estate-agency', 'name': 'Real Estate Agency', 'category': 'Real Estate'},
    {'slug': 'food-hospitality-001-fine-dining-restaurant', 'name': 'Fine Dining', 'category': 'Food'},
    {'slug': 'healthcare-wellness-001-family-doctor-clinic', 'name': 'Family Clinic', 'category': 'Healthcare'},
    {'slug': 'education-training-001-private-school', 'name': 'Private School', 'category': 'Education'},
    {'slug': 'fitness-sports-001-fitness-center', 'name': 'Fitness Center', 'category': 'Fitness'},
    {'slug': 'travel-tourism-001-travel-agency', 'name': 'Travel Agency', 'category': 'Travel'},
]

# Valid curated slugs (for validation).
FE_TEMPLATE_SLUGS = [t['slug'] for t in FE_TEMPLATES]


def get_fe_template(slug: str = None) -> dict:
    """Find template metadata by slug (fallback to the default template)."""
    for t in FE_TEMPLATES:
        if t['slug'] == slug:
            return t
    return next(t for t in FE_TEMPLATES if t['slug'] == DEFAULT_FE_TEMPLATE)
