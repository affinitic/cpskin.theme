from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting

import cpskin.theme


CPSKIN_THEME_FIXTURE = PloneWithPackageLayer(
    name="CPSKIN_THEME_FIXTURE",
    zcml_filename="testing.zcml",
    zcml_package=cpskin.theme,
    gs_profile_id="cpskin.theme:testing")

CPSKIN_THEME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_THEME_FIXTURE,),
    name="CPSkinTheme:Integration")
