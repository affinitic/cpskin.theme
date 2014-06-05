# -*- coding: utf-8 -*-

from zope.traversing.interfaces import ITraverser
from zope.location.interfaces import LocationError
from plone.app.theming.utils import getCurrentTheme
from Products.Five import BrowserView


class CSSView(BrowserView):

    def getCSS(self, cssName):
        """
        Returns specified CSS from currently activated theme
        """
        request = self.request
        response = request.response
        activeTheme = getCurrentTheme()
        if activeTheme is None:
            return ""
        filePath = "++theme++%s/css/%s" % (activeTheme, cssName)
        try:
            resource = ITraverser(self.context).traverse(filePath,
                                                         request=self.request)
        except LocationError:
            return ""
        return resource(REQUEST=resource, RESPONSE=response)

    def getStylesCSS(self):
        return self.getCSS('styles.css')

    def getFontsCSS(self):
        return self.getCSS('fonts.css')
