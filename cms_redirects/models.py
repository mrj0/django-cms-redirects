from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

RESPONSE_CODES = (
    ('301', '301'),
    ('302', '302'),
)

class CMSRedirect(models.Model):
    site = models.ForeignKey(Site)
    old_path = models.CharField(_('redirect from'), max_length=200, db_index=True,
        help_text=_("This should be an absolute path, excluding the domain name. Example: '/events/search/'."))
    new_path = models.CharField(_('redirect to'), max_length=200, blank=True,
        help_text=_("This can be either an absolute path (as above) or a full URL starting with 'http://'."))
    response_code = models.CharField(_('response code'), max_length=3, choices=RESPONSE_CODES, default=RESPONSE_CODES[0][0],
        help_text=_("This is the http response code returned if a destination is specified. If no destination is specified the response code will be 410."))

    def actual_response_code(self):
        if self.new_path:
            return self.response_code
        return u'410'
    actual_response_code.short_description = "Response Code"
    
    class Meta:
        verbose_name = _('CMS Redirect')
        verbose_name_plural = _('CMS Redirects')
        unique_together=(('site', 'old_path'),)
        ordering = ('old_path',)
    
    def __unicode__(self):
        return "%s ---> %s" % (self.old_path, self.new_path)
