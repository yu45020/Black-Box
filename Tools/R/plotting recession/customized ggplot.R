library(ggpubr)
library(ggplot2)
library(lubridate)

recession_bar = function(time_col, recession.df=read.csv("us_recession.csv",colClasses = c("Date"))){
  # assume either year(numeric) or Date format
  if (is.numeric(time_col)){
    recession.df = data.frame(sapply(recession.df,year))
  }
  recession.trim = subset(recession.df, Peak>=min(time_col)) 
  res = geom_rect(mapping=aes(xmin=Peak, xmax=Trough, ymin=-Inf, ymax=+Inf),
            fill='grey', alpha=0.3,data=recession.trim,
            inherit.aes=FALSE)
  return(res)
}





