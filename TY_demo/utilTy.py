from operator import itemgetter

def find_best_data(id_score_date, limit=7):
	
	#take a list of tuple in the form of id, score, date 
	#sort primarily by the date, then by score
	result = []
	id_score_date_mod = [(x[0], int(x[1]/10), x[2]) for x in id_score_date]
	for x in sorted(sorted(id_score_date_mod,key=itemgetter(2),reverse=True), key=itemgetter(1), reverse=True):
		#print(x)
		result.append(x[0])
	return result[:limit]

def main():
	dummy = [(1,71.0,201809),(2,50.0,201801),(3,45.5,201808),(4,45.5,201809),(5,32.0,201808)]
	print(find_best_data(dummy))
	return 
	
if __name__ == "__main__":
    main()
