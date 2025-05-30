# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from unittest import mock

from openstack.config import cloud_region

from os_client_config import cloud_config
from os_client_config import defaults
from os_client_config.tests import base


fake_config_dict = {'a': 1, 'os_b': 2, 'c': 3, 'os_c': 4}
fake_services_dict = {
    'compute_api_version': '2',
    'compute_endpoint_override': 'http://compute.example.com',
    'telemetry_endpoint': 'http://telemetry.example.com',
    'interface': 'public',
    'image_service_type': 'mage',
    'identity_interface': 'admin',
    'identity_service_name': 'locks',
    'volume_api_version': '1',
    'auth': {'password': 'hunter2', 'username': 'AzureDiamond'},
}


class TestCloudConfig(base.TestCase):
    @mock.patch.object(cloud_region.CloudRegion, 'get_api_version')
    @mock.patch.object(cloud_region.CloudRegion, 'get_auth_args')
    @mock.patch.object(cloud_region.CloudRegion, 'get_session_endpoint')
    def test_legacy_client_object_store_password(
        self,
        mock_get_session_endpoint,
        mock_get_auth_args,
        mock_get_api_version,
    ):
        mock_client = mock.Mock()
        mock_get_session_endpoint.return_value = 'http://swift.example.com'
        mock_get_api_version.return_value = '3'
        mock_get_auth_args.return_value = dict(
            username='testuser',
            password='testpassword',
            project_name='testproject',
            auth_url='http://example.com',
        )
        config_dict = defaults.get_defaults()
        config_dict.update(fake_services_dict)
        cc = cloud_config.CloudConfig(
            "test1", "region-al", config_dict, auth_plugin=mock.Mock()
        )
        cc.get_legacy_client('object-store', mock_client)
        mock_client.assert_called_with(
            session=mock.ANY,
            os_options={
                'region_name': 'region-al',
                'service_type': 'object-store',
                'object_storage_url': None,
                'endpoint_type': 'public',
            },
        )

    @mock.patch.object(cloud_region.CloudRegion, 'get_auth_args')
    @mock.patch.object(cloud_region.CloudRegion, 'get_session_endpoint')
    def test_legacy_client_object_store_password_v2(
        self, mock_get_session_endpoint, mock_get_auth_args
    ):
        mock_client = mock.Mock()
        mock_get_session_endpoint.return_value = 'http://swift.example.com'
        mock_get_auth_args.return_value = dict(
            username='testuser',
            password='testpassword',
            project_name='testproject',
            auth_url='http://example.com',
        )
        config_dict = defaults.get_defaults()
        config_dict.update(fake_services_dict)
        cc = cloud_config.CloudConfig(
            "test1", "region-al", config_dict, auth_plugin=mock.Mock()
        )
        cc.get_legacy_client('object-store', mock_client)
        mock_client.assert_called_with(
            session=mock.ANY,
            os_options={
                'region_name': 'region-al',
                'service_type': 'object-store',
                'object_storage_url': None,
                'endpoint_type': 'public',
            },
        )

    @mock.patch.object(cloud_region.CloudRegion, 'get_auth_args')
    @mock.patch.object(cloud_region.CloudRegion, 'get_session_endpoint')
    def test_legacy_client_object_store(
        self, mock_get_session_endpoint, mock_get_auth_args
    ):
        mock_client = mock.Mock()
        mock_get_session_endpoint.return_value = 'http://example.com/v2'
        mock_get_auth_args.return_value = {}
        config_dict = defaults.get_defaults()
        config_dict.update(fake_services_dict)
        cc = cloud_config.CloudConfig(
            "test1", "region-al", config_dict, auth_plugin=mock.Mock()
        )
        cc.get_legacy_client('object-store', mock_client)
        mock_client.assert_called_with(
            session=mock.ANY,
            os_options={
                'region_name': 'region-al',
                'service_type': 'object-store',
                'object_storage_url': None,
                'endpoint_type': 'public',
            },
        )

    @mock.patch.object(cloud_region.CloudRegion, 'get_auth_args')
    @mock.patch.object(cloud_region.CloudRegion, 'get_session_endpoint')
    def test_legacy_client_object_store_timeout(
        self, mock_get_session_endpoint, mock_get_auth_args
    ):
        mock_client = mock.Mock()
        mock_get_session_endpoint.return_value = 'http://example.com/v2'
        mock_get_auth_args.return_value = {}
        config_dict = defaults.get_defaults()
        config_dict.update(fake_services_dict)
        config_dict['api_timeout'] = 9
        cc = cloud_config.CloudConfig(
            name="test1",
            region_name="region-al",
            config=config_dict,
            auth_plugin=mock.Mock(),
        )
        cc.get_legacy_client('object-store', mock_client)
        mock_client.assert_called_with(
            session=mock.ANY,
            os_options={
                'region_name': 'region-al',
                'service_type': 'object-store',
                'object_storage_url': None,
                'endpoint_type': 'public',
            },
        )

    @mock.patch.object(cloud_region.CloudRegion, 'get_auth_args')
    def test_legacy_client_object_store_endpoint(self, mock_get_auth_args):
        mock_client = mock.Mock()
        mock_get_auth_args.return_value = {}
        config_dict = defaults.get_defaults()
        config_dict.update(fake_services_dict)
        config_dict['object_store_endpoint'] = 'http://example.com/swift'
        cc = cloud_config.CloudConfig(
            "test1", "region-al", config_dict, auth_plugin=mock.Mock()
        )
        cc.get_legacy_client('object-store', mock_client)
        mock_client.assert_called_with(
            session=mock.ANY,
            os_options={
                'region_name': 'region-al',
                'service_type': 'object-store',
                'object_storage_url': 'http://example.com/swift',
                'endpoint_type': 'public',
            },
        )

    @mock.patch.object(cloud_region.CloudRegion, 'get_session_endpoint')
    def test_legacy_client_image(self, mock_get_session_endpoint):
        mock_client = mock.Mock()
        mock_get_session_endpoint.return_value = 'http://example.com/v2'
        config_dict = defaults.get_defaults()
        config_dict.update(fake_services_dict)
        cc = cloud_config.CloudConfig(
            "test1", "region-al", config_dict, auth_plugin=mock.Mock()
        )
        cc.get_legacy_client('image', mock_client)
        mock_client.assert_called_with(
            version=2.0,
            service_name=None,
            endpoint_override='http://example.com',
            region_name='region-al',
            interface='public',
            session=mock.ANY,
            # Not a typo - the config dict above overrides this
            service_type='mage',
        )

    @mock.patch.object(cloud_region.CloudRegion, 'get_session_endpoint')
    def test_legacy_client_image_override(self, mock_get_session_endpoint):
        mock_client = mock.Mock()
        mock_get_session_endpoint.return_value = 'http://example.com/v2'
        config_dict = defaults.get_defaults()
        config_dict.update(fake_services_dict)
        config_dict['image_endpoint_override'] = 'http://example.com/override'
        cc = cloud_config.CloudConfig(
            "test1", "region-al", config_dict, auth_plugin=mock.Mock()
        )
        cc.get_legacy_client('image', mock_client)
        mock_client.assert_called_with(
            version=2.0,
            service_name=None,
            endpoint_override='http://example.com/override',
            region_name='region-al',
            interface='public',
            session=mock.ANY,
            # Not a typo - the config dict above overrides this
            service_type='mage',
        )

    @mock.patch.object(cloud_region.CloudRegion, 'get_session_endpoint')
    def test_legacy_client_image_versioned(self, mock_get_session_endpoint):
        mock_client = mock.Mock()
        mock_get_session_endpoint.return_value = 'http://example.com/v2'
        config_dict = defaults.get_defaults()
        config_dict.update(fake_services_dict)
        # v2 endpoint was passed, 1 requested in config, endpoint wins
        config_dict['image_api_version'] = '1'
        cc = cloud_config.CloudConfig(
            "test1", "region-al", config_dict, auth_plugin=mock.Mock()
        )
        cc.get_legacy_client('image', mock_client)
        mock_client.assert_called_with(
            version=2.0,
            service_name=None,
            endpoint_override='http://example.com',
            region_name='region-al',
            interface='public',
            session=mock.ANY,
            # Not a typo - the config dict above overrides this
            service_type='mage',
        )

    @mock.patch.object(cloud_region.CloudRegion, 'get_session_endpoint')
    def test_legacy_client_image_unversioned(self, mock_get_session_endpoint):
        mock_client = mock.Mock()
        mock_get_session_endpoint.return_value = 'http://example.com/'
        config_dict = defaults.get_defaults()
        config_dict.update(fake_services_dict)
        # Versionless endpoint, config wins
        config_dict['image_api_version'] = '1'
        cc = cloud_config.CloudConfig(
            "test1", "region-al", config_dict, auth_plugin=mock.Mock()
        )
        cc.get_legacy_client('image', mock_client)
        mock_client.assert_called_with(
            version='1',
            service_name=None,
            endpoint_override='http://example.com',
            region_name='region-al',
            interface='public',
            session=mock.ANY,
            # Not a typo - the config dict above overrides this
            service_type='mage',
        )

    @mock.patch.object(cloud_region.CloudRegion, 'get_session_endpoint')
    def test_legacy_client_image_argument(self, mock_get_session_endpoint):
        mock_client = mock.Mock()
        mock_get_session_endpoint.return_value = 'http://example.com/v3'
        config_dict = defaults.get_defaults()
        config_dict.update(fake_services_dict)
        # Versionless endpoint, config wins
        config_dict['image_api_version'] = '6'
        cc = cloud_config.CloudConfig(
            "test1", "region-al", config_dict, auth_plugin=mock.Mock()
        )
        cc.get_legacy_client('image', mock_client, version='beef')
        mock_client.assert_called_with(
            version='beef',
            service_name=None,
            endpoint_override='http://example.com',
            region_name='region-al',
            interface='public',
            session=mock.ANY,
            # Not a typo - the config dict above overrides this
            service_type='mage',
        )

    @mock.patch.object(cloud_region.CloudRegion, 'get_session_endpoint')
    def test_legacy_client_network(self, mock_get_session_endpoint):
        mock_client = mock.Mock()
        mock_get_session_endpoint.return_value = 'http://example.com/v2'
        config_dict = defaults.get_defaults()
        config_dict.update(fake_services_dict)
        cc = cloud_config.CloudConfig(
            "test1", "region-al", config_dict, auth_plugin=mock.Mock()
        )
        cc.get_legacy_client('network', mock_client)
        mock_client.assert_called_with(
            api_version='2.0',
            endpoint_type='public',
            endpoint_override=None,
            region_name='region-al',
            service_type='network',
            session=mock.ANY,
            service_name=None,
        )

    @mock.patch.object(cloud_region.CloudRegion, 'get_session_endpoint')
    def test_legacy_client_compute(self, mock_get_session_endpoint):
        mock_client = mock.Mock()
        mock_get_session_endpoint.return_value = 'http://example.com/v2'
        config_dict = defaults.get_defaults()
        config_dict.update(fake_services_dict)
        cc = cloud_config.CloudConfig(
            "test1", "region-al", config_dict, auth_plugin=mock.Mock()
        )
        cc.get_legacy_client('compute', mock_client)
        mock_client.assert_called_with(
            version='2',
            endpoint_type='public',
            endpoint_override='http://compute.example.com',
            region_name='region-al',
            service_type='compute',
            session=mock.ANY,
            service_name=None,
        )

    @mock.patch.object(cloud_region.CloudRegion, 'get_session_endpoint')
    def test_legacy_client_identity(self, mock_get_session_endpoint):
        mock_client = mock.Mock()
        mock_get_session_endpoint.return_value = 'http://example.com/v2'
        config_dict = defaults.get_defaults()
        config_dict.update(fake_services_dict)
        cc = cloud_config.CloudConfig(
            "test1", "region-al", config_dict, auth_plugin=mock.Mock()
        )
        cc.get_legacy_client('identity', mock_client)
        mock_client.assert_called_with(
            version='2.0',
            endpoint='http://example.com/v2',
            endpoint_type='admin',
            endpoint_override=None,
            region_name='region-al',
            service_type='identity',
            session=mock.ANY,
            service_name='locks',
        )

    @mock.patch.object(cloud_region.CloudRegion, 'get_session_endpoint')
    def test_legacy_client_identity_v3(self, mock_get_session_endpoint):
        mock_client = mock.Mock()
        mock_get_session_endpoint.return_value = 'http://example.com'
        config_dict = defaults.get_defaults()
        config_dict.update(fake_services_dict)
        config_dict['identity_api_version'] = '3'
        cc = cloud_config.CloudConfig(
            "test1", "region-al", config_dict, auth_plugin=mock.Mock()
        )
        cc.get_legacy_client('identity', mock_client)
        mock_client.assert_called_with(
            version='3',
            endpoint='http://example.com',
            interface='admin',
            endpoint_override=None,
            region_name='region-al',
            service_type='identity',
            session=mock.ANY,
            service_name='locks',
        )
