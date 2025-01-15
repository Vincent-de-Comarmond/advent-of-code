(defun next-pseudorandom (current)
  (let* ((step1 (mod (logxor (* current 64) current) 16777216))
	 (step2 (mod (logxor (floor step1 32) step1) 16777216)))
    (mod (logxor (* step2 2048) step2) 16777216)))

(defun nth-pseudorandom (seed number)
  (if (<= number 0)
      seed
      (nth-pseudorandom (next-pseudorandom seed) (1- number))))

(with-open-file (stream "./input.txt")
  (let ((cache (make-hash-table))
	(prices '()))
    (do ((line (read-line stream nil) (read-line stream nil)))
	((not line)) ;; not nil ... i.e. a line has been read from the stream
      (let ((seed (parse-integer line)))
	(cond ((gethash seed cache)
	       (push (gethash seed cache) prices))
	      (t (let ((nth-ps (nth-pseudorandom seed 2000)))
		   (push nth-ps prices)
		   (setf (gethash seed cache) nth-ps))))))
    ;; (format t "~a~%" prices)
    (print (reduce '+ prices))))

;; 19150344884 is the correct answer for part 1
;; Also common lisp is tooo damned fast
