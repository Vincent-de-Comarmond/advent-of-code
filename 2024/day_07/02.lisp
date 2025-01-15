(ql:quickload "str")

(defun parse-junky-int (c)
  (parse-integer c :junk-allowed T))

(defun to-string (c)
  (write-to-string c))

(defun split-line (ln)
  (str:split #\Space ln :omit-nulls T))

(defun power-set (accumulator power &optional symbol-set)
  (if (null symbol-set)  (setf symbol-set (mapcar 'first accumulator)))
  (if (<= power 1) (return-from power-set accumulator))
  (let ((tmp '()))
    (loop for branch in accumulator do
      (loop for symbol in symbol-set do
	(let ((copy (copy-list branch)))
	  (push symbol copy)
	  (push copy tmp)))
      (setf accumulator tmp)))
  (power-set accumulator (1- power) symbol-set))

(defun custom-reduce (function-list number-list &optional accumulator)
	   (if (null accumulator)
	       (setf accumulator (pop number-list)))
	   (if (= 0 (length number-list)) accumulator
	       (custom-reduce (rest function-list)
			      (rest number-list)
			      (funcall (car function-list)
				       accumulator (car number-list)))))

(defun concat (a b)
  (parse-junky-int (str:concat (to-string a) (to-string b))))


(defun validity-score (target components)
  (let ((possibilities (power-set '((+) (*) (concat)) (1- (length components)))))
    (loop for combo in possibilities do
      (if (= target (custom-reduce combo components))
	  (return-from validity-score target))))
  0)

(with-open-file (stream "./input.txt")
  (let ((valid-records '()))
    (do ((line (read-line stream nil) (read-line stream nil)))
	((not line)) ;; not nil ... i.e. a line has been read from the stream
      (let* ((record (mapcar 'parse-junky-int (split-line line)))
	     (target (first record))
	     (components (rest record)))
	(push (validity-score target components) valid-records)))
    (reduce '+ valid-records)))

;; 159490400628354 is the correct answer
