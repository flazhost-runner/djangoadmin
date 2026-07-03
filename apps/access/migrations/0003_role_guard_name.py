from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0002_seed'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='guard_name',
            field=models.CharField(default='web', max_length=20),
        ),
    ]
