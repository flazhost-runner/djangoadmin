import urllib.request

DEFAULT_SLUG = 'agency-consulting-002-creative-agency'

CATALOG = [
    {"slug": "agency-consulting-002-creative-agency", "name": "Creative Agency",      "category": "agency"},
    {"slug": "agency-consulting-001-corporate",       "name": "Corporate Agency",     "category": "agency"},
    {"slug": "saas-005-saas-landing",                 "name": "SaaS Landing",         "category": "saas"},
    {"slug": "saas-001-startup-saas",                 "name": "Startup SaaS",         "category": "saas"},
    {"slug": "ecommerce-001-online-shop",             "name": "Online Shop",          "category": "ecommerce"},
    {"slug": "portfolio-001-personal-portfolio",      "name": "Personal Portfolio",   "category": "portfolio"},
    {"slug": "blog-001-minimal-blog",                 "name": "Minimal Blog",         "category": "blog"},
    {"slug": "restaurant-001-food-restaurant",        "name": "Food Restaurant",      "category": "restaurant"},
    {"slug": "startup-001-tech-startup",              "name": "Tech Startup",         "category": "startup"},
    {"slug": "education-001-online-course",           "name": "Online Course",        "category": "education"},
    {"slug": "fitness-001-gym-fitness",               "name": "Gym & Fitness",        "category": "fitness"},
    {"slug": "real-estate-001-property",              "name": "Property Listing",     "category": "real-estate"},
    {"slug": "medical-001-healthcare",                "name": "Healthcare",           "category": "medical"},
    {"slug": "finance-001-fintech",                   "name": "Fintech",              "category": "finance"},
    {"slug": "travel-001-travel-agency",              "name": "Travel Agency",        "category": "travel"},
    {"slug": "photography-001-photo-studio",          "name": "Photo Studio",         "category": "photography"},
    {"slug": "music-001-music-band",                  "name": "Music Band",           "category": "music"},
    {"slug": "nonprofit-001-charity",                 "name": "Charity / Nonprofit",  "category": "nonprofit"},
    {"slug": "architecture-001-design-studio",        "name": "Design Studio",        "category": "architecture"},
    {"slug": "automotive-001-car-dealer",             "name": "Car Dealer",           "category": "automotive"},
    {"slug": "fashion-001-clothing-store",            "name": "Clothing Store",       "category": "fashion"},
    {"slug": "hotel-001-hospitality",                 "name": "Hotel & Hospitality",  "category": "hotel"},
    {"slug": "landing-001-product-launch",            "name": "Product Launch",       "category": "landing"},
    {"slug": "app-001-mobile-app",                    "name": "Mobile App",           "category": "app"},
]


class FeCatalogService:
    def get_catalog(self, search='', category='', page=1, per_page=12, active_slug=''):
        items = list(CATALOG)

        if search:
            s = search.lower()
            items = [t for t in items if s in t['name'].lower() or s in t['slug'].lower()]
        if category:
            items = [t for t in items if t['category'] == category]

        total = len(items)
        total_page = max(1, (total + per_page - 1) // per_page)
        page = max(1, min(page, total_page))
        start = (page - 1) * per_page
        page_items = items[start:start + per_page]

        page_range = list(range(max(1, page - 2), min(total_page, page + 2) + 1))

        return {
            'items': page_items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_page': total_page,
            'has_prev': page > 1,
            'has_next': page < total_page,
            'page_range': page_range,
        }

    def get_categories(self):
        seen = set()
        cats = []
        for t in CATALOG:
            c = t['category']
            if c not in seen:
                seen.add(c)
                cats.append(c)
        return cats

    def get_preview_html(self, slug):
        url = f'https://cdn.jsdelivr.net/gh/lindoai/opentailwind@main/{slug}/index.html'
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'DjangoAdmin/1.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.read().decode('utf-8', errors='replace')
        except Exception:
            return ''
