BEGIN {
    total_joltage = 0
}

{
    subtotal = -1
    _length = length($0)
    choose_optimal(1, 1, "")
    total_joltage += subtotal
}

END {
    print "Max Joltage:", total_joltage
}

function choose_optimal(level, start, accumulator,
                        i, level_best, current, end, idx){

    end = _length - 12 + level
    level_best = 0
    if (level == 13){
        subtotal = subtotal < accumulator ? accumulator : subtotal
    } else {
        for (i=start; i <= end; i++){
            current = substr($0, i, 1)
            if (level_best < current){
                level_best = current
                idx = i
            }
        }
        choose_optimal(level + 1, idx + 1, accumulator level_best)
    }
}

# 172601598658203 is the right answer for part 2
