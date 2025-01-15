declare -A resolved
declare -A operations

while read -r key value; do
	resolved["$key"]="$value"
done < <(grep ":" "$1" | tr -d ":")

while read -r output inputs; do
	operations["$output"]="$inputs"
done < <(grep "\->" "$1" |
	sed -e 's/\(.*\) -> \(.*\)/\2 \1/g' -e 's/XOR/^/' -e 's/AND/\&/' -e 's/OR/|/')

while ((${#operations[@]} > 0)); do
	echo "Number unresolved: ${#operations[@]}"
	for key in "${!operations[@]}"; do
		value="${operations[$key]}"
		read -r input1 operation input2 <<<"$value"
		if [[ -v "resolved[$input1]" ]] && [[ -v "resolved[$input2]" ]]; then
			# NOTE: can't use mathematical expression here as it doesn't correctly resolve the dynamic operator
			let "result=${resolved[$input1]} $operation ${resolved[$input2]}"
			resolved["$key"]="$result"
			unset "operations[$key]"
		fi
	done
done

binary=$(typeset -p resolved |
	tr " " "\n" |
	tr -d \" |
	grep -Eo "\[z.*" |
	sort -r |
	cut -d = -f2 |
	paste -s -d "")

echo "$((2#$binary))"
# 52728619468518 is the right answer for part 1
