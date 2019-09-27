from encore_base_action_test_case import EncoreBaseActionTestCase

from get_zone_dns_records import GetZoneDNSRecords
from st2common.runners.base_action import Action

import mock
import requests


class GetZoneDNSRecordsTestCase(EncoreBaseActionTestCase):
    __test__ = True
    action_cls = GetZoneDNSRecords

    def _mock_response(self, status=200, content="CONTENT", json_data=None, raise_for_status=None):
        """Since we will be makeing alot of rest calls that
        all raise for status, we are creating this helper
        method to build the mock reponse for us to reduce
        duplicated code.
        """
        mock_resp = mock.Mock()
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        mock_resp.status_code = status
        mock_resp.content = content
        if json_data:
            mock_resp.json = mock.Mock(
                return_value=json_data
            )
        return mock_resp

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, GetZoneDNSRecords)
        self.assertIsInstance(action, Action)

    @mock.patch('get_zone_dns_records.GetZoneDNSRecords.mm_build_client')
    def test_get_dns_zone_success(self, mock_client):
        action = self.get_action_instance(self.config_good)
        connection_name = 'base'
        connection_config = self.config_good['menandmice'][connection_name]
        test_dict = {"url": connection_config['server'],
                     "dns_domain": "test.name"}
        expected_ref = "test_ref"
        expected_json = {'result': {'dnsZones': [{'ref': expected_ref}]}}
        mock_response = self._mock_response(json_data=expected_json)
        mock_client.get.return_value = mock_response
        result = action.get_dns_zone(test_dict['url'], mock_client, test_dict['dns_domain'])
        mock_client.get.assert_called_with("abc/DNSZones?filter=type:^Master$ name:^test.name.$")
        self.assertEqual(result, expected_ref)

    @mock.patch('get_zone_dns_records.GetZoneDNSRecords.mm_build_client')
    def test_get_dns_zone_error(self, mock_client):
        action = self.get_action_instance(self.config_good)
        connection_name = 'base'
        connection_config = self.config_good['menandmice'][connection_name]
        test_dict = {"url": connection_config['server'],
                     "dns_domain": "test.name"}
        mock_response = self._mock_response(status=404,
                            raise_for_status=requests.exceptions.HTTPError("Unknown Site"))
        mock_client.get.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError) as context:
            action.get_dns_zone(test_dict['url'], mock_client, test_dict['dns_domain'])

        mock_client.get.assert_called_with("abc/DNSZones?filter=type:^Master$ name:^test.name.$")
        self.assertTrue('Unknown Site' in context.exception)

    @mock.patch('get_zone_dns_records.GetZoneDNSRecords.mm_build_client')
    def test_get_dns_records_success(self, mock_client):
        action = self.get_action_instance(self.config_good)
        connection_name = 'base'
        connection_config = self.config_good['menandmice'][connection_name]
        test_dict = {"url": connection_config['server'],
                     "dns_zone_ref": "test/123"}
        expected_ref = [{'ref': 'test'}]
        expected_json = {'result': {'dnsRecords': expected_ref}}
        mock_response = self._mock_response(json_data=expected_json)
        mock_client.get.return_value = mock_response
        result = action.get_dns_records(test_dict['url'], mock_client, test_dict['dns_zone_ref'])
        mock_client.get.assert_called_with("abc/test/123/DNSRecords?filter=type:^A$")
        self.assertEqual(result, expected_ref)

    @mock.patch('get_zone_dns_records.GetZoneDNSRecords.mm_build_client')
    def test_get_dns_records_error(self, mock_client):
        action = self.get_action_instance(self.config_good)
        connection_name = 'base'
        connection_config = self.config_good['menandmice'][connection_name]
        test_dict = {"url": connection_config['server'],
                     "dns_zone_ref": "test/123"}
        mock_response = self._mock_response(status=404,
                            raise_for_status=requests.exceptions.HTTPError("Unknown Site"))
        mock_client.get.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError) as context:
            action.get_dns_records(test_dict['url'], mock_client, test_dict['dns_zone_ref'])

        mock_client.get.assert_called_with("abc/test/123/DNSRecords?filter=type:^A$")
        self.assertTrue('Unknown Site' in context.exception)

    @mock.patch('get_zone_dns_records.GetZoneDNSRecords.mm_build_client')
    def test_resolve_fqdn_success(self, mock_client):
        action = self.get_action_instance(self.config_good)
        connection_name = 'base'
        connection_config = self.config_good['menandmice'][connection_name]
        test_dict = {"url": connection_config['server'],
                     "dns_record": {'ref': 'test/123',
                                    'name': 'test_name',
                                    'dnsZoneRef': 'test/5'}}
        expected_result = "test_name.domain.tld"
        expected_json = {'result': {'dnsZone': {'name': 'domain.tld'}}}
        mock_response = self._mock_response(json_data=expected_json)
        mock_client.get.return_value = mock_response
        result = action.resolve_fqdn(test_dict['url'], mock_client, test_dict['dns_record'])
        mock_client.get.assert_called_with("abc/test/5")
        self.assertEqual(result, expected_result)

    @mock.patch('get_zone_dns_records.GetZoneDNSRecords.mm_build_client')
    def test_resolve_fqdn_success_extra(self, mock_client):
        action = self.get_action_instance(self.config_good)
        connection_name = 'base'
        connection_config = self.config_good['menandmice'][connection_name]
        test_dict = {"url": connection_config['server'],
                     "dns_record": {'ref': 'test/123',
                                    'name': 'test_name',
                                    'dnsZoneRef': 'test/5'}}
        expected_result = "test_name.domain.tld"
        expected_json = {'result': {'dnsZone': {'name': 'domain.tld.'}}}
        mock_response = self._mock_response(json_data=expected_json)
        mock_client.get.return_value = mock_response
        result = action.resolve_fqdn(test_dict['url'], mock_client, test_dict['dns_record'])
        mock_client.get.assert_called_with("abc/test/5")
        self.assertEqual(result, expected_result)

    @mock.patch('get_zone_dns_records.GetZoneDNSRecords.mm_build_client')
    def test_resolve_fqdn_error(self, mock_client):
        action = self.get_action_instance(self.config_good)
        connection_name = 'base'
        connection_config = self.config_good['menandmice'][connection_name]
        test_dict = {"url": connection_config['server'],
                     "dns_record": {'ref': 'test/123',
                                    'name': 'test_name',
                                    'dnsZoneRef': 'test/5'}}
        mock_response = self._mock_response(status=404,
                            raise_for_status=requests.exceptions.HTTPError("Unknown Site"))
        mock_client.get.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError) as context:
            action.resolve_fqdn(test_dict['url'], mock_client, test_dict['dns_record'])

        mock_client.get.assert_called_with("abc/test/5")
        self.assertTrue('Unknown Site' in context.exception)

    @mock.patch('get_zone_dns_records.GetZoneDNSRecords.resolve_fqdn')
    @mock.patch('get_zone_dns_records.GetZoneDNSRecords.mm_build_client')
    def test_get_dns_related_records_success(self, mock_client, mock_fqdn):
        action = self.get_action_instance(self.config_good)
        connection_name = 'base'
        connection_config = self.config_good['menandmice'][connection_name]
        test_dict = {"url": connection_config['server'],
                     "dns_record_ref": "test/123"}
        expected_records = [{'ref': 'test'}]
        expected_result = [{'ref': 'test',
                            'name_fqdn': 'test.domain.tld'}]
        expected_json = {'result': {'dnsRecords': expected_records}}
        mock_response = self._mock_response(json_data=expected_json)
        mock_client.get.return_value = mock_response
        mock_fqdn.return_value = 'test.domain.tld'
        result = action.get_dns_related_records(test_dict['url'],
                                                mock_client,
                                                test_dict['dns_record_ref'])
        mock_client.get.assert_called_with("abc/test/123/RelatedDNSRecords")
        self.assertEqual(result, expected_result)

    @mock.patch('get_zone_dns_records.GetZoneDNSRecords.mm_build_client')
    def test_get_dns_related_records_none(self, mock_client):
        action = self.get_action_instance(self.config_good)
        connection_name = 'base'
        connection_config = self.config_good['menandmice'][connection_name]
        test_dict = {"url": connection_config['server'],
                     "dns_record_ref": "test/123"}
        expected_records = []
        expected_json = {'result': {'dnsRecords': expected_records}}
        mock_response = self._mock_response(json_data=expected_json)
        mock_client.get.return_value = mock_response
        result = action.get_dns_related_records(test_dict['url'],
                                                mock_client,
                                                test_dict['dns_record_ref'])
        mock_client.get.assert_called_with("abc/test/123/RelatedDNSRecords")
        self.assertEqual(result, expected_records)

    @mock.patch('get_zone_dns_records.GetZoneDNSRecords.mm_build_client')
    def test_get_dns_related_records_error(self, mock_client):
        action = self.get_action_instance(self.config_good)
        connection_name = 'base'
        connection_config = self.config_good['menandmice'][connection_name]
        test_dict = {"url": connection_config['server'],
                     "dns_record_ref": "test/123"}
        mock_response = self._mock_response(status=404,
                            raise_for_status=requests.exceptions.HTTPError("Unknown Site"))
        mock_client.get.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError) as context:
            action.get_dns_related_records(test_dict['url'],
                                           mock_client,
                                           test_dict['dns_record_ref'])

        mock_client.get.assert_called_with("abc/test/123/RelatedDNSRecords")
        self.assertTrue('Unknown Site' in context.exception)

    @mock.patch('get_zone_dns_records.GetZoneDNSRecords.get_dns_related_records')
    @mock.patch('get_zone_dns_records.GetZoneDNSRecords.mm_build_client')
    def test_get_build_dns_information(self, mock_client, mock_get_dns_related_records):
        action = self.get_action_instance(self.config_good)
        connection_name = 'base'
        connection_config = self.config_good['menandmice'][connection_name]
        test_dict = {"url": connection_config['server'],
                     "dns_records": [{'ref': 'test/123',
                                    'name': 'test_name',
                                    'dnsZoneRef': 'test/5'}],
                     "dns_domain": "domain.tld"}
        expected_related_records = [{'name': 'test_name_2'}]
        expected_result = {
            'test_name.domain.tld': {
                'ref': 'test/123',
                'name': 'test_name',
                'dnsZoneRef': 'test/5',
                'related_records': expected_related_records
            }
        }
        mock_get_dns_related_records.return_value = expected_related_records
        result = action.build_dns_information(test_dict['url'],
                                              mock_client,
                                              test_dict['dns_records'],
                                              test_dict['dns_domain'])
        self.assertEqual(result, expected_result)

    @mock.patch('get_zone_dns_records.GetZoneDNSRecords.get_dns_related_records')
    @mock.patch('get_zone_dns_records.GetZoneDNSRecords.mm_build_client')
    def test_get_build_dns_information_no_related(self, mock_client, mock_get_dns_related_records):
        action = self.get_action_instance(self.config_good)
        connection_name = 'base'
        connection_config = self.config_good['menandmice'][connection_name]
        test_dict = {"url": connection_config['server'],
                     "dns_records": [{'ref': 'test/123',
                                    'name': 'test_name',
                                    'dnsZoneRef': 'test/5'}],
                     "dns_domain": "domain.tld"}
        expected_related_records = []
        expected_result = {
            'test_name.domain.tld': {
                'ref': 'test/123',
                'name': 'test_name',
                'dnsZoneRef': 'test/5',
                'related_records': expected_related_records
            }
        }
        mock_get_dns_related_records.return_value = expected_related_records
        result = action.build_dns_information(test_dict['url'],
                                              mock_client,
                                              test_dict['dns_records'],
                                              test_dict['dns_domain'])
        self.assertEqual(result, expected_result)

    @mock.patch('get_zone_dns_records.GetZoneDNSRecords.mm_build_client')
    def test_get_build_dns_information_none(self, mock_client):
        action = self.get_action_instance(self.config_good)
        connection_name = 'base'
        connection_config = self.config_good['menandmice'][connection_name]
        test_dict = {"url": connection_config['server'],
                     "dns_records": [],
                     "dns_domain": "domain.tld"}
        expected_result = {}
        result = action.build_dns_information(test_dict['url'],
                                              mock_client,
                                              test_dict['dns_records'],
                                              test_dict['dns_domain'])
        self.assertEqual(result, expected_result)

    @mock.patch("get_zone_dns_records.GetZoneDNSRecords.build_dns_information")
    @mock.patch("get_zone_dns_records.GetZoneDNSRecords.get_dns_records")
    @mock.patch("get_zone_dns_records.GetZoneDNSRecords.get_dns_zone")
    @mock.patch('get_zone_dns_records.GetZoneDNSRecords.mm_build_client')
    def test_run(self,
                 mock_build_client,
                 mock_get_dns_zone,
                 mock_get_dns_records,
                 mock_build_dns_information):
        action = self.get_action_instance({})
        test_dict = {"dns_domain": "test.local"}
        client = "client"
        url = "url"
        dns_zone_ref = "test/4"
        dns_records = [{'name': 'test_name',
                        'ref': 'test/123'}]
        expected_result = {
            'test_name.test.local': {
                'name': 'test_name',
                'ref': 'test/123'
            }
        }

        mock_build_client.return_value = (url, client)
        mock_get_dns_zone.return_value = dns_zone_ref
        mock_get_dns_records.return_value = dns_records
        mock_build_dns_information.return_value = expected_result

        result = action.run(**test_dict)
        self.assertEqual(result, expected_result)
