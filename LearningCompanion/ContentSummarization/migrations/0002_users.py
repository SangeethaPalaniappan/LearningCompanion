from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ContentSummarization", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Users",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("user_name", models.CharField(max_length=150, unique=True)),
                ("mail_id", models.EmailField(max_length=254, unique=True)),
                ("password", models.CharField(max_length=128)),
            ],
            options={
                "db_table": "Users",
            },
        ),
    ]
