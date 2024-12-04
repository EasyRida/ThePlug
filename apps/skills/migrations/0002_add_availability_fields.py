from django.db import migrations, models
import django.core.validators

class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='available_from',
            field=models.TimeField(default='09:00'),
        ),
        migrations.AddField(
            model_name='skill',
            name='available_to',
            field=models.TimeField(default='17:00'),
        ),
        migrations.AddField(
            model_name='skill',
            name='available_days',
            field=models.CharField(default='1,2,3,4,5', max_length=100),
        ),
        migrations.AddField(
            model_name='skill',
            name='min_hours',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='skill',
            name='max_hours',
            field=models.IntegerField(default=8, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.CreateModel(
            name='SkillUnavailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('reason', models.CharField(choices=[('booked', 'Booked'), ('blocked', 'Blocked by Provider')], max_length=100)),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unavailable_slots', to='skills.skill')),
            ],
            options={
                'verbose_name_plural': 'Skill unavailabilities',
            },
        ),
    ]