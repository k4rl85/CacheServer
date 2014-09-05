#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'carlo'

import xmlrpclib

server = xmlrpclib.ServerProxy('http://localhost:8080')
var = 'var'
var2 = 'b'

print server.set(var, 10)
print 'Try to find "{}": '.format(var), server.get(var)
print 'Try to find "{}":'.format(var2), server.get(var2)
print server.delete('a')

server.set(var, 1)
print server.get(var)
print server.set_many({'c': 2, 'l': 3})
print server.set_many({var: 2, var2: 6, 'fsdfd': 'ciao'})
l = [var, var2, 'drfgdgfvdf']
print 'received from server', server.get_many(l)
print server.set(var, 134534)
server.set('pincopallino', 5)
