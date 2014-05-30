# -*- coding: utf-8 -*-

from zope.traversing.interfaces import ITraverser
from zope.location.interfaces import LocationError
from plone.app.theming.utils import getCurrentTheme
from Products.Five import BrowserView


class CSSView(BrowserView):

    def getCSS(self, cssName):
        """
        Returns CSS (depending on theme id) from currently activated theme
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

    def getHomePageCSS(self):
        return self.getCSS('homepage.css')

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
