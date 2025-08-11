# This migration is no longer needed because 0006 aligns the state-only table name.
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_feedback_table_feedbackattachment'),
    ]

    operations = []
