## Test ##
library(data.table)



hotencoder = function(dat_, keep_col=FALSE, drop_first_level=FALSE, sep_char='=',inplace=FALSE){

  ###################################
  .create_col_names = function(unique_level,col_to_encode,drop_first_level,sep_char){
    
    if(drop_first_level){
      unique_level = lapply(unique_level,FUN=function(x)x[-1])
    }
    
    col_names= mapply(paste, col_to_encode, unique_level,sep=sep_char,SIMPLIFY = FALSE)
    return(col_names)
  }

  ###################################
  
  if(inplace){
    dat = dat_
  }else{
    dat = copy(dat_)
  }
  
  # get non-numeric column names
  col_attr = sapply(dat, is.numeric)
  col_to_encode = c(names(dat)[!col_attr])
  
  setindexv(dat, col_to_encode)
  
  # get unique values for each columns 
  unique_level_percol = dat[,.(lapply(.SD,unique)),.SDcols=col_to_encode]$V1
  names(unique_level_percol)= col_to_encode
  
  unique_level_percol = lapply(unique_level_percol,as.character) # make sure no factor 
  
  # get newe column names with unique value e.g. col1=type A 
  col_newname = .create_col_names(unique_level_percol,col_to_encode,drop_first_level,sep_char)
  
  # create dummy columns with all 0
  dat[,(unlist(col_newname)):=0L]
  
  # assign matched row entry to 1 
  for(col_ in col_to_encode){
    col_name_dummy = col_newname[[col_]]
    unique_level = unique_level_percol[[col_]]
    for(i in 1:length(col_name_dummy)){
      dat[unique_level[i],(col_name_dummy[i]):=1L, on=col_]
    }
  }
  
}



N=1e7; K=10
set.seed(1)
DT <- data.table(
  id1 = sample(sprintf("id%03d",1:K), N, TRUE),      # large groups (char)
  id3 = sample(sprintf("id%010d",1:K), N, TRUE),     # small groups (char)
  id4 = sample(K, N, TRUE),                          # large groups (int)
  id5 = factor(sample(K, N, TRUE)),                  # large groups (int)
  id6 = sample(N/K, N, TRUE),                        # small groups (int)
  v1 =  sample(5, N, TRUE),                          # int in range [1,5]
  v2 =  sample(5, N, TRUE),                          # int in range [1,5]
  v3 =  sample(round(runif(100,max=100),4), N, TRUE) # numeric e.g. 23.5749
)

format(object.size(DT), units = 'Mb')
DT[,lapply(.SD, uniqueN)]
DT_ = copy(DT)



system.time(hotencoder(DT))


library(fastDummies)
system.time(dummy_cols(DT_))
