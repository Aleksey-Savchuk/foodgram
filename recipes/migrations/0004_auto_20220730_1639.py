# Generated by Django 3.2.3 on 2022-07-30 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20220730_1628'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favorite',
            name='unique_favorite',
        ),
        migrations.RemoveConstraint(
            model_name='favorite',
            name='prevent_self_favorite',
        ),
    ]
