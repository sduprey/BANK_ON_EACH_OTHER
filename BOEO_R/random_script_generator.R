### random script generator
library("igraph")
library("lubridate")
library("data.table")
library("ggplot2")
set.seed(11181928)

simulationWithoutDefault <- FALSE
if (simulationWithoutDefault){
  plotGraph <- TRUE
  if(plotGraph){
    #### generate a random graph
    # g <- erdos.renyi.game(1000, 1/1000)
    # degree.distribution(g)
    
    
    # Load the igraph package (install if needed)
    # require(igraph)
    
    # Data format. The data is in 'edges' format meaning that each row records a relationship (edge) between two people (vertices).
    # Additional attributes can be included. Here is an example:
    # Waranter Warrantee grade_specification
    # AA BD 6 X 
    # BD CA 8 Y
    # AA DE 7 Y
    # ... ... ... ...
    # In this anonymized example, we have data on co-supervision with additional information about grades and specialization. 
    # It is also possible to have the data in a matrix form (see the igraph documentation for details)
    
    # Load the data. The data needs to be loaded as a table first: 
    
    print('Reading from disk')
    # bsk <- readRDS("../input/bsk.rds")
    bsk <- read.csv("../input/bsk.csv")
    
    
    
    ###############################
    ###############################
    ###############################
    ##### Getting the warranter, the warrantee, and the amount
    ###############################
    ###############################
    ###############################
    print(head(bsk))
    pure_warranter <- setdiff(bsk$warranter,bsk$warrantee)
    bsk$isBorrower <- !(bsk$warranter %in% pure_warranter)
    ### gettng to know the borrowing strength
    warrantee_strength <- as.data.frame(table(bsk$warrantee))
    colnames(warrantee_strength)<- c("name","borrower_strength")
    
    warranter_weakness <- as.data.frame(table(bsk$warranter))
    colnames(warranter_weakness)<- c("name","lender_weakness")
    
    
    # colnames(warrantee_strength)<- c("warrantee","borrower_strength")
    # bsk <- merge(bsk, warrantee_strength, all.x = TRUE, by="warrantee")
    # print(head(bsk))
    
    ###############################
    ###############################
    ###############################
    ###############################
    ###############################
    ###############################
    
    
    # Transform the table into the required graph format:
    bsk.network <- graph.data.frame(bsk, directed=F) #the 'directed' attribute specifies whether the edges are directed
    # or equivelent irrespective of the position (1st vs 2nd column). For directed graphs use 'directed=T'
    
    # Inspect the data:
    
    V(bsk.network) #prints the list of vertices (people)
    E(bsk.network) #prints the list of edges (relationships)
    degree(bsk.network) #print the number of edges per vertex (relationships per people)
    
    print(length(degree(bsk.network)))
    print(class(degree(bsk.network)))
    print(hist(degree(bsk.network),100))
    # First try. We can plot the graph right away but the results will usually be unsatisfactory:
    
    
    ###############################
    ###############################
    ###############################
    ##### Sandard visualization
    ###############################
    ###############################
    ###############################
    
    # plot(bsk.network)
    # 
    # plot(bsk.network, layout=layout_with_fr, vertex.size=4,
    #      vertex.label.dist=0.5, vertex.color="red", edge.arrow.size=0.5)
    # 
    # 
    ############################
    ############################
    #### Visualization force atlas 2
    ############################
    ############################
    ############################
    # ###### visualization force atlas 2
    # source("./layout.forceatlas2.R")
    # layout.forceatlas2(bsk.network, iterations=10000, plotstep=500)
    # 
    # library(ForceAtlas2)
    # # g <- nexus.get("miserables")
    # layout <- layout.forceatlas2(bsk.network, iterations=2000, plotstep=100)
    
    
    # # Here is the result:
    # # Not very informative indeed. Let’s go on:
    # #Subset the data. If we want to exclude people who are in the network only tangentially (participate in one or two relationships only)
    # # we can exclude the by subsetting the graph on the basis of the 'degree':
    # bad.vs<-V(bsk.network)[degree(bsk.network)<3] #identify those vertices part of less than three edges
    # bsk.network<-delete.vertices(bsk.network, bad.vs) #exclude them from the graph
    
    # Plot the data.Some details about the graph can be specified in advance.
    # For example we can separate some vertices (people) by color:
    
    print("getting the right color and size")
    V(bsk.network)$isBorrower <- !(V(bsk.network)$name %in% pure_warranter)
    
    library(plyr)
    temp <- plyr::join(data.frame(name = V(bsk.network)$name),warrantee_strength, by='name')
    V(bsk.network)$borrower_strength <- temp$borrower_strength
    
    temp <- plyr::join(data.frame(name = V(bsk.network)$name),warranter_weakness, by='name')
    V(bsk.network)$lender_weakness <- temp$lender_weakness
    
    V(bsk.network)$strength <- V(bsk.network)$borrower_strength 
    V(bsk.network)$strength[is.na(V(bsk.network)$strength)] <- V(bsk.network)$lender_weakness[is.na(V(bsk.network)$strength)]+1
    
    V(bsk.network)$color <- ifelse(V(bsk.network)$isBorrower, 'blue','green') #useful for highlighting certain people. Works by matching the name attribute of the vertex to the one specified in the 'ifelse' expression
    V(bsk.network)$size <- V(bsk.network)$strength
    
    # # We can also color the connecting edges differently depending on the 'grade': 
    # E(bsk.network)$color<-ifelse(E(bsk.network)$grade==9, "red", "grey")
    # # or depending on the different specialization ('spec'):
    # E(bsk.network)$color<-ifelse(E(bsk.network)$spec=='X', "red", ifelse(E(bsk.network)$spec=='Y', "blue", "grey"))
    # # Note: the example uses nested ifelse expressions which is in general a bad idea but does the job in this case
    # # Additional attributes like size can be further specified in an analogous manner, either in advance or when the plot function is called:
    # V(bsk.network)$size<-degree(bsk.network)/10#here the size of the vertices is specified by the degree of the vertex, so that people supervising more have get proportionally bigger dots. Getting the right scale gets some playing around with the parameters of the scale function (from the 'base' package)
    
    # Note that if the same attribute is specified beforehand and inside the function, the former will be overridden.
    # And finally the plot itself:
    par(mai=c(0,0,1,0)) #this specifies the size of the margins. the default settings leave too much free space on all sides (if no axes are printed)
    plot(bsk.network, #the graph to be plotted
         layout=layout.fruchterman.reingold, # the layout method. see the igraph documentation for details
         main='Warranter/warrantee network', #specifies the title
         vertex.label.dist=1, #puts the name labels slightly off the dots
         vertex.frame.color='blue', #the color of the border of the dots 
         vertex.label.color='black', #the color of the name labels
         vertex.label.font=2, #the font of the name labels
         vertex.label=V(bsk.network)$name, #specifies the lables of the vertices. in this case the 'name' attribute is used
         vertex.label.cex=1 #specifies the size of the font of the labels. can also be made to vary
    )
    
    # Save and export the plot. The plot can be copied as a metafile to the clipboard, or it can be saved as a pdf or png (and other formats).
    # For example, we can save it as a png:
    png(filename="../input/warranter_warrantee_network.png", height=800, width=600) #call the png writer
    #run the plot
    dev.off() #dont forget to close the device
    #And that's the end for now.
    
    print("computing the page rank")
    page_rank_results <- page_rank(bsk.network)
    print(length(page_rank_results$vector))
    page_rank_results_df <- data.frame(name = names(page_rank_results$vector),default_probability = page_rank_results$vector)
    
    people_summary <- data.frame(name = V(bsk.network)$name, isBorrower = V(bsk.network)$isBorrower, lender_weakness = V(bsk.network)$lender_weakness, borrower_strength = V(bsk.network)$borrower_strength)
    people_summary <- merge (people_summary, page_rank_results_df,all.x = TRUE, sort = FALSE, by = "name")
    print("checking our probability sums up to 1")
    print(sum(people_summary$default_probability))
    saveRDS(people_summary, "../input/people_summary.rds")
    saveRDS(bsk.network, "../input/people_graph.rds")
    saveRDS(bsk, "../input/people_graph_edges.rds")
  } else {
    people_summary <- readRDS("../input/people_summary.rds")
  }
  
  print(head(people_summary))
  hist_borrower_strength <- data.frame(Borrower.Strength = people_summary$borrower_strength[!is.na(people_summary$borrower_strength)])
  hist_lender_weakness <-   data.frame(Lender.Weakness = people_summary$lender_weakness[!is.na(people_summary$lender_weakness)])
  
  library("ggplot2")
  print("plotting the distributions")
  ggplot(data=hist_borrower_strength, aes(Borrower.Strength)) + geom_histogram()
  ggplot(data=hist_lender_weakness, aes(Lender.Weakness)) + geom_histogram()
  
  print("computing the borrowed amount")
  borrowed_amount_per_warranter <- 1000
  people_summary$borrowed_amount <- people_summary$borrower_strength*borrowed_amount_per_warranter
  people_summary$borrowed_amount[is.na(people_summary$borrowed_amount)] <- 0
  
  people_summary$startingDate <- sample(seq(as.Date('2016/01/01'), as.Date('2017/01/01'), by="day"), dim(people_summary)[1])
  
  people_summary$rate <- rnorm(dim(people_summary)[1],7,0.5)
  people_summary$monthly_reimbursed_amount <-floor(runif(dim(people_summary)[1], min = 500, max = 700))
  
  
  print("First simulation without the default")
  simulated_days <- seq(as.Date('2017/01/01'), as.Date('2017/05/01'), by="day")
  # library("hashmap")
  # customer_loans <- hashmap(people_summary$name,people_summary$name)
  customer_loans <- new.env(hash=T, parent=emptyenv())
  flows_matrix <- NULL
  daily_flow_asof_2017 <- NULL
  for (client_index in 1:dim(people_summary)[1]){
    if(people_summary$isBorrower[client_index]){
      name <- people_summary$name[client_index]
      startingDate <- people_summary$startingDate[client_index]
      borrowed_amount <- people_summary$borrowed_amount[client_index]
      rate <- people_summary$rate[client_index]
      
      month <- month(as.POSIXlt(startingDate, format="%Y/%m/%d"))
      day <- day(as.POSIXlt(startingDate, format="%Y/%m/%d"))
      year <- year(as.POSIXlt(startingDate, format="%Y/%m/%d"))
      
      print("Monthly flow")
      monthly_reimbursed_amount <- people_summary$monthly_reimbursed_amount[client_index]
      print(monthly_reimbursed_amount)
      
      print("rate")
      print(rate)
      
      print("Number of monthly payments")
      nb_mensualities <- ceiling((1+rate/100)*borrowed_amount/monthly_reimbursed_amount)
      print(nb_mensualities)
      
      payment_schedule <- seq(as.Date(startingDate), by = "month", length.out = nb_mensualities+1)
      
      cust_daily_flow_asof_2017 <- data.frame(dates = seq(as.Date("2016/01/01"), as.Date("2018/01/01"),by = "day"), customer = name, flows = 0)
      
      initiating <- TRUE
      for (daily_date_index in 1:dim(cust_daily_flow_asof_2017)[1]){
        matching_index <- cust_daily_flow_asof_2017$dates[daily_date_index] == as.character(payment_schedule)
        if (sum(matching_index)>0){
          if(initiating){
            initiating <- FALSE
            cust_daily_flow_asof_2017$flows[daily_date_index] <- -borrowed_amount
          } else {
            cust_daily_flow_asof_2017$flows[daily_date_index] <- monthly_reimbursed_amount
          }
        }
      }
      
      if(is.null(daily_flow_asof_2017)){
        daily_flow_asof_2017 <- cust_daily_flow_asof_2017
      } else {
        daily_flow_asof_2017 <- rbind(daily_flow_asof_2017,cust_daily_flow_asof_2017)
      }
      
      lending_contract <- list()
      lending_contract$startingDate <- startingDate
      lending_contract$borrowed_amount <- borrowed_amount
      lending_contract$name <- name
      lending_contract$rate <- rate
      lending_contract$payment_schedule <- payment_schedule
      lending_contract$nb_mensualities <- nb_mensualities
      lending_contract$monthly_reimbursed_amount <- monthly_reimbursed_amount
      
      customer_loans[[as.character(name)]] <- lending_contract
      
    }
  }
  
  print("reordering the flow matrix")
  
  
  daily_flow_asof_2017 <- dcast(daily_flow_asof_2017, dates ~ customer, value.var = "flows", fun.aggregate = sum)
  print("flow matrix")
  print(dim(daily_flow_asof_2017))
  print(head(daily_flow_asof_2017))
  print("done")
  
  saveRDS(daily_flow_asof_2017, "../input/daily_flow_asof_2017.rds")
  
  ########################################################################
  ########################################################################
  ######################## simulation without default
  ########################################################################
  ########################################################################
  
  print("simulation without defaults")
  
  neg_flows <- daily_flow_asof_2017[,2:dim(daily_flow_asof_2017)[2]]
  pos_flows <- daily_flow_asof_2017[,2:dim(daily_flow_asof_2017)[2]]
  
  neg_flows[neg_flows > 0] <- 0
  pos_flows[pos_flows < 0] <- 0
  
  outFlows <- rowSums(neg_flows)
  inFlows <- rowSums(pos_flows)
  inOutFlows <- data.frame(dates=daily_flow_asof_2017$dates,without_default_outFlows=outFlows,without_default_inFlows=inFlows)
  
  print(dim(inOutFlows))
  print(head(inOutFlows))
  print(tail(inOutFlows))
  
  cumInOutFlows <- inOutFlows
  cumInOutFlows$without_default_inFlows <- cumsum(cumInOutFlows$without_default_inFlows)
  cumInOutFlows$without_default_outFlows <- cumsum(cumInOutFlows$without_default_outFlows)
  
  saveRDS(cumInOutFlows, "../input/without_default_cumInOutFlows.rds")
  
  print(tail(cumInOutFlows))
  
  g <- ggplot(cumInOutFlows) + geom_line(aes(dates, without_default_outFlows))  + geom_line(aes(dates, without_default_inFlows))
  
  print(g)
  
  ########################################################################
  ########################################################################
  ######################## simulation with default
  ########################################################################
  ########################################################################
} else {
  print("Simulation with defaults")
  borrowed_amount_per_warranter <- 1000
  daily_flow_asof_2017 <- readRDS("../input/daily_flow_asof_2017.rds")
  people_summary <- readRDS("../input/people_summary.rds")
  bsk.network <- readRDS("../input/people_graph.rds")
  withoutdefault_cumInOutFlows <- readRDS("../input/without_default_cumInOutFlows.rds")
  bsk <- readRDS("../input/people_graph_edges.rds")
  bsk$warranter <- as.character(bsk$warranter)
  
  nb_days <- dim(daily_flow_asof_2017)[1]
  daily_default_asof_2017 <- daily_flow_asof_2017
  rescaling_factor <- 2.5
  people_summary$default_probability <- people_summary$default_probability/(nb_days/rescaling_factor)
  print("simulating default for the customers")
  defaulting_customers <- c()
  for (date_index in 1:nb_days){


    borrowing_customers <- data.frame(name=colnames(daily_flow_asof_2017)[-1])
    borrowing_customers <- merge(borrowing_customers,people_summary,all.x=TRUE,sort=FALSE,by="name")
    # print("we should have here a proper assessment of the customers default probability")
    borrowing_customers <- borrowing_customers[,c("name","default_probability")]
    
    
    random_draw <- function(p){
      default_proba <- rbinom(n=1,size=1,prob=p)
      return(default_proba)
    }
    
    computeCustomerDefault <- function(x) {
      customer_default <- random_draw(as.numeric(x["default_probability"]))
      return(customer_default)
    }
    
    customer_defaults <- apply(X = borrowing_customers,MARGIN = 1,FUN =computeCustomerDefault)
    if (sum(customer_defaults)>0){
      defaulting_customer_name <- as.character(borrowing_customers$name[customer_defaults>0])
      print("customer default")
      print("Date")
      defaulting_date <- daily_flow_asof_2017$dates[date_index]
      print(defaulting_date)
      print("defaulting customer")
      print(defaulting_customer_name)
      
      daily_flow_asof_2017[daily_flow_asof_2017$dates >= defaulting_date, as.character(defaulting_customer_name)] <- 0
      
      nb_warranter <- dim(bsk[bsk$warranter == defaulting_customer_name,])[1]
      daily_flow_asof_2017[date_index, as.character(defaulting_customer_name)] <- nb_warranter*borrowed_amount_per_warranter/2
      
      defaulting_customer_name <- borrowing_customers$name[customer_defaults>0]
      defaulting_customers <- c(defaulting_customers,as.character(defaulting_customer_name))
      V(bsk.network)$color <- ifelse(V(bsk.network)$isBorrower, 'blue','green') #useful for highlighting certain people. Works by matching the name attribute of the vertex to the one specified in the 'ifelse' expression
      V(bsk.network)$color[V(bsk.network)$name %in% defaulting_customers] <- "red"
      V(bsk.network)$size <- V(bsk.network)$strength
      
      plot(bsk.network, #the graph to be plotted
           layout=layout.fruchterman.reingold, # the layout method. see the igraph documentation for details
           main='Warranter/warrantee network', #specifies the title
           vertex.label.dist=0.5, #puts the name labels slightly off the dots
           vertex.frame.color='blue', #the color of the border of the dots 
           vertex.label.color='black', #the color of the name labels
           vertex.label.font=2, #the font of the name labels
           vertex.label=V(bsk.network)$name, #specifies the lables of the vertices. in this case the 'name' attribute is used
           vertex.label.cex=1 #specifies the size of the font of the labels. can also be made to vary
      )
      
    }
    daily_default_asof_2017[date_index,-1] <- customer_defaults
  }
  
  print("Acknowledging the flows after default simulation")
  neg_flows <- daily_flow_asof_2017[,2:dim(daily_flow_asof_2017)[2]]
  pos_flows <- daily_flow_asof_2017[,2:dim(daily_flow_asof_2017)[2]]
  
  default_flows <- daily_default_asof_2017[,2:dim(daily_flow_asof_2017)[2]]
  default_flows <- sapply(X = default_flows, FUN = function(x){return(1-cumsum(x))})

  
  neg_flows[neg_flows > 0] <- 0
  pos_flows[pos_flows < 0] <- 0
  inFlowsWithoutWarranter <- rowSums(pos_flows*(default_flows))
  inFlows <- rowSums(pos_flows)
  outFlows <- rowSums(neg_flows)

  # outFlowsWithoutWarranter[outFlowsWithoutWarranter < 0] <- 0
  
  inOutFlows <- data.frame(dates=daily_flow_asof_2017$dates,outFlows=outFlows,inFlowsWithoutWarranter=inFlowsWithoutWarranter,inFlows=inFlows)
  
  print(dim(inOutFlows))
  print(head(inOutFlows))
  print(tail(inOutFlows))
  
  cumInOutFlows <- inOutFlows
  cumInOutFlows$inFlows <- cumsum(cumInOutFlows$inFlows)
  cumInOutFlows$inFlowsWithoutWarranter <- cumsum(cumInOutFlows$inFlowsWithoutWarranter)
  cumInOutFlows$outFlows <- cumsum(cumInOutFlows$outFlows)
  
  print(tail(cumInOutFlows))
  print(tail(withoutdefault_cumInOutFlows))
  
  cumInOutFlows <- merge(cumInOutFlows,withoutdefault_cumInOutFlows,by="dates")
  cumInOutFlows$without_default_outFlows <- NULL
  
  g <- ggplot(cumInOutFlows) + geom_line(aes(dates, outFlows)) + geom_line(aes(dates, inFlows)) + geom_line(aes(dates, inFlowsWithoutWarranter))
  print(g)
  g <- g + geom_line(aes(dates, without_default_inFlows))
  print(g)
  
  dd = melt(cumInOutFlows, id=c("dates"))
  
  gg <- ggplot(dd) + geom_line(aes(x=dates, y=value, colour=variable))
  print(gg)
}


