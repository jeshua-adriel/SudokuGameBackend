from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]
    operations = [
        migrations.AddField(
            model_name="player",
            name="email",
            field=models.EmailField(blank=True, default="", max_length=254),
        ),
    ]