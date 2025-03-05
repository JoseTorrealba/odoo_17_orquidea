from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class UberDeliveryRequest(models.Model):
    _name = 'uber.delivery.request'
    _description = 'Uber Delivery Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char('Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    picking_id = fields.Many2one('stock.picking', 'Delivery Order', required=True)
    uber_delivery_id = fields.Char('Uber Delivery ID', readonly=True)
    
    # Delivery Information
    origin_address = fields.Text('Pickup Address', required=True)
    destination_address = fields.Text('Delivery Address', required=True)
    pickup_contact_name = fields.Char('Pickup Contact Name')
    pickup_contact_phone = fields.Char('Pickup Contact Phone')
    delivery_contact_name = fields.Char('Delivery Contact Name')
    delivery_contact_phone = fields.Char('Delivery Contact Phone')
    
    # Package Information
    package_size = fields.Selection([
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large')
    ], string='Package Size', required=True)
    package_weight = fields.Float('Weight (kg)')
    
    # Tracking
    tracking_url = fields.Char('Tracking URL', readonly=True)
    estimated_delivery_time = fields.Datetime('Estimated Delivery Time')
    actual_delivery_time = fields.Datetime('Actual Delivery Time')
    delivery_cost = fields.Float('Delivery Cost')
    currency_id = fields.Many2one('res.currency', string='Currency')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('uber.delivery.request') or _('New')
        return super().create(vals)

    def action_create_uber_delivery(self):
        self.ensure_one()
        if not self.env.company.uber_api_key:
            raise UserError(_('Uber API credentials are not configured.'))

        try:
            # Preparar datos para la API de Uber
            delivery_data = self._prepare_uber_delivery_data()
            
            # Llamar a la API de Uber
            response = self._call_uber_api('POST', '/v1/deliveries', delivery_data)
            
            if response.get('id'):
                self.write({
                    'uber_delivery_id': response['id'],
                    'state': 'confirmed',
                    'tracking_url': response.get('tracking_url'),
                    'estimated_delivery_time': response.get('estimated_delivery_time'),
                })
            else:
                raise UserError(_('Failed to create Uber delivery: %s') % response.get('error'))

        except Exception as e:
            raise UserError(_('Error creating Uber delivery: %s') % str(e))

    def _prepare_uber_delivery_data(self):
        return {
            'pickup': {
                'address': self.origin_address,
                'contact': {
                    'name': self.pickup_contact_name,
                    'phone': self.pickup_contact_phone,
                }
            },
            'dropoff': {
                'address': self.destination_address,
                'contact': {
                    'name': self.delivery_contact_name,
                    'phone': self.delivery_contact_phone,
                }
            },
            'package': {
                'size': self.package_size,
                'weight': self.package_weight,
            }
        }

    def _call_uber_api(self, method, endpoint, data=None):
        base_url = 'https://api.uber.com'
        headers = {
            'Authorization': f'Bearer {self.env.company.uber_api_key}',
            'Content-Type': 'application/json',
        }
        
        try:
            response = requests.request(
                method=method,
                url=f'{base_url}{endpoint}',
                headers=headers,
                data=json.dumps(data) if data else None
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            _logger.error('Uber API Error: %s', str(e))
            raise UserError(_('Error communicating with Uber API: %s') % str(e)) 