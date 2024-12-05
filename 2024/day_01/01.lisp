(ql:quickload "str")
(with-open-file (stream "./input.txt")
  (let* ((list1 '())
	 (list2 '()))
    (do ((line (read-line stream nil) (read-line stream nil)))
	((not line)) ;; not nil ... i.e. a line has been read from the stream
      (let ((tmp (str:split #\Space line :omit-nulls 'true)))
	(push (parse-integer (first tmp)) list1)
	(push (parse-integer (second tmp)) list2)))
    (let ((list1 (sort list1 #'<))
	  (list2 (sort list2 #'<)))
      (print (reduce '+ (mapcar 'abs (mapcar '- list1 list2)))))))

;; Correct answer is 1197984
