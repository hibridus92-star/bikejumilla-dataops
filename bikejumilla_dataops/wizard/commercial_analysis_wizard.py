from odoo import fields, models, _
from odoo.exceptions import ValidationError


class BikeJumillaCommercialAnalysisWizard(models.TransientModel):
    _name = "bikejumilla.commercial.analysis.wizard"
    _description = "BikeJumilla DataOps - Analizador comercial"

    date_from = fields.Date(string="Fecha inicial", required=True)
    date_to = fields.Date(string="Fecha final", required=True)
    salesperson_id = fields.Many2one("res.users", string="Comercial")
    partner_id = fields.Many2one("res.partner", string="Cliente")
    product_category_id = fields.Many2one("product.category", string="Categoría de producto")
    order_state = fields.Selection(
        [("draft", "Presupuesto"), ("sent", "Presupuesto enviado"), ("sale", "Pedido de venta"), ("done", "Bloqueado"), ("cancel", "Cancelado")],
        string="Estado",
    )
    min_amount = fields.Monetary(string="Importe mínimo", currency_field="currency_id", default=0.0)
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id, required=True, readonly=True)
    result_count = fields.Integer(string="N.º de operaciones", readonly=True)
    result_amount = fields.Monetary(string="Importe total", currency_field="currency_id", readonly=True)

    def _validate_parameters(self):
        self.ensure_one()
        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise ValidationError(_("La fecha inicial no puede ser posterior a la fecha final."))

    def _build_domain(self):
        """TODO RA3 / CE a-b: construir el dominio según los parámetros del wizard."""
        self.ensure_one()
        self._validate_parameters()
        return []

    def action_analyze(self):
        """TODO RA3 / CE a-b-h: consultar con ORM y presentar resultados."""
        self.ensure_one()
        self._validate_parameters()
        self.result_count = 0
        self.result_amount = 0.0
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("BikeJumilla DataOps"),
                "message": _("Esqueleto instalado. TODO: implementar la consulta del Analizador comercial."),
                "type": "warning",
                "sticky": False,
            },
        }

    def action_print_report(self):
        """TODO RA3 / CE c: preparar datos y lanzar el informe QWeb."""
        self.ensure_one()
        self._validate_parameters()
        return self.env.ref("bikejumilla_dataops.action_report_commercial_summary").report_action(self)
