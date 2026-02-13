# Generated migration to add Indian states

from django.db import migrations


def add_indian_states(apps, schema_editor):
    stateModel = apps.get_model('address_master', 'stateModel')
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
    existing = set(stateModel.objects.values_list('state_name', flat=True))
    for state_name in INDIAN_STATES:
        if state_name not in existing:
            stateModel.objects.create(state_name=state_name)
            existing.add(state_name)


def remove_indian_states(apps, schema_editor):
    stateModel = apps.get_model('address_master', 'stateModel')
    INDIAN_STATES = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
        "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
        "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
        "Telangana", "Tripura", "Uttarakhand", "Uttar Pradesh", "West Bengal",
    ]
    stateModel.objects.filter(state_name__in=INDIAN_STATES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('address_master', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_indian_states, remove_indian_states),
    ]
