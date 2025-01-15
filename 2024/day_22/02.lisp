(defparameter *ps-cache* (make-hash-table))


(defun next-pseudorandom (current)
  (cond ((gethash current *ps-cache*) (gethash current *ps-cache*))
	(t
	 (let* ((step1 (mod (logxor (* current 64) current) 16777216))
		(step2 (mod (logxor (floor step1 32) step1) 16777216))
		(next (mod (logxor (* step2 2048) step2) 16777216)))
	   (setf (gethash current *ps-cache*) next)
	   next))))

(defun nth-pseudorandom (seed number)
  (if (<= number 0)
      seed
      (nth-pseudorandom (next-pseudorandom seed) (1- number))))

(defun part2-pseudorandom-sequence (seed number &optional (accumulator '()))
  (if (<= number 0)
      (nreverse (mapcar (lambda (x) (mod x 10)) accumulator))
      (let ((next (next-pseudorandom seed)))
	(part2-pseudorandom-sequence next (1- number) (push seed accumulator)))))

(defun make-sequence-hash-tables (sequence &optional (accumulator (make-hash-table :test 'equal)))
   (cond
     ((< (length sequence) 5) accumulator)
     (t
      (let* ((subsequence (subseq sequence 0 5))
	     (deltas (mapcar '- (subseq subsequence 1) (butlast subsequence)))
	     (value (car (last subsequence))))
	(if (not (gethash deltas accumulator))
	    (setf (gethash deltas accumulator) value))
	(make-sequence-hash-tables (subseq sequence 1) accumulator)))))


(with-open-file (stream "./input.txt")
  (let ((sequence-maps '())
	(all-keys (make-hash-table :test 'equal))
	(i 0))
    (do ((line (read-line stream nil) (read-line stream nil)))
	((not line)) ;; not nil ... i.e. a line has been read from the stream
      (let* ((seed (parse-integer line))
	     (ps-map (make-sequence-hash-tables
		      (part2-pseudorandom-sequence seed 2000))))
	(push ps-map sequence-maps)
	(maphash (lambda (k v) (setf (gethash k all-keys) v)) ps-map))
      (incf i)
      (if (= 0 (mod i 50))(format t "Completed ~s~%" i)))
    (let ((subsequence-sums '()))
      (maphash
       (lambda (k v)
	 (push
	  (reduce '+ (mapcar (lambda (s) (gethash k s 0)) sequence-maps))
	  subsequence-sums))
       all-keys)
      (print (reduce 'max subsequence-sums)))))

;; 19150344884 is the correct answer for part 1
;; 2121 is the correct answer for part 2
