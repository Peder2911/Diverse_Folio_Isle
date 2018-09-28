
library(glue)
library(dplyr)

doStuff <- function(dat){

        print(glue_collapse(c('rows read:',nrow(dat)),sep = ' '))

	dat <- dat[dat$mpg < 20,]

        print(glue_collapse(c('rows after filtering:',nrow(dat)),sep = ' '))
        print(glue_collapse(c('column names:',names(dat)),sep = '\n'))

	dat
	}
	
