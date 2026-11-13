import logging

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
        help="TODO alumno: decidir qué indicador empresarial representa este campo.",
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
        """Punto de entrada de la acción planificada.

        TODO RA3 / CE e:
        - Definir el periodo que debe analizarse.
        - Consultar los datos mediante el ORM de Odoo.
        - Calcular los indicadores necesarios.
        - Crear un nuevo registro bikejumilla.dataops.snapshot.
        - Gestionar y documentar las incidencias relevantes.
        """
        _logger.info("BikeJumilla DataOps: cron ejecutado. TODO: implementar la extracción automática.")
        return True
