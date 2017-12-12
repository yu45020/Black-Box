library(data.table)

encodedummy = function(dat_, keep_col=FALSE, drop_first_level=FALSE, sep_char='=',inplace=FALSE){

  ###################################
  # Helper Function ####
  .create_col_names = function(unique_level,col_to_encode,drop_first_level,sep_char){
    
    if(drop_first_level){
      unique_level = lapply(unique_level,FUN=function(x)x[-1])
    }
    
    col_names= mapply(paste, col_to_encode, unique_level,sep=sep_char,SIMPLIFY = FALSE)
    return(col_names)
  }
  
  .create_dummy_cols = function(col_){
    col_unique = unique_level_percol[[col_]]
    col_name = col_newname[[col_]]
    dat[,(col_name):=lapply(col_unique, chmatch, x=get(col_),nomatch=0L)]    
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
  dat[,(col_to_encode):=lapply(.SD,as.character),.SDcols=col_to_encode]
  
  # get unique values for each columns 
  unique_level_percol = dat[,.(lapply(.SD,unique)),.SDcols=col_to_encode]$V1
  names(unique_level_percol)= col_to_encode
  
  unique_level_percol = lapply(unique_level_percol,as.character) # make sure no factor 
  
  unique_level_percol = lapply(unique_level_percol,sort) #sort order
  
  # get newe column names with unique value e.g. col1=type A 
  col_newname = .create_col_names(unique_level_percol,col_to_encode,drop_first_level,sep_char)
  
  
  for(col_ in col_to_encode){
    .create_dummy_cols(col_)
  }

  return(dat)
}


# test ################ 
#get_test_data=function(N=1e5,K=6){
#  set.seed(1)
#  DT <- data.table(
#    id1 = factor(sample(sprintf("id%03d",1:K), N, TRUE)),      # large groups (char)
#    id3 = sample(sprintf("id%010d",1:K), N, TRUE),     # small groups (char)
    #id4 = sample(K, N, TRUE),                          # large groups (int)
 #   id5 = factor(sample(K, N, TRUE)),                  # large groups (int)
    #id6 = sample(N/K, N, TRUE),                        # small groups (int)
    #v1 =  sample(5, N, TRUE),                          # int in range [1,5]
  #  v3 =  sample(round(runif(100,max=100),4), N, TRUE) # numeric e.g. 23.5749
   # )
#}
#dat = encodedummy(get_test_data())
#  print(format(object.size(DT), units = 'Mb'))
#  print(DT[,lapply(.SD, uniqueN)])
##  return(DT)
#}
#DT = get_test_data(N=1e5,K=10)
#system.time(dummyencoder(DT))
#system.time(dummyencoder(DT))
##############################