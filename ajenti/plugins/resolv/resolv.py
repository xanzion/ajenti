from ajenti.api import *
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui.binder import Binder

from reconfigure.configs import ResolvConfig
from reconfigure.items.resolv import Item


@plugin
class Resolv (SectionPlugin):
    def init(self):
        self.title = 'Nameservers'
        self.category = 'System'

        self.append(self.ui.inflate('resolv:main'))
        self.find('name-box').items = ['DNS nameserver', 'Local domain name', 'Search list', 'Sort list', 'Options']
        self.find('name-box').values = ['nameserver', 'domain', 'search', 'sortlist', 'options']

        self.config = ResolvConfig(path='/etc/resolv.conf')
        self.config.load()
        self.binder = Binder(self.config.tree, self.find('resolv-config'))
        self.find('items').new_item = lambda c: Item()
        self.binder.autodiscover()
        self.binder.populate()

        self.find('save').on('click', self.save)

    def save(self):
        self.binder.update()
        self.config.save()
        self.publish()
