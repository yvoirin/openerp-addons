import random
import uuid
import simplejson

import werkzeug.exceptions

from openerp import SUPERUSER_ID
from openerp.osv import osv
from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.addons.website.models import website

class sale_quote(http.Controller):

    def get_quote(self, token):
        quote_pool = request.registry.get('sale.quote')
        quote_id = quote_pool.search(request.cr, SUPERUSER_ID, [('access_token', '=', token)], context=request.context)
        return quote_id
        
    @website.route(['/quote/<token>'], type='http', auth="public")
    def view(self, token=None, **post):
        values = {}
        # http://hostname:8069/quote?id=
        quote_pool = request.registry.get('sale.quote')
        quotation = quote_pool.browse(request.cr, SUPERUSER_ID, self.get_quote(token))[0]
        values.update({
            'quotation' : quotation,
        })
        return request.website.render('website_sale_quote.quotation', values)

    @website.route(['/quote/<token>/accept'], type='http', auth="public")
    def accept(self, token=None , **post):
        values = {}
        quotation = request.registry.get('sale.quote').write(request.cr, SUPERUSER_ID, self.get_quote(token), {'state': 'accept'})
        return request.redirect("/quote/%s" % token)

    @website.route(['/quote/<token>/decline'], type='http', auth="public")
    def decline(self, token=None , **post):
        values = {}
        quotation = request.registry.get('sale.quote').write(request.cr, SUPERUSER_ID, self.get_quote(token), {'state': 'cancel'})
        return request.redirect("/quote/%s" % token)

    @website.route(['/quote/<token>/post'], type='http', auth="public")
    def post(self, token=None, **post):
        values = {}
        if post.get('new_message'):
            request.session.body = post.get('new_message')
        if 'body' in request.session and request.session.body:
            request.registry.get('sale.quote').message_post(request.cr, SUPERUSER_ID, self.get_quote(token),
                    body=request.session.body,
                    type='comment',
                    subtype='mt_comment',
                )
            request.session.body = False
        return request.redirect("/quote/%s" % token)


