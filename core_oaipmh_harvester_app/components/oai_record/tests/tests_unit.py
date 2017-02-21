from unittest.case import TestCase
from bson.objectid import ObjectId
from mock.mock import Mock, patch
import core_oaipmh_harvester_app.components.oai_record.api as oai_record_api
from core_main_app.commons import exceptions
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord
from core_oaipmh_harvester_app.components.oai_harvester_set.models import OaiHarvesterSet
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import OaiHarvesterMetadataFormat
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry
import datetime
from core_main_app.utils.xml import OrderedDict


class TestOaiRecordUpsert(TestCase):
    def setUp(self):
        self.oai_record = _create_oai_record()

    @patch.object(OaiRecord, 'save')
    def test_upsert_oai_record_return_object(self, mock_save):
        # Arrange
        mock_save.return_value = self.oai_record

        # Act
        result = oai_record_api.upsert(self.oai_record)

        # Assert
        self.assertIsInstance(result, OaiRecord)

    @patch.object(OaiRecord, 'save')
    def test_upsert_oai_harvester_raises_exception_if_save_failed(self, mock_save):
        # Arrange
        mock_save.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            oai_record_api.upsert(self.oai_record)

    @patch.object(OaiRecord, 'save')
    def test_upsert_deleted_oai_record_return_object_with_empty_metadata(self, mock_save):
        # Arrange
        self.oai_record.deleted = True
        mock_save.return_value = self.oai_record

        # Act
        result = oai_record_api.upsert(self.oai_record)

        # Assert
        self.assertEquals(result.metadata, {})


class TestOaiRecordGetById(TestCase):
    @patch.object(OaiRecord, 'get_by_id')
    def test_get_by_id_return_object(self, mock_get_by_id):
        # Arrange
        mock_oai_record = _create_mock_oai_record()

        mock_get_by_id.return_value = mock_oai_record

        # Act
        result = oai_record_api.get_by_id(mock_get_by_id.id)

        # Assert
        self.assertIsInstance(result, OaiRecord)

    @patch.object(OaiRecord, 'get_by_id')
    def test_get_by_id_raises_exception_if_object_does_not_exist(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()

        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            oai_record_api.get_by_id(mock_absent_id)

    @patch.object(OaiRecord, 'get_by_id')
    def test_get_by_id_raises_exception_if_internal_error(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()

        mock_get_by_id.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            oai_record_api.get_by_id(mock_absent_id)


class TestOaiRecordGetAllByRegistryId(TestCase):
    @patch.object(OaiRecord, 'get_all_by_registry_id')
    def test_get_all_by_registry_id_return_object(self, mock_get_all):
        _generic_get_all_test(self, mock_get_all, oai_record_api.get_all_by_registry_id(ObjectId()))


class TestOaiRecordGetAll(TestCase):
    @patch.object(OaiRecord, 'get_all')
    def test_get_all_contains_only_oai_record(self, mock_get_all):
        _generic_get_all_test(self, mock_get_all, oai_record_api.get_all())


class TestOaiRecordGetCountByRegistryId(TestCase):
    @patch.object(OaiRecord, 'get_count_by_registry_id')
    def test_get_count_by_registry_id_return_number(self, mock_get):
        # Arrange
        mock_registry_id = ObjectId()

        mock_get.return_value = 2

        # Act
        result = oai_record_api.get_count_by_registry_id(mock_registry_id)

        # Assert
        self.assertEquals(result, 2)


class TestOaiRecordDelete(TestCase):
    @patch.object(OaiRecord, 'delete')
    def test_delete_oai_record_raises_exception_if_object_does_not_exist(self, mock_delete):
        # Arrange
        oai_record = _create_oai_record()
        mock_delete.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(Exception):
            oai_record_api.delete(oai_record)


class TestOaiRecordExecuteFullTextQuery(TestCase):
    @patch.object(OaiRecord, 'execute_full_text_query')
    def test_oai_record_execute_full_text_query_return_collection(self, mock_execute):
        _generic_get_all_test(self, mock_execute, oai_record_api.execute_full_text_query('', [ObjectId(), ObjectId()]))


def _generic_get_all_test(self, mock_get_all, act_function):
    # Arrange
    mock_oai_record1 = _create_mock_oai_record()
    mock_oai_record2 = _create_mock_oai_record()

    mock_get_all.return_value = [mock_oai_record1, mock_oai_record2]

    # Act
    result = act_function

    # Assert
    self.assertTrue(all(isinstance(item, OaiRecord) for item in result))


def _create_oai_record():
    """ Get an OaiRecord object.

        Returns:
            OaiRecord instance.

    """
    oai_record = OaiRecord()
    _set_oai_record_fields(oai_record)

    return oai_record


def _create_mock_oai_record():
    """ Mock an OaiRecord.

        Returns:
            OaiRecord mock.

    """
    mock_oai_record = Mock(spec=OaiRecord)
    _set_oai_record_fields(mock_oai_record)

    return mock_oai_record


def _set_oai_record_fields(oai_record):
    """ Set OaiRecord fields.

        Args:
            oai_record:

        Returns:
            OaiRecord with assigned fields.

    """
    oai_record.identifier = "oai:test/id.0006"
    oai_record.datestamp = datetime.datetime.now()
    oai_record.deleted = False
    oai_record.harvester_sets = [OaiHarvesterSet(), OaiHarvesterSet()]
    oai_record.harvester_metadata_format = OaiHarvesterMetadataFormat()
    oai_record.metadata = "<test><message>Hello</message></test>"
    oai_record.raw = dict()
    oai_record.registry = OaiRegistry()

    return oai_record