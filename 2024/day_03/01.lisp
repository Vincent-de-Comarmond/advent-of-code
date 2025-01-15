(defun digit-or-comma (input-char)
  (or (digit-char-p input-char) (eql #\, input-char)))

(defun digit-or-close (input-char)
  (or (digit-char-p input-char) (eql #\) input-char)))

(defun str-char+ (str-in char-in)
  (concatenate 'string str-in (string char-in)))

(defun digit-1 (char-in number-1)
  (and (digit-char-p char-in) (not (null number-1))))

(defun digit-not-1 (char-in number-1)
  (and (digit-char-p char-in) (null number-1)))

(defun add-element (accumulator number-1 number-2-string)
  (+ accumulator (* number-1 (parse-integer number-2-string))))

(defmacro expect (c)
  `(lambda (x) (eql x ,c)))

(defun parser (stream-in expect-func &optional (accum 0) (num-buf "") (num-1 nil))
  (let ((char (read-char stream-in nil)))
    (cond
      ;; Return the accumulated value if we hit the end of the stream
      ((null char) accum)
      ;; reset if we don't read the expected character
      ((not (funcall expect-func char))
       (parser stream-in (expect #\m) accum))

      ((eql char #\m)
       (parser stream-in (expect #\u) accum))

      ((eql char #\u)
       (parser stream-in (expect #\l) accum))

      ((eql char #\l)
       (parser stream-in (expect #\() accum))

      ((eql char #\()
       (parser stream-in 'digit-char-p accum))

      ((digit-not-1 char num-1)
       (parser stream-in 'digit-or-comma accum  (str-char+ num-buf char)))

      ((eql char #\,)
       (parser stream-in 'digit-char-p accum "" (parse-integer num-buf)))

      ((digit-1 char num-1)
       (parser stream-in 'digit-or-close accum (str-char+ num-buf char) num-1))

      ((eql char #\))
       (parser stream-in (expect #\m) (add-element accum num-1 num-buf) ""))

      (t (parser stream-in (expect #\m) accum))))) 

(with-open-file (stream "./input.txt")
    (format t "~d~%" (parser stream (expect #\m ))))

;;;; 167090022 is the right answer for part1
