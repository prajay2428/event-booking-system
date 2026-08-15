from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("booking", "0005_bookingseat_unique_show_seat"),
    ]

    operations = [
        migrations.RenameField(
            model_name="booking",
            old_name="amount_paid",
            new_name="total_amount",
        ),
    ]
