from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0002_add_availability_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='type',
            field=models.CharField(
                choices=[('learning', 'Learning Skills'), ('services', 'Professional Services')],
                default='learning',
                max_length=20
            ),
        ),
    ]