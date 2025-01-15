(defun custom-make-list (digit-char fill-char)
  (make-list (digit-char-p digit-char) :initial-element fill-char))

(defun first-null (input-list)
  (position nil input-list))

(defun last-nonnull (input-list)
  (position-if-not (lambda (x) (null x)) input-list :from-end 'end))

(defun organize-list (input-list)
  (let* ((null-first (first-null input-list))
	 (nonnull-last (last-nonnull input-list)))
    (if (<= nonnull-last null-first) (return-from organize-list input-list))
    (setf (nth null-first input-list) (nth nonnull-last input-list))
    (setf (nth nonnull-last input-list) nil)
    (organize-list input-list)))


(defun multiply-by-index (input-list &optional (current-idx 0) (accumulator '()))
  (if (= (length accumulator) (length input-list)) (reverse accumulator)
      (multiply-by-index
       input-list
       (1+ current-idx)
       (push (* current-idx (nth current-idx input-list)) accumulator))))
  

(with-open-file (stream "./input.txt")
  (let ((index 0)
	(parity 0)
	(expanded '()))
    (do ((char (read-char stream nil) (read-char stream nil)))
	((or (not char) (eql char #\Newline))) ;; read a char from the stream
      (if (= 0 parity)
	  (setf expanded (concatenate 'list expanded (custom-make-list char index)))
	  (setf expanded (concatenate 'list expanded (custom-make-list char nil))))
      (setf parity (mod (1+ parity) 2))
      (if (= 1 parity) (setf index (1+ index))))
    (reduce '+ (multiply-by-index (remove nil (organize-list expanded))))))

;; 6288599492129 is the correct answer
