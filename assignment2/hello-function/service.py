# -*- coding: utf-8 -*-

print "Loading functions"
def handler(event, context):
    # Your code goes here!
    print "Hello world"
    print event
    e = event.get('e')
    pi = event.get('pi')
    return e + pi
