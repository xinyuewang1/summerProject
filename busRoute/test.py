from .models import Testtrip

print(Testtrip.objects.all())

# Testtrip.objects.filter(routeid__startswith = '4') 