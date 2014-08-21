# -*- coding: utf-8 -*-
##############################################################################
#
#    Author Joel Grand-Guillaume. Copyright 2012 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.multi
    def _check_fiscal_year(self):
        for move in self:
            if move.journal_id.allow_date_fy:
                date_start = move.period_id.fiscalyear_id.date_start
                date_stop = move.period_id.fiscalyear_id.date_stop
                if not date_start <= move.date <= date_stop:
                    return False
        return True

    _constraints = [
        (_check_fiscal_year,
            'You cannot create entries with date not in the '
            'fiscal year of the chosen period',
            ['line_id']),
    ]
