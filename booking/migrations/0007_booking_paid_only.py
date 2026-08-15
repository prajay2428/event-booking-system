from django.db import migrations, models


def mark_existing_bookings_paid(apps, schema_editor):
    Booking = apps.get_model("booking", "Booking")
    Booking.objects.exclude(payment_status="paid").update(payment_status="paid")


class Migration(migrations.Migration):
    dependencies = [
        ("booking", "0006_rename_amount_paid_total_amount"),
    ]

    operations = [
        migrations.RunPython(mark_existing_bookings_paid, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="booking",
            name="payment_status",
            field=models.CharField(
                choices=[("paid", "Paid")],
                default="paid",
                max_length=10,
            ),
        ),
    ]
