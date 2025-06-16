from django.db import migrations

def assign_user_order_numbers(apps, schema_editor):
    Order = apps.get_model('menu', 'Order')

    # Get all users who have orders
    user_ids = Order.objects.values_list('user', flat=True).distinct()

    for user_id in user_ids:
        # Get all orders for this user ordered by created time or id
        user_orders = Order.objects.filter(user_id=user_id).order_by('id')  # or 'created_at' if you have that

        # Assign incremental user_order_number starting at 1
        for i, order in enumerate(user_orders, start=1):
            if order.user_order_number != i:
                order.user_order_number = i
                order.save(update_fields=['user_order_number'])


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_order_user_order_number_alter_order_address_and_more'),
    ]

    operations = [
        migrations.RunPython(assign_user_order_numbers),
    ]
