(ql:quickload "str")

(defun differences (record-list)
  (mapcar '- (rest record-list) (subseq record-list 0 (1- (length record-list)))))

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

(defun remove-element (n list)
	   (remove-if (constantly t) list :start n :count 1))

(defun anysafe (record-list index)
  (cond
    ((>= index (length record-list)) 0)
    ((= 1 (issafe (differences (remove-element index record-list)))) 1)
    (t (anysafe record-list (1+ index)))))


(with-open-file (stream "./input.txt")
  (let* ((total 0))
    (do ((line (read-line stream nil) (read-line stream nil)))
	((not line)) ;; not nil ... i.e. a line has been read from the stream
      (let ((tmp (mapcar 'parse-integer (str:split #\Space line :omit-nulls 'true))))
	(if (= 1 (issafe (differences tmp)))
	    (setf total (1+ total))
	    (setf total (+ total (anysafe tmp 0))))))
    (print total)))

;; Correct answer is 577
