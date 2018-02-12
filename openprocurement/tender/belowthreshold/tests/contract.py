# -*- coding: utf-8 -*-
import unittest

from openprocurement.api.tests.base import snitch

from openprocurement.tender.belowthreshold.tests.base import (
    TenderContentWebTest,
    test_bids,
    test_lots,
    test_organization,
    test_tender_data
)
from openprocurement.tender.belowthreshold.tests.contract_blanks import (
    # TenderContractResourceTest
    create_tender_contract_invalid,
    create_tender_contract,
    create_tender_contract_in_complete_status,
    patch_tender_contract,
    patch_tender_contract_item,
    get_tender_contract,
    get_tender_contracts,
    # Tender2LotContractResourceTest
    lot2_patch_tender_contract,
    # TenderContractDocumentResourceTest
    not_found,
    create_tender_contract_document,
    create_update_contract_document,
    put_tender_contract_document,
    patch_tender_contract_document,
    # Tender2LotContractDocumentResourceTest
    lot2_create_tender_contract_document,
    lot2_put_tender_contract_document,
    lot2_patch_tender_contract_document,
    # TenderContractChangeStatusTest
    patch_tender_contract_pending_signed_status,

)


class TenderContractResourceTestMixin(object):
    test_create_tender_contract_invalid = snitch(create_tender_contract_invalid)
    test_get_tender_contract = snitch(get_tender_contract)
    test_get_tender_contracts = snitch(get_tender_contracts)


class TenderContractDocumentResourceTestMixin(object):
    test_not_found = snitch(not_found)
    test_create_tender_contract_document = snitch(create_tender_contract_document)
    test_put_tender_contract_document = snitch(put_tender_contract_document)
    test_patch_tender_contract_document = snitch(patch_tender_contract_document)


class TenderContractResourceTest(TenderContentWebTest, TenderContractResourceTestMixin):
    initial_status = 'active.qualification'
    initial_bids = test_bids

    def setUp(self):
        super(TenderContractResourceTest, self).setUp()
        # Create award
        auth = self.app.authorization
        self.app.authorization = ('Basic', ('token', ''))
        response = self.app.post_json('/tenders/{}/awards'.format(
            self.tender_id), {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': self.initial_bids[0]['id'], 'value': self.initial_data["value"], 'items': self.initial_data["items"]}})
        self.app.authorization = auth
        award = response.json['data']
        self.award_id = award['id']
        self.award_value = award['value']
        self.award_suppliers = award['suppliers']
        self.award_items = award['items']
        response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, self.award_id, self.tender_token), {"data": {"status": "active"}})

    test_create_tender_contract = snitch(create_tender_contract)
    test_create_tender_contract_in_complete_status = snitch(create_tender_contract_in_complete_status)
    test_patch_tender_contract = snitch(patch_tender_contract)
    test_patch_tender_contract_item = snitch(patch_tender_contract_item)
    test_patch_tender_contract_pending_signed_status = snitch(patch_tender_contract_pending_signed_status)


class Tender2LotContractResourceTest(TenderContentWebTest):
    initial_status = 'active.qualification'
    initial_bids = test_bids
    initial_lots = 2 * test_lots

    def setUp(self):
        super(Tender2LotContractResourceTest, self).setUp()
        # Create award

        auth = self.app.authorization
        self.app.authorization = ('Basic', ('token', ''))
        response = self.app.post_json('/tenders/{}/awards'.format(self.tender_id), {'data': {
            'suppliers': [test_organization],
            'status': 'pending',
            'bid_id': self.initial_bids[0]['id'],
            'lotID': self.initial_lots[0]['id']
        }})
        award = response.json['data']
        self.award_id = award['id']
        self.app.authorization = auth
        self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, self.award_id, self.tender_token), {"data": {"status": "active"}})

    test_lot2_patch_tender_contract = snitch(lot2_patch_tender_contract)


class TenderContractDocumentResourceTest(TenderContentWebTest, TenderContractDocumentResourceTestMixin):
    initial_status = 'active.qualification'
    initial_bids = test_bids

    def setUp(self):
        super(TenderContractDocumentResourceTest, self).setUp()
        # Create award
        auth = self.app.authorization
        self.app.authorization = ('Basic', ('token', ''))

        response = self.app.post_json('/tenders/{}/awards'.format(
            self.tender_id), {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': self.initial_bids[0]['id']}})
        award = response.json['data']
        self.award_id = award['id']

        self.app.authorization = auth
        response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, self.award_id, self.tender_token), {"data": {"status": "active"}})

        # Create contract for award
        auth = self.app.authorization
        self.app.authorization = ('Basic', ('token', ''))

        response = self.app.post_json('/tenders/{}/contracts'.format(self.tender_id), {'data': {'title': 'contract title', 'description': 'contract description', 'awardID': self.award_id}})
        contract = response.json['data']
        self.contract_id = contract['id']
        self.app.authorization = auth

    test_create_update_contract_document = snitch(create_update_contract_document)


class Tender2LotContractDocumentResourceTest(TenderContentWebTest):
    initial_status = 'active.qualification'
    initial_bids = test_bids
    initial_lots = 2 * test_lots

    def setUp(self):
        super(Tender2LotContractDocumentResourceTest, self).setUp()
        # Create award
        auth = self.app.authorization
        self.app.authorization = ('Basic', ('token', ''))

        response = self.app.post_json('/tenders/{}/awards'.format(self.tender_id), {'data': {
            'suppliers': [test_organization],
            'status': 'pending',
            'bid_id': self.initial_bids[0]['id'],
            'lotID': self.initial_lots[0]['id']
        }})
        award = response.json['data']
        self.award_id = award['id']

        self.app.authorization = auth
        self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, self.award_id, self.tender_token), {"data": {"status": "active"}})
        # Create contract for award

        self.app.authorization = ('Basic', ('token', ''))
        response = self.app.post_json('/tenders/{}/contracts'.format(self.tender_id), {'data': {'title': 'contract title', 'description': 'contract description', 'awardID': self.award_id}})
        contract = response.json['data']
        self.contract_id = contract['id']
        self.app.authorization = auth

    lot2_create_tender_contract_document = snitch(lot2_create_tender_contract_document)
    lot2_put_tender_contract_document = snitch(lot2_put_tender_contract_document)
    lot2_patch_tender_contract_document = snitch(lot2_patch_tender_contract_document)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TenderContractResourceTest))
    suite.addTest(unittest.makeSuite(TenderContractDocumentResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
