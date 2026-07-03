from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='favicon',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
