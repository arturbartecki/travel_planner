# Generated by Django 2.1.7 on 2019-02-14 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TripDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('content', models.TextField()),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trip.Trip')),
            ],
            options={
                'ordering': ('trip', 'order'),
                'abstract': False,
            },
        ),
    ]
