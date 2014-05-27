# -*- coding: utf-8 -*-

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

    def isInATheme(self):
        """
        Returns True if we are currently in a theme
        """
        context = self.context
        # Get the right object if we are on a default page
        portal = getToolByName(context, 'portal_url').getPortalObject()
        plone_view = portal.restrictedTraverse('@@plone')
        if plone_view.isDefaultPageInFolder():
            # if the context is a default page, get the parent!
            obj = context.aq_inner.aq_parent
            context = obj
        # Take the path, traverse to the first level and see if it is a
        # element respecting the navigation strategy
        portal_url = getToolByName(context, 'portal_url')
        contentPath = portal_url.getRelativeContentPath(context)
        if not len(contentPath):
            # we are on the home page
            return False
        # Use the portal_catalog the get the first level element
        portal_catalog = getToolByName(context, 'portal_catalog')
        portal = getToolByName(context, 'portal_url').getPortalObject()
        queryDict = {}
        queryDict['path'] = {'query': '/'.join(portal.getPhysicalPath()) + '/' + contentPath[0], 'depth': 0}
        queryDict['portal_type'] = 'Folder'
        brains = portal_catalog(queryDict)
        if not brains:
            return False
        brain = brains[0]
        navtreeProps = getToolByName(context, 'portal_properties').navtree_properties
        if not brain.meta_type in navtreeProps.metaTypesNotToList and \
           (brain.review_state in navtreeProps.wf_states_to_show or \
            not navtreeProps.enable_wf_state_filtering) and \
           not brain.id in navtreeProps.idsNotToList:
            return True
        return False
