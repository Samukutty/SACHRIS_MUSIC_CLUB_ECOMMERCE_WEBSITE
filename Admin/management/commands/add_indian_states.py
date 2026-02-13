"""
Management command to add Indian states to the state dropdown.
"""
from django.core.management.base import BaseCommand

from Admin.address_master.models import stateModel


INDIAN_STATES = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttarakhand",
    "Uttar Pradesh",
    "West Bengal",
]


class Command(BaseCommand):
    help = "Add Indian states to the state dropdown"

    def handle(self, *args, **options):
        existing = set(stateModel.objects.values_list('state_name', flat=True))
        added = 0
        for state_name in INDIAN_STATES:
            if state_name not in existing:
                stateModel.objects.create(state_name=state_name)
                added += 1
                existing.add(state_name)
        self.stdout.write(self.style.SUCCESS(f'Added {added} Indian states. Total states: {stateModel.objects.count()}'))
