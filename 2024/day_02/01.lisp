(ql:quickload "str")

(defun differences (record-list)
  (mapcar '- (subseq record-list 0 (1- (length record-list))) (rest record-list)))

(defun issafe (difference-list &optional previous)
  (if (null difference-list)
      1
      (let* ((current (car difference-list))
	     (current-abs (abs current)))
	(cond
	  ((<= current-abs 0 ) 0)
	  ((> current-abs 3) 0)
	  ((and previous (< (* current previous) 0)) 0)
	  (t (issafe (rest difference-list) (car difference-list)))))))

(with-open-file (stream "./input.txt")
  (let* ((total 0))
    (do ((line (read-line stream nil) (read-line stream nil)))
	((not line)) ;; not nil ... i.e. a line has been read from the stream
      (let ((tmp (mapcar 'parse-integer (str:split #\Space line :omit-nulls 'true))))
	(setf total (+ total (issafe (differences tmp))))))
    (print total)))

;; Correct answer is 534
