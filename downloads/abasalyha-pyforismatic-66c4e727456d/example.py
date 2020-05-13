# -*- coding: UTF-8 -*-

# Just importing Forsimatic class
from forismatic import Forismatic

# Initializing manager
f = Forismatic()

# Getting Quote object & printing quote and author
q = f.get_quote()
print u'%s\t%s' % (q.quote, q.author)