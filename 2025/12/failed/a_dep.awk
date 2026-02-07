BEGIN {
	FS = ""
	split("", shapes, FS)
	split("", gallery, FS)
	split("", optimal_packs, FS)
	row_idx = 1
	pres_idx = 1
}

/#|\./ {
	shapes[pres_idx][row_idx][1] = $1 == "#" ? 1 : 0
	shapes[pres_idx][row_idx][2] = $2 == "#" ? 1 : 0
	shapes[pres_idx][row_idx][3] = $3 == "#" ? 1 : 0
	row_idx++
	if (3 < row_idx) {
		add_to_gallery(pres_idx)
		pres_idx++
		row_idx = 1
	}
}

/x/ {
	gsub(/:/, "", $0)
	gsub(/x/, " ", $0)
	split($0, a, " ")
	#
	split("", desired, FS)
	for (i = 3; i <= length(a); i++) {
		desired[i - 2] = a[i]+1
	}
	# solve_one(a[1], a[2], desired)
}

END {
	for (i in gallery) {
		for (j in gallery[i]) {
			printf "Basis: %d, %d\n", i, j
			print_matrix(gallery[i][j])
			print ""
		}
	}
	# for (i = 1; i <= length(gallery); i++) {
	# 	for (j = 1; j <= length(gallery[i]); j++) {
	# 		if (j == 1) {
	# 			print "#####\nBASIS\n#####"
	# 		}
	# 		print i, j
	# 		print_matrix(gallery[i][j])
	# 		print ""
	# 	}
	# }
}


function add_to_gallery(present_index, idx, rep)
{
	#############
	# rotations #
	#############
	split("", rot1, FS)
	split("", rot2, FS)
	split("", rot3, FS)
	rotate(shapes[present_index], rot1)
	rotate(rot1, rot2)
	rotate(rot2, rot3)
	# flip
	split("", flipped, FS)
	flip(shapes[present_index], flipped)
	#####################
	# flipped_rotations #
	#####################
	split("", frot1, FS)
	split("", frot2, FS)
	split("", frot3, FS)
	rotate(flipped, frot1)
	rotate(frot1, frot2)
	rotate(frot2, frot3)
	#############################################################
	# force awk to treat gallery as a minimum 3 dimension array #
	#############################################################
	for (idx = 1; idx <= 8; idx++) {
		gallery[present_index][idx][-1] = -1
	}
	##################
	# add to gallery #
	##################
	idx = 1
	split("", deduplicator, FS)
	copy_matrix(shapes[present_index], gallery[present_index][idx])
	deduplicator[matrixtostring(shapes[present_index])] = 1
	idx++
	rep = matrixtostring(rot1)
	if (! (rep in deduplicator)) {
		copy_matrix(rot1, gallery[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(rot2)
	if (! (rep in deduplicator)) {
		copy_matrix(rot2, gallery[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(rot3)
	if (! (rep in deduplicator)) {
		copy_matrix(rot3, gallery[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(flipped)
	if (! (rep in deduplicator)) {
		copy_matrix(flipped, gallery[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(frot1)
	if (! (rep in deduplicator)) {
		copy_matrix(frot1, gallery[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(frot2)
	if (! (rep in deduplicator)) {
		copy_matrix(frot2, gallery[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(frot3)
	if (! (rep in deduplicator)) {
		copy_matrix(frot3, gallery[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	for (idx = 1; idx <= 8; idx++) {
		delete gallery[present_index][idx][-1]
		if (length(gallery[present_index][idx]) == 0) {
			delete gallery[present_index][idx]
		}
	}
}

function copy_matrix(input, output, i, j)
{
	split("", output, FS)
	for (i = 1; i <= length(input); i++) {
		for (j = 1; j <= length(input[1]); j++) {
			output[i][j] = input[i][j]
		}
	}
}

function flip(input, output, i, j)
{
	make_canvas(length(input[1]), length(input), output)
	output[1][1] = input[1][3]
	output[1][2] = input[1][2]
	output[1][3] = input[1][1]
	output[2][1] = input[2][3]
	output[2][2] = input[2][2]
	output[2][3] = input[2][1]
	output[3][1] = input[3][3]
	output[3][2] = input[3][2]
	output[3][3] = input[3][1]
}

# function solve(desired, region, base, i)
# {
#     while (0 < length(desired)){
# 	for (i in desired) {
# 	    if (desired[i] == 0) {
# 		delete desired[i]
# 		continue
# 	    }
# 	    desired[i] -= 1
# 	    base = shapes[i]



# 	    for 



# 	}
#     }


# 	print "Width x Length:", _width, _length
# 	for (i in desired) {
# 		if (desired[i] == 0) {
# 			continue
# 		}
# 		split("", region, FS)
# 		make_region(_width, _length, region)





# 	}
# }
function make_canvas(_width, _length, region_matrix, i, j)
{
	split("", region_matrix, FS)
	for (i = 1; i <= _length; i++) {
		for (j = 1; j <= _width; j++) {
			region_matrix[i][j] = 0
		}
	}
}

function make_optimal_pack(_length, _width, pack1, pack2, idx, _end, i, j, k, added,  s1, s2, l, m)
{ 
    if (!isarray(pack1) || !isarray(pack2)) {
		split("", pack1, FS)
		split("", pack2)
		make_canvas(_width, _length, pack1)
		return make_optimal_pack(_length, _width, pack1, pack2)
	}

    added = 0
	for (i in pack1){
	    for (j in pack1[i]){
		for (k in pack1[i][j])
		    if (pack1[i][j][k] != 0){
			continue
		    }

		for (s1 in gallery){
		    for (s2 in gallery[s1]){
			for 

			
		    }
		}
		


		
		
		
	    }
	}

	
	split("", canvas, FS)
	make_canvas(_width, _length, canvas)
	for (i = 1; i <= length(canvas); i++) {
		for (j = 1; j <= length(canvas[0]); j++) {
		}
	}
}

function matrixtostring(input_matrix, output, i, j)
{
	output = ""
	for (i = 1; i <= length(input_matrix); i++) {
		for (j = 1; j <= length(input_matrix[1]); j++) {
			output = output input_matrix[i][j]
		}
	}
	return output
}

function print_matrix(matrix, _i, _j)
{
	for (_i = 1; _i <= length(matrix); _i++) {
		for (_j = 1; _j <= length(matrix[1]); _j++) {
			printf matrix[_i][_j]
		}
		print ""
	}
}

function rotate(input, output, i, j)
{
	make_canvas(length(input[1]), length(input), output)
	output[1][1] = input[1][3]
	output[1][2] = input[2][3]
	output[1][3] = input[3][3]
	output[2][1] = input[1][2]
	output[2][2] = input[2][2]
	output[2][3] = input[3][2]
	output[3][1] = input[1][1]
	output[3][2] = input[2][1]
	output[3][3] = input[3][1]
}
