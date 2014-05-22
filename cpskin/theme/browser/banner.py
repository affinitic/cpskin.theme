# -*- coding: utf-8 -*-

from Products.Five import BrowserView


BANNER_STYLE = """
#portal-header {
  background-image: url(%s/banner.jpg);
  background-size: cover;
}
"""


class BannerView(BrowserView):

    def getCSS(self):
        """
        LATER : If no special behavior is needed, we can put the background
        style in a real CSS file
        """
        response = self.request.response
        response.setHeader("Content-type", "text/css")
        css = BANNER_STYLE % self.context.absolute_url()
        return css
