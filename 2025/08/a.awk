BEGIN {
	FS = ","
	split("", boxes, "")
	split("", distances, "")
}

{
	for (i = 1; i <= 3; i++) {
		boxes[NR][i] = $i
	}
	for (j = 1; j < NR; j++) {
		dist = ($1 - boxes[j][1]) ^ 2 + ($2 - boxes[j][2]) ^ 2 + ($3 - boxes[j][3]) ^ 2
		distances[NR, j] = dist
		distances[j, NR] = dist
	}
}

END {
	n = asorti(distances, dist_sorted, "@val_num_asc")
	split("", circuits, "")
	connections = 0
	split("", groups, "")
	num_groups = 0
	for (i = 1; i <= n; i += 2) {
		connections++
		split(dist_sorted[i], pair, SUBSEP)
		a = pair[1]
		b = pair[2]
		agroup = -1
		bgroup = -1
		for (j in groups) {
			if (0 < agroup && 0 < bgroup) {
				break
			}
			if (agroup < 0 && a in groups[j]) {
				agroup = j
			}
			if (bgroup < 0 && b in groups[j]) {
				bgroup = j
			}
		}
		# print agroup
		# print bgroup
		if (agroup == bgroup && agroup < 0) {
			# Start
			num_groups++
			groups[num_groups][a] = 1
			groups[num_groups][b] = 1
		} else if (agroup == bgroup && 0 < agroup) {
			# connections--
		} else if (0 < agroup && bgroup < 0) {
			groups[agroup][b] = 1
		} else if (agroup < 0 && 0 < bgroup) {
			groups[bgroup][a] = 1
		} else {
			for (k in groups[bgroup]) {
				groups[agroup][k] = 1
			}
			delete groups[bgroup]
		}
		if (1000 <= connections) {
			break
		}
	}
	idx = 1
	split("", group_sizes, "")
	for (j in groups) {
		group_sizes[idx++] = length(groups[j])
	}
	split("", group_sizes_sorted, "")
	n = asort(group_sizes, group_sizes_sorted, "@val_num_desc")
	box_group_power = 1
	for (i = 1; i <= 3; i++) {
		box_group_power *= group_sizes_sorted[i]
	}
	print "Boxes multiplied:", box_group_power
	# 26400 is the right answer for part 1
}


function add_dist(box1_id, box2_id, a, b, dist_sq)
{
	split(boxes[box1_id], a, ",")
	split(boxes[box2_id], b, ",")
	dist_sq = (a[1] - b[1]) ^ 2 + (a[2] - b[2]) ^ 2 + (a[3] - b[3]) ^ 2
	distances[box1_id, box2_id] = dist_sq
	distances[box2_id, box1_id] = dist_sq
}
