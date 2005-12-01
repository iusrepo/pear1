# Makefile for source rpm: php-pear
# $Id$
NAME := php-pear
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
