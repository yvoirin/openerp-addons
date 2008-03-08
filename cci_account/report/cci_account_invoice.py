##############################################################################
#
# Copyright (c) 2005-2006 TINY SPRL. (http://tiny.be) All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import time
from report import report_sxw
import pooler

class account_invoice_with_message(report_sxw.rml_parse):
	def __init__(self, cr, uid, name, context):
		super(account_invoice_with_message, self).__init__(cr, uid, name, context)
		self.localcontext.update({
			'time': time,
			'spcl_msg': self.spcl_msg,
		})

	def spcl_msg(self, form):
		return pooler.get_pool(self.cr.dbname).get('cci_account.message').browse(self.cr, self.uid, form['message']).name

report_sxw.report_sxw('report.cci_account.invoice', 'account.invoice', 'addons/cci_account/report/cci_account_invoice.rml', parser=account_invoice_with_message)