# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2004-2008 TINY SPRL. (http://tiny.be) All Rights Reserved.
#
# $Id$
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

import wizard
import threading
import pooler

parameter_form = '''<?xml version="1.0"?>
<form string="Parameters" colspan="4">
    <label string="This wizard will schedule procurements." colspan="4" align="0.0"/>
</form>'''

parameter_fields = {
}

def _procure_calculation_procure(self, db_name, uid, data, context):
    db, pool = pooler.get_db_and_pool(db_name)
    cr = db.cursor()
    proc_obj = pool.get('mrp.procurement')
    proc_obj._procure_confirm(cr, uid, use_new_cursor=cr.dbname, context=context)
    return {}

def _procure_calculation(self, cr, uid, data, context):
    threaded_calculation = threading.Thread(target=_procure_calculation_procure, args=(self, cr.dbname, uid, data, context))
    threaded_calculation.start()
    return {}

class procurement_compute(wizard.interface):
    states = {
        'init': {
            'actions': [],
            'result': {'type': 'form', 'arch':parameter_form, 'fields': parameter_fields, 'state':[('end','Cancel'),('compute','Compute Procurements') ]}
        },
        'compute': {
            'actions': [_procure_calculation],
            'result': {'type': 'state', 'state':'end'}
        },
    }
procurement_compute('mrp.procurement.compute')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

