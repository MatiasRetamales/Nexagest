import uuid
from django.db import migrations


def backfill_tokens(apps, schema_editor):
    Pedido = apps.get_model('pedidos', 'Pedido')
    for pedido in Pedido.objects.filter(token_seguimiento__isnull=True):
        pedido.token_seguimiento = uuid.uuid4()
        pedido.save(update_fields=['token_seguimiento'])
    # Handle any duplicated non-null values as well
    seen = set()
    for pedido in Pedido.objects.exclude(token_seguimiento__isnull=True).order_by('id'):
        if pedido.token_seguimiento in seen:
            pedido.token_seguimiento = uuid.uuid4()
            pedido.save(update_fields=['token_seguimiento'])
        else:
            seen.add(pedido.token_seguimiento)


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0010_pedido_estado_pago_pedido_token_seguimiento'),
    ]

    operations = [
        migrations.RunPython(backfill_tokens, migrations.RunPython.noop),
    ]
