# Generated by Django 3.2.3 on 2022-07-29 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_follow',
        ),
        migrations.RemoveConstraint(
            model_name='follow',
            name='prevent_self_follow',
        ),
    ]
