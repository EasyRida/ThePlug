from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email_notifications',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='sms_notifications',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('es', 'Spanish'), ('fr', 'French')], default='en', max_length=2),
        ),
        migrations.AddField(
            model_name='customuser',
            name='timezone',
            field=models.CharField(choices=[('UTC', 'UTC'), ('US/Pacific', 'US/Pacific'), ('US/Eastern', 'US/Eastern'), ('Europe/London', 'Europe/London'), ('Asia/Dubai', 'Asia/Dubai')], default='UTC', max_length=50),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('provider', 'Skill Provider'), ('client', 'Skill Renter')], max_length=10),
        ),
    ]