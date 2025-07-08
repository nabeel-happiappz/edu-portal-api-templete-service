import re
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class CSRFExemptMiddleware(MiddlewareMixin):
    """
    Middleware to exempt certain URLs from CSRF protection.
    URLs matching patterns in CSRF_EXEMPT_URLS will be exempt from CSRF validation.
    """
    
    def process_request(self, request):
        """
        Check if the request URL matches any exempt patterns.
        If it does, set the CSRF_COOKIE_USED flag to False.
        """
        exempt_urls = getattr(settings, 'CSRF_EXEMPT_URLS', [])
        
        for url_pattern in exempt_urls:
            if re.match(url_pattern, request.path):
                # Mark this request as exempt from CSRF protection
                setattr(request, '_dont_enforce_csrf_checks', True)
                break
        
        return None