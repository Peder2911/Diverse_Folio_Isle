
require(stringr)
require(glue)

require(tools)

require(jsonlite)
require(redux)

# Utility stuff ####################

scriptpath <- ComfyInTurns::myPath()

config <- readLines('stdin')%>%
	fromJSON()%>%
	suppressWarnings()

# Read my functions ################

dirname(scriptpath)%>%
	paste('lib/funcs.R',sep = '/')%>%
	source()

# Redis stuff ######################

redis_config(host = config$redis$hostname,
	     port = config$redis$port,
	     db = config$redis$db)

r <- hiredis()

# Read data ########################

ln <- ''
indata <- character()

while(!is.null(ln)){
	ln <- r$LPOP(config$redis$listkey)
	indata <- c(indata,ln)
	}

if(length(indata) > 1){

	# text to csv ##############

	indata <- glue_collapse(indata,sep = '\n')
	dat <- read.csv(text = indata)
	rm(indata)
	
	# Do stuff to the data #####

	doStuff(dat)

	# Write the data back ######

	fauxfile <- textConnection('fauxfile','w')
	write.csv(dat,fauxfile)
	rm(dat)
	
	# shut it up
	devnull <- file('/dev/null')
	sink(devnull)

	write(fauxfile,'tee.txt')

	sapply(fauxfile,FUN = function(x){
	     		r$RPUSH(config$redis$listkey,x)
	     		})
	sink()

	}else{

	# Or else? #################

	warning('no data read')
	}


