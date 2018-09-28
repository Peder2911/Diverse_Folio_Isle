
require(stringr)
require(glue)

require(tools)

require(jsonlite)
require(redux)

# Utility stuff ####################

myPath <- ComfyInTurns::myPath() 

# Redis stuff ######################

r <- hiredis()

r$FLUSHDB()

# Write the data back ##############

dat <- mtcars
dat['name'] <- rownames(dat)

fauxfile <- textConnection('fauxfile','w')
write.csv(dat,fauxfile)
#rm(dat)
textrep <- fauxfile
#rm(fauxfile)

null <- file('/dev/null')
sink(null)
sapply(textrep,FUN = function(x){
		r$RPUSH('data',x)
		})
sink()

# Or else? #########################


