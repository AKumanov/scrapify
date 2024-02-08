from django.db import models

class Site(models.Model):
    __SITE_NAME_MAX_LENGTH = 255
    
    domain = models.CharField(
        max_length=__SITE_NAME_MAX_LENGTH,
        unique = True,
        help_text='Fully Qualified Domain Name (FQDN)'
    )

    def __str__(self):
        return self.domain
    
class Collector(models.Model):

    STATE_TYPES = [
    ('active', 'Active'),
    ('inactive', 'Inactive')
]
    name = models.CharField(max_length=255) # here it should be choices
    state = models.CharField(max_length=20, choices=STATE_TYPES, default='active')


    def __str__(self):
        return self.name
    
class Contact(models.Model):

    CONTACT_TYPES = [
        ('phone', 'Phone'),
        ('email', 'Email'),
    ]

    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    contact_type = models.CharField(max_length=10, choices=CONTACT_TYPES, blank=True)
    contect_value = models.CharField(max_length=255)
    collector = models.ForeignKey(Collector, on_delete=models.SET_NULL, null=True)
    source = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # It contact type is not set, determine it based on the collector
        if not self.contact_type and self.collector_id:
            if '@' in self.contect_value:
                self.contact_type = 'email'
            else:
                self.contact_type = 'phone'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.site}: {self.contact_type} - {self.contect_value} ({self.source})'


        