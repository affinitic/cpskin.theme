# -*- coding: utf-8 -*-

from zope.traversing.interfaces import ITraverser
from zope.location.interfaces import LocationError
from plone.app.theming.utils import getCurrentTheme
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class ThemesView(BrowserView):

    def isInTheme(self, themeId):
        """
        Returns True if we are in the theme id
        """
        context = self.context
        # Get 1st level folders appearing in navigation
        portal_catalog = getToolByName(context, 'portal_catalog')
        navtreeProps = getToolByName(context, 'portal_properties').navtree_properties
        portal = getToolByName(context, 'portal_url').getPortalObject()
        queryDict = {}
        # LATER : queryPath = getNavigationRoot(context) ?
        queryDict['path'] = {'query': '/'.join(portal.getPhysicalPath()), 'depth': 1}
        if navtreeProps.enable_wf_state_filtering:
            queryDict['review_state'] = navtreeProps.wf_states_to_show
        queryDict['sort_on'] = 'getObjPositionInParent'
        queryDict['portal_type'] = 'Folder'
        queryDict['is_default_page'] = False
        brains = portal_catalog(queryDict)
        res = [b for b in brains if b.id not in navtreeProps.idsNotToList]

        # Get the first level of the current
        actual_url_path = '/'.join(context.getPhysicalPath())
        # Check if we are in a theme and check if we are in the right one (position)
        index = 1
        for brain in res:
            # checking startswith is not enough
            # see ticket #1227 :
            # if theme1 id is "theme" and theme2 id is "theme2", while being in the
            # theme2, it starts with 'theme' so it returns True to checking if being in theme 1...
            brainPath = brain.getPath()
            if actual_url_path.startswith(brainPath):
                brainPathLen = len(brainPath)
                if len(actual_url_path) == brainPathLen \
                   or actual_url_path[brainPathLen:brainPathLen + 1] == '/':
                    return (index == themeId)
            index += 1
        return False

    def getCSS(self, cssName):
        """
        Returns CSS (depending on theme id) from currently activated theme
        """
        request = self.request
        response = request.response
        activeTheme = getCurrentTheme()
        if activeTheme is None:
            return
        filePath = "++theme++%s/css/%s" % (activeTheme, cssName)
        try:
            resource = ITraverser(self.context).traverse(filePath,
                                                         request=self.request)
        except LocationError:
            return
        return resource(REQUEST=resource, RESPONSE=response)

    def getTheme1CSS(self):
        return self.getCSS('theme1.css')

    def getTheme2CSS(self):
        return self.getCSS('theme2.css')

    def getTheme3CSS(self):
        return self.getCSS('theme3.css')

    def getTheme4CSS(self):
        return self.getCSS('theme4.css')

    def getTheme5CSS(self):
        return self.getCSS('theme5.css')
