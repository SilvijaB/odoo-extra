from openerp.osv import osv, fields
import collections
from openerp.tools.translate import _


class sale_order_line(osv.osv):
    _inherit = "sale.order.line"
    _name = "sale.order.line"

    def product_uom_change(self, cursor, user, ids, *args, **kwargs):
        res = super(sale_order_line, self).product_uom_change(cursor, user, ids, *args, **kwargs)
        if 'value' in res:
            if 'name' in res['value']:
                res['value'].pop('name', None)
        print res
        return res

sale_order_line()


class account_invoice(osv.osv):
    _inherit = "account.invoice"
    _name = "account.invoice"

    def write(self, cr, uid, ids, values, context = None):
        if ids == []:
            return super(account_invoice, self).write(cr, uid, ids, values, context)
        if isinstance(ids, collections.Iterable):
            ids = ids[0]
        if 'date_invoice' in values:
            period = self.browse(cr, uid, ids, context).period_id.with_context(context).find(values['date_invoice'])[:1]
            values.update({'period_id': period.id})
            if values['date_invoice'] == False:
                values.update({'period_id': False})
        if 'period_id' in values and values['period_id'] != False:
            dates = self.pool.get('account.period').read(cr, uid, values['period_id'], ['date_start','date_stop'])
            if 'date_invoice' in values:
                date_invoice = values['date_invoice']
            else:
                date_invoice = self.read(cr, uid, ids, ['date_invoice'])['date_invoice']
            if date_invoice != False and dates['date_start'] <= date_invoice and dates['date_stop'] >= date_invoice:
                pass
            elif date_invoice != False:
                raise osv.except_osv(_('Error!'),_('Invoice Date must belong to the period!'))
        return super(account_invoice, self).write(cr, uid, ids, values, context)

account_invoice()



from openerp import models, api

class FooterlessNotification(models.Model):
    _inherit = 'mail.notification'

    @api.model
    def get_signature_footer(self, user_id, res_model=None, res_id=None, context=None, user_signature=True):
        return ""



class mail_mail(osv.Model):
    """ Update of mail_mail class, to add the signin URL to notifications. """
    _inherit = 'mail.mail'

    def _get_partner_access_link(self, cr, uid, mail, partner=None, context=None):
        """ Generate URLs for links in mails:
            - partner is not an user: signup_url
            - partner is an user: fallback on classic URL
        """
        return ""

