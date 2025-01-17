# Generated by Django 2.2.13 on 2020-09-09 19:38

from django.db import migrations

def create_data(apps, schema_editor):
    Movies = apps.get_model('movie_rating', 'Movies')
    Movies(name="Black Panther", actor="Chadwick Boseman", director=" Ryan Coogler",
    description='TChalla, heir to the hidden but advanced kingdom of Wakanda, must step'+
     'forward to lead his people into a new future and must confront a challenger from his countrys past.',
    release_date='2001-12-12',
    image='https://m.media-amazon.com/images/M/MV5BMTg1MTY2MjYzNV5BMl5BanBnXkFtZTgwMTc4NTMwNDI@._V1_UX182_CR0,0,182,268_AL__QL50.jpg').save()


class Migration(migrations.Migration):

    dependencies = [
        ('movie_rating', '0003_auto_20200910_0055'),
    ]

    operations = [
        migrations.RunPython(create_data),
    ]
