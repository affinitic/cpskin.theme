import os
import logging
from plone import api

logger = logging.getLogger('cpskin.theme')


def installTheme(context):
    if context.readDataFile('cpskin.theme-default.txt') is None:
        return

    logger.info('Installing')
    portal = context.getSite()

    dataPath = os.path.join(os.path.dirname(__file__), 'data')
    bannerPath = os.path.join(dataPath, 'banner.jpg')
    bannerFd = open(bannerPath, 'rb')
    if not portal.hasObject('banner.jpg'):
        api.content.create(type='Image',
                           title='banner.jpg',
                           container=portal,
                           file=bannerFd)
    bannerFd.close()


def uninstallTheme(context):
    if context.readDataFile('cpskin.theme-uninstall.txt') is None:
        return

    logger.info('Uninstalling')
    portal = context.getSite()

    if portal.hasObject('banner.jpg'):
        api.content.delete(obj=portal['banner.jpg'])
