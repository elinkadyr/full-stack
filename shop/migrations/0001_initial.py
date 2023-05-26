# Generated by Django 4.2.1 on 2023-05-26 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('size', models.CharField(choices=[('s', 'small'), ('m', 'medium'), ('l', 'large')], max_length=50)),
                ('color', models.CharField(choices=[('red', 'red'), ('blue', 'blue'), ('green', 'green'), ('yellow', 'yellow'), ('brown', 'brown'), ('black', 'black'), ('white', 'white'), ('gray', 'gray')], max_length=50)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=50)),
                ('quantity', models.IntegerField()),
                ('image1', models.ImageField(blank=True, null=True, upload_to='shop/')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='shop/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.category')),
            ],
        ),
    ]
