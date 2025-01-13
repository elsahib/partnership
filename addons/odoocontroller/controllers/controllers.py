# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import jwt
import datetime
import hashlib
from odoo.exceptions import AccessDenied
import json
import logging

_logger = logging.getLogger(__name__)

class AuthController(http.Controller):
    # Secret key for JWT signing - should be in config
    JWT_SECRET = 'your-secret-key'  # Move to secure configuration
    JWT_EXPIRATION = 24  # hours

    @http.route('/api/v1/auth/register', auth='public', methods=['POST'], csrf=False)
    def register(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            email = data.get('email')
            password = data.get('password')
            name = data.get('name')

            # Create new user
            user = request.env['res.users'].sudo().create({
                'name': name,
                'login': email,
                'password': password,  # Plain password, Odoo handles the hashing
            })
            
            return json.dumps({
                'status': 'success',
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.login
                }
            })
            
        except Exception as e:
            _logger.error(f"Error during registration: {str(e)}")  # Log the error
            return json.dumps({
                'status': 'error',
                'message': str(e)
            })

    @http.route('/api/v1/auth/login', auth='public', methods=['POST'], csrf=False)
    def login(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            email = data.get('email')
            password = data.get('password')
            
            # Get the database name
            db_name = request.env.cr.dbname
            
            # Authenticate using the built-in authenticate method
            uid = request.env['res.users'].authenticate(
                db_name,
                email,
                password,
                None  # Pass None if user_agent_env is not required
            )
            
            if not uid:
                return json.dumps({
                    'status': 'error',
                    'message': 'Invalid credentials'
                })
            
            # Get user record
            user = request.env['res.users'].sudo().browse(uid)
            
            # Generate JWT token
            token = self._generate_jwt(user)
            
            return json.dumps({
                'status': 'success',
                'token': token,
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.login
                }
            })
            
        except AccessDenied:
            return json.dumps({
                'status': 'error',
                'message': 'Invalid credentials'
            })
        except Exception as e:
            _logger.error(f"Error during login: {str(e)}")  # Log the error
            return json.dumps({
                'status': 'error',
                'message': str(e)
            })

    def _generate_jwt(self, user):
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=self.JWT_EXPIRATION),
            'iat': datetime.datetime.utcnow()
        }
        return jwt.encode(payload, self.JWT_SECRET, algorithm='HS256')

    @http.route('/api/v1/auth/verify', auth='public', methods=['GET'], csrf=False)
    def verify_token(self, **kwargs):
        auth_header = request.httprequest.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return json.dumps({
                'status': 'error',
                'message': 'No token provided'
            })

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, self.JWT_SECRET, algorithms=['HS256'])
            return json.dumps({
                'status': 'success',
                'valid': True
            })
        except jwt.ExpiredSignatureError:
            return json.dumps({
                'status': 'error',
                'message': 'Token has expired'
            })
        except jwt.InvalidTokenError:
            return json.dumps({
                'status': 'error',
                'message': 'Invalid token'
            })
        except Exception as e:
            _logger.error(f"Error during token verification: {str(e)}")  # Log the error
            return json.dumps({
                'status': 'error',
                'message': str(e)
            })


class EcommerceAPI(http.Controller):
    @http.route('/api/v1/products', auth='public', methods=['GET'], csrf=False)
    def get_products(self, **kwargs):
        products = request.env['product.template'].sudo().search([('website_published', '=', True)])
        product_list = []
        
        for product in products:
            product_list.append({
                'id': product.id,
                'name': product.name,
                'price': product.list_price,
                'description': product.description_sale,
                'image_url': f'/web/image/product.template/{product.id}/image_1024',
                'stock_quantity': product.qty_available
            })
            
        return json.dumps({'status': 'success', 'data': product_list})
    
    @http.route('/api/v1/orders', auth='user', methods=['POST'], csrf=False)
    def create_order(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            order = request.env['sale.order'].sudo().create({
                'partner_id': request.env.user.partner_id.id,
                'order_line': [(0, 0, {
                    'product_id': line['product_id'],
                    'product_uom_qty': line['quantity']
                }) for line in data.get('order_lines', [])]
            })
            
            return json.dumps({
                'status': 'success',
                'order_id': order.id,
                'amount_total': order.amount_total
            })
            
        except Exception as e:
            return json.dumps({'status': 'error', 'message': str(e)})
            
    @http.route('/api/v1/user/profile', auth='user', methods=['GET'], csrf=False)
    def get_user_profile(self, **kwargs):
        user = request.env.user
        return json.dumps({
            'status': 'success',
            'data': {
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'address': user.partner_id.street
            }
        })

       
class Odoocontroller(http.Controller):
    @http.route('/odooc', auth='public')
    def index(self, **kw): 
        _logger.info("Received a request") 
        _logger.info("Headers: %s", request.httprequest.headers) 
        _logger.info("Arguments: %s", kw) 
        return "Hello, there"

#     @http.route('/odoocontroller/odoocontroller/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoocontroller.listing', {
#             'root': '/odoocontroller/odoocontroller',
#             'objects': http.request.env['odoocontroller.odoocontroller'].search([]),
#         })

#     @http.route('/odoocontroller/odoocontroller/objects/<model("odoocontroller.odoocontroller"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoocontroller.object', {
#             'object': obj
#         })

