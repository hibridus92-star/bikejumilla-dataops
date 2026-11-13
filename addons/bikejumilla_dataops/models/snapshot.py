import logging
from datetime import timedelta

from odoo import fields, models

_logger = logging.getLogger(__name__)


class BikeJumillaDataOpsSnapshot(models.Model):
    _name = "bikejumilla.dataops.snapshot"
    _description = "BikeJumilla DataOps - Snapshot de indicadores"
    _order = "execution_datetime desc, id desc"

    name = fields.Char(string="Referencia", required=True, default="Snapshot pendiente")
    execution_datetime = fields.Datetime(string="Fecha y hora de ejecución", default=fields.Datetime.now, required=True, readonly=True)
    date_from = fields.Date(string="Desde")
    date_to = fields.Date(string="Hasta")
    total_operations = fields.Integer(string="N.º de operaciones", readonly=True)
    amount_total = fields.Monetary(string="Importe total", currency_field="currency_id", readonly=True)
    extra_metric = fields.Float(
        string="Indicador adicional",
        readonly=True,
        help="Indicador empresarial (Ticket medio por operación).",
    )
    currency_id = fields.Many2one(
        "res.currency", string="Moneda", default=lambda self: self.env.company.currency_id, required=True, readonly=True
    )
    state = fields.Selection(
        [("draft", "Pendiente"), ("done", "Correcto"), ("error", "Error")],
        string="Estado", default="draft", required=True, readonly=True,
    )
    notes = fields.Text(string="Observaciones", readonly=True)

    def _cron_generate_snapshot(self):
        """Punto de entrada de la acción planificada."""
        _logger.info("BikeJumilla DataOps: Iniciando generación de snapshot.")
        
        # 1. Definimos el periodo (últimos 30 días)
        today = fields.Date.today()
        date_from = today - timedelta(days=30)
        date_to = today
        
        # 2. Consultamos los pedidos de venta confirmados en ese periodo
        domain = [
            ('date_order', '>=', date_from),
            ('date_order', '<=', date_to),
            ('state', '=', 'sale')
        ]
        pedidos = self.env['sale.order'].search(domain)
        
        # 3. Calculamos las métricas
        total_ops = len(pedidos)
        total_amount = sum(pedidos.mapped('amount_total'))
        # Indicador adicional: ticket medio
        avg_ticket = total_amount / total_ops if total_ops > 0 else 0.0
        
        # 4. Creamos el registro snapshot
        self.create({
            'name': f"Snapshot {today.strftime('%Y-%m-%d')}",
            'date_from': date_from,
            'date_to': date_to,
            'total_operations': total_ops,
            'amount_total': total_amount,
            'extra_metric': avg_ticket,
            'state': 'done',
            'notes': f"Generado automáticamente. Pedidos confirmados en los últimos 30 días."
        })
        
        _logger.info(f"BikeJumilla DataOps: Snapshot generado. {total_ops} operaciones, {total_amount} €.")
        return True