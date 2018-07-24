#!/usr/local/bin/rscript

library(randomNames)
name = randomNames(name.order='first.last',name.sep='_')
writeLines(name)
