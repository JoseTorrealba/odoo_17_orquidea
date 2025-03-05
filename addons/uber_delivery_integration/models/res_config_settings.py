from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    uber_api_key = fields.Char(
        string='Uber API Key',
        config_parameter='uber_delivery_integration.api_key'
    )
    uber_client_id = fields.Char(
        string='Uber Client ID',
        config_parameter='uber_delivery_integration.client_id'
    )
    uber_client_secret = fields.Char(
        string='Uber Client Secret',
        config_parameter='uber_delivery_integration.client_secret'
    )
    uber_sandbox_mode = fields.Boolean(
        string='Sandbox Mode',
        config_parameter='uber_delivery_integration.sandbox_mode'
    ) 