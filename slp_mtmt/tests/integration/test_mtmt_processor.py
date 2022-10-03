from sl_util.sl_util.file_utils import get_byte_data
from slp_mtmt import MTMTProcessor
from slp_mtmt.tests.resources import test_resource_paths

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'
SAMPLE_VALID_MTMT_FILE = test_resource_paths.model_mtmt_mvp
SAMPLE_VALID_MAPPING_FILE = test_resource_paths.mapping_mtmt_mvp


class TestMtmtProcessor:

    def test_run_valid_mappings(self):
        # GIVEN a valid MTMT file with some resources
        source_file = get_byte_data(SAMPLE_VALID_MTMT_FILE)

        # AND a valid MTMT mapping file
        mapping_file = get_byte_data(SAMPLE_VALID_MAPPING_FILE)

        # WHEN the MTMT file is processed
        otm = MTMTProcessor(SAMPLE_ID, SAMPLE_NAME, source_file, [mapping_file]).process()

        # THEN the number of TZs, components and dataflows are right
        assert len(otm.trustzones) == 2
        assert len(otm.components) == 4
        assert len(otm.dataflows) == 6

        # AND the project info is also right
        assert otm.project_id == "id"
        assert otm.project_name == "name"

        # AND the representations info is also right
        assert otm.representations_id == "Microsoft Threat Model"
        assert otm.representations_name == "Microsoft Threat Model"
        assert otm.representations_type == "etm"

        # AND the info inside trustzones is also right
        trustzone = otm.trustzones[0]
        assert trustzone.id == '75605184-4ca0-43be-ba4c-5fa5ad15e367'
        assert trustzone.name == 'Internet'
        trustzone = otm.trustzones[1]
        assert trustzone.id == '24cdf4da-ac7f-4a35-bab0-29256d4169bf'
        assert trustzone.name == 'Private Secured Cloud'

        # AND the info inside components is also right
        component = otm.components[0]
        assert component.id == '53245f54-0656-4ede-a393-357aeaa2e20f'
        assert component.name == 'Accounting PostgreSQL'
        assert component.type == 'CD-MICROSOFT-AZURE-DB-POSTGRESQL'
        assert component.parent == '24cdf4da-ac7f-4a35-bab0-29256d4169bf'
        component = otm.components[1]
        assert component.id == '6183b7fa-eba5-4bf8-a0af-c3e30d144a10'
        assert component.name == 'Mobile Client'
        assert component.type == 'android-device-client'
        assert component.parent == '75605184-4ca0-43be-ba4c-5fa5ad15e367'
        component = otm.components[2]
        assert component.id == '5d15323e-3729-4694-87b1-181c90af5045'
        assert component.name == 'Public API v2'
        assert component.type == 'rest-full-web-service'
        assert component.parent == "24cdf4da-ac7f-4a35-bab0-29256d4169bf"
        component = otm.components[3]
        assert component.id == '91882aca-8249-49a7-96f0-164b68411b48'
        assert component.name == 'Azure File Storage'
        assert component.type == 'azure-storage'
        assert component.parent == '24cdf4da-ac7f-4a35-bab0-29256d4169bf'

        # AND the info inside dataflows is also right
        dataflow = otm.dataflows[0]
        assert dataflow.id == 'eb072144-af37-4b75-b46b-b78111850d3e'
        assert dataflow.source_node == '5d15323e-3729-4694-87b1-181c90af5045'
        assert dataflow.destination_node == '53245f54-0656-4ede-a393-357aeaa2e20f'
        assert not dataflow.bidirectional
        dataflow = otm.dataflows[1]
        assert dataflow.id == '36091fd8-dba8-424e-a3cd-784ea6bcb9e0'
        assert dataflow.source_node == '53245f54-0656-4ede-a393-357aeaa2e20f'
        assert dataflow.destination_node == '5d15323e-3729-4694-87b1-181c90af5045'
        dataflow = otm.dataflows[2]
        assert dataflow.id == 'f5fe3c6e-e10b-4252-a4aa-4ec6108c96a6'
        assert dataflow.source_node == '5d15323e-3729-4694-87b1-181c90af5045'
        assert dataflow.destination_node == '91882aca-8249-49a7-96f0-164b68411b48'
        dataflow = otm.dataflows[3]
        assert dataflow.id == 'f894ed9d-d1c3-42b7-9010-34274bf01c84'
        assert dataflow.source_node == '5d15323e-3729-4694-87b1-181c90af5045'
        assert dataflow.destination_node == '91882aca-8249-49a7-96f0-164b68411b48'
        dataflow = otm.dataflows[4]
        assert dataflow.id == '9840bcdf-c444-437d-8289-d5468f41b0db'
        assert dataflow.source_node == '6183b7fa-eba5-4bf8-a0af-c3e30d144a10'
        assert dataflow.destination_node == '5d15323e-3729-4694-87b1-181c90af5045'
        dataflow = otm.dataflows[5]
        assert dataflow.id == 'bf3d1783-c7c8-43dd-bfa4-efafeac1fe14'
        assert dataflow.source_node == '6183b7fa-eba5-4bf8-a0af-c3e30d144a10'
        assert dataflow.destination_node == '5d15323e-3729-4694-87b1-181c90af5045'
