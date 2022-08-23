import pytest

from startleft.api.errors import OtmBuildingError
from startleft.iac.iac_to_otm import IacToOtm
from startleft.iac.iac_type import IacType
from startleft.utils import file_utils as FileUtils
from tests.resources import test_resource_paths


class TestApp:

    def test_load_yaml_file(self):
        filename = test_resource_paths.example_yaml
        iac_to_otm = IacToOtm('name', 'id', IacType.CLOUDFORMATION)
        iac_to_otm.load_yaml_source(FileUtils.get_data(filename))
        assert iac_to_otm.source_model.data

    def test_load_json_file(self):
        filename = test_resource_paths.example_json
        iac_to_otm = IacToOtm('name', 'id', IacType.CLOUDFORMATION)
        iac_to_otm.load_yaml_source(FileUtils.get_data(filename))
        assert iac_to_otm.source_model.data

    def test_run(self):
        filename = test_resource_paths.example_json
        mapping_filename = test_resource_paths.default_cloudformation_mapping
        iac_to_otm = IacToOtm('name', 'id', IacType.CLOUDFORMATION)
        iac_to_otm.run(IacType.CLOUDFORMATION, [FileUtils.get_data(mapping_filename)], [FileUtils.get_data(filename)])
        assert iac_to_otm.source_model.data

    def test_run_cloudformation_mappings(self):
        filename = test_resource_paths.cloudformation_for_mappings_tests_json
        mapping_filename = test_resource_paths.default_cloudformation_mapping
        iac_to_otm = IacToOtm('name', 'id', IacType.CLOUDFORMATION)
        iac_to_otm.run(IacType.CLOUDFORMATION, [FileUtils.get_data(mapping_filename)], [FileUtils.get_data(filename)])

        assert iac_to_otm.source_model.otm
        assert len(iac_to_otm.otm.trustzones) == 1
        assert len(iac_to_otm.otm.components) > 1
        assert len(iac_to_otm.otm.dataflows) == 1

        assert list(filter(lambda obj: obj.name == 'DummyCertificate', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'RDSCluster', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'kms (grouped)', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'sns (grouped)', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'cloudwatch (grouped)', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'api-gateway (grouped)', iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'DynamoDB from VPCEndpoint', iac_to_otm.otm.components))
        assert list(
            filter(lambda obj: obj.name == 'Systems Manager from VPCEndpoint (grouped)', iac_to_otm.otm.components))
        assert list(
            filter(lambda obj: obj.name == 'API gateway data flow from DummyApiAuthorizer', iac_to_otm.otm.dataflows))

        assert list(filter(lambda obj: obj.name == 'DummyCertificate'
                                       and "AWS::CertificateManager::Certificate" in obj.tags
                                       and len(obj.tags) == 1, iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'kms (grouped)'
                                       and "DummyTableKey (AWS::KMS::Key)" in obj.tags
                                       and "DummyCanaryBucketKey (AWS::KMS::Key)" in obj.tags
                                       and len(obj.tags) == 2, iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'sns (grouped)'
                                       and "DummySubscription (AWS::SNS::Subscription)" in obj.tags
                                       and "DummyTopic (AWS::SNS::Topic)" in obj.tags
                                       and len(obj.tags) == 2, iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'cloudwatch (grouped)'
                                       and "DummyCWAlarm (AWS::CloudWatch::Alarm)" in obj.tags
                                       and "DummyLogGroupA (AWS::Logs::LogGroup)" in obj.tags
                                       and "DummyLogGroupB (AWS::Logs::LogGroup)" in obj.tags
                                       and len(obj.tags) == 3, iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'api-gateway (grouped)'
                                       and "DummyApiAuthorizer (AWS::ApiGateway::Authorizer)" in obj.tags
                                       and "DummyApiGwKdsRestApi (AWS::ApiGateway::RestApi)" in obj.tags
                                       and len(obj.tags) == 2, iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == 'Systems Manager from VPCEndpoint (grouped)'
                                       and "DummyVPCssm (AWS::EC2::VPCEndpoint)" in obj.tags
                                       and "DummyVPCssmmessages (AWS::EC2::VPCEndpoint)" in obj.tags
                                       and len(obj.tags) == 2, iac_to_otm.otm.components))
        assert list(filter(lambda obj: obj.name == "DynamoDB from VPCEndpoint"
                                       and "DummyVPCdynamodb (AWS::EC2::VPCEndpoint)" in obj.tags
                                       and len(obj.tags) == 1, iac_to_otm.otm.components))

    @pytest.mark.parametrize('iac_type,filename,mapping_filename',
                             [
                                 (IacType.CLOUDFORMATION,
                                  test_resource_paths.cloudformation_component_without_parent,
                                  test_resource_paths.cloudformation_mapping_component_without_parent),
                             ])
    def test_mapping_component_without_parent(self, iac_type: IacType, filename: str, mapping_filename: str):
        iac_to_otm = IacToOtm('name', 'id', iac_type)
        with pytest.raises(OtmBuildingError) as e_info:
            iac_to_otm.run(iac_type, [FileUtils.get_data(mapping_filename)], [FileUtils.get_data(filename)])
        assert 'KeyError' == e_info.value.detail
        assert "'parent'" == e_info.value.message

    @pytest.mark.parametrize('iac_type,filename,mapping_filename',
                             [
                                 (IacType.CLOUDFORMATION,
                                  test_resource_paths.cloudformation_skipped_component_without_parent,
                                  test_resource_paths.cloudformation_mapping_component_without_parent),
                             ])
    def test_mapping_skipped_component_without_parent(self, iac_type: IacType, filename: str, mapping_filename: str):
        iac_to_otm = IacToOtm('name', 'id', iac_type)
        iac_to_otm.run(iac_type, [FileUtils.get_data(mapping_filename)], [FileUtils.get_data(filename)])

        assert iac_to_otm.source_model.otm
        assert len(iac_to_otm.otm.trustzones) == 1
        assert len(iac_to_otm.otm.components) == 1
        assert len(iac_to_otm.otm.dataflows) == 0
        assert iac_to_otm.otm.trustzones[0].id == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert iac_to_otm.otm.trustzones[0].name == 'Public Cloud'
        assert iac_to_otm.otm.components[0].type == 'aws_control'
        assert iac_to_otm.otm.components[0].name == 'Control_component'
        assert iac_to_otm.otm.components[0].parent == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

