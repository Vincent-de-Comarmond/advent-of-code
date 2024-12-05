(ql:quickload "str")
(with-open-file (stream "./input.txt")
  (let* ((hash1 (make-hash-table :test 'equal))
	 (hash2 (make-hash-table :test 'equal)))
    (do ((line (read-line stream nil) (read-line stream nil)))
	((not line)) ;; not nil ... i.e. a line has been read from the stream
      (let* ((tmp (str:split #\Space line :omit-nulls 'true))
	     (k1  (first tmp))
	     (k2  (second tmp)))
	(setf (gethash k1 hash1) (+ 1 (gethash k1 hash1 0)))
	(setf (gethash k2 hash2) (+ 1 (gethash k2 hash2 0)))))
    (let ((total 0))
      (maphash (lambda (k v)
		 (setf total
		       (+ total (* (parse-integer k) v (gethash k hash2 0)))))
	       hash1)
      (print total))))

;; Correct answer is 23387399
