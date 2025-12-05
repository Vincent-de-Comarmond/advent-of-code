BEGIN {
FS=","
total=0
}

{
    for (i=1; i <=NF; i++){
        split($i, limits, "-")
        for (j=limits[1]; j <=limits[2]; j++){
	    split("", seen, "")
	    for (k=1; k <=int(length(j)/2); k++){
		a = substr(j, 0, k)
		b = a
		for (l=1; l < length(j)/k; l++){
		    b = b a
		}

		if (j == b){
		    seen[j] = 1
		}
	    }
	    for (unique in seen)
		total += unique
	}
    }
}



END {
    print("Invalid sum:", total)
}

# 34421651192 is the right answer for part 2
