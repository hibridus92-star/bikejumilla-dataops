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
        """Construye el dominio según los parámetros del wizard."""
        self.ensure_one()
        self._validate_parameters()
        
        domain = [('date_order', '>=', self.date_from), ('date_order', '<=', self.date_to)]
        
        if self.salesperson_id:
            domain.append(('user_id', '=', self.salesperson_id.id))
        if self.partner_id:
            domain.append(('partner_id', '=', self.partner_id.id))
        if self.order_state:
            domain.append(('state', '=', self.order_state))
        if self.min_amount > 0:
            domain.append(('amount_total', '>=', self.min_amount))
            
        return domain

    def action_analyze(self):
        """Consulta con ORM y presenta resultados."""
        self.ensure_one()
        self._validate_parameters()
        
        # 1. Buscamos los pedidos según el dominio
        pedidos = self.env['sale.order'].search(self._build_domain())
        
        # 2. Calculamos los totales
        self.result_count = len(pedidos)
        self.result_amount = sum(pedidos.mapped('amount_total'))
        
        # 3. Devolvemos una notificación con el resultado
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Análisis completado"),
                "message": _("Se han encontrado %s operaciones por un importe de %s €.") % (self.result_count, self.result_amount),
                "type": "success",
                "sticky": False,
            },
        }

    def action_print_report(self):
        """TODO RA3 / CE c: preparar datos y lanzar el informe QWeb."""
        self.ensure_one()
        self._validate_parameters()
        return self.env.ref("bikejumilla_dataops.action_report_commercial_summary").report_action(self)