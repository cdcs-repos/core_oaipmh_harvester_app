from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

sharing_children = (
    MenuItem("Request builder", reverse("admin:core_oaipmh_harvester_app_request_builder"), icon="magic"),
    MenuItem("Data providers", reverse("admin:core_oaipmh_harvester_app_registries"), icon="database"),
    MenuItem("Local configuration", reverse("admin:core_oaipmh_harvester_app_local_configuration"), icon="gear")
)

Menu.add_item(
    "admin", MenuItem("OAI PMH", None, children=sharing_children)
)