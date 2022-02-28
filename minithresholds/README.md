### Instructions:  
* Start the container  
  `docker-compose up -d`
* Enter the container  
  `docker exec -it minizn bash`
* Solve model with chuffed  
  `minizinc --data scores.dzn --solver chuffed model.mzn`
