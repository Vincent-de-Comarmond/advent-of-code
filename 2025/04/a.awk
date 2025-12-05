BEGIN {
    a=""
    b=""
    c=""
    accessable_paper=0
}
{
    c=b
    b=a
    a=$0
    accessable_paper += count_paper(a, b, c)
}
END {
    c=b
    b=a
    a=""
    accessable_paper += count_paper(a, b, c)
    print "Accessable paper", accessable_bales
}


function count_paper(a, b, c,
                     rowtotal, i, subtotal, j){
    rowtotal=0
    for (i=1; i <=length(b); i++){
        if (substr(b, i, 1) != "@")
            continue
        subtotal=0
        for (j=i-1; j <= i+1; j++) {
            if ((j < 1) || length($0) < j)
                continue
            subtotal += substr(a, j, 1) == "@" ? 1 : 0
            subtotal += substr(c, j, 1) == "@" ? 1 : 0
            subtotal += ((j != i) && (substr(b, j, 1) == "@")) ? 1 : 0
        }
        accessable_bales += (subtotal < 4) ? 1 : 0
    }
    return rowtotal
}

# 1564 is too high for part 1
# 1516 is the right answer for part 1
