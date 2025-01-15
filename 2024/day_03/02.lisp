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

(defmacro expect (c)
  `(lambda (x) (eql x ,c)))

(defun parse-nums (char expect-func num-buf num-1)
  (cond
    ((not (funcall expect-func char)) (lambda (x) (parse-nums x (expect #\m) "" nil)))
    ((eql char #\m)                   (lambda (x) (parse-nums x (expect #\u) "" nil)))
    ((eql char #\u)                   (lambda (x) (parse-nums x (expect #\l) "" nil)))
    ((eql char #\l)                   (lambda (x) (parse-nums x (expect #\() "" nil)))
    ((eql char #\()                   (lambda (x) (parse-nums x 'digit-char-p "" nil)))
    ((digit-not-1 char num-1)         (lambda (x) (parse-nums x 'digit-or-comma (str-char+ num-buf char) nil)))
    ((eql char #\,)                   (lambda (x) (parse-nums x 'digit-char-p "" (parse-integer num-buf))))
    ((digit-1 char num-1)             (lambda (x) (parse-nums x 'digit-or-close (str-char+ num-buf char) num-1)))
    ((eql char #\))                   (* num-1 (parse-integer num-buf)))
    (T                                (lambda (x) (parse-nums x (expect #\m) "" nil)))))


(defun parse-dont (char expected-func)
  (cond
    ((not (funcall expected-func char)) (lambda (x) (parse-dont x (expect #\d))))
    ((eql char #\d)                     (lambda (x) (parse-dont x (expect #\o))))
    ((eql char #\o)                     (lambda (x) (parse-dont x (expect #\n))))
    ((eql char #\n)                     (lambda (x) (parse-dont x (expect #\'))))
    ((eql char #\')                     (lambda (x) (parse-dont x (expect #\t))))
    ((eql char #\t)                     (lambda (x) (parse-dont x (expect #\())))
    ((eql char #\()                     (lambda (x) (parse-dont x (expect #\)))))
    ((eql char #\))                     nil)
    (T                                  (lambda (x) (parse-dont x (expect #\d))))))

(defun parse-do (char expected-func)
  (cond
    ((not (funcall expected-func char)) (lambda (x) (parse-do x (expect #\d))))
    ((eql char #\d)                     (lambda (x) (parse-do x (expect #\o))))
    ((eql char #\o)                     (lambda (x) (parse-do x (expect #\())))
    ((eql char #\()                     (lambda (x) (parse-do x (expect #\)))))
    ((eql char #\))                     T)
    (T                                  (lambda (x) (parse-do x (expect #\d))))))


(with-open-file (stream "./input.txt")
  (let* ((total 0)
	 (active T)
	 (active-parser (lambda (x) (parse-dont x (expect #\d))))
	 (num-parse (lambda (x) (parse-nums x (expect #\m) "" nil))))

    (do ((char (read-char stream nil) (read-char stream nil)))
	((not char) (eql char #\Newline))
      (let ((next-number (if active (funcall num-parse char)))
	    (next-switch (funcall active-parser char)))
	(cond
	  ((not active))
	  ((functionp next-number) (setf num-parse next-number))
	  ((numberp next-number)
	   (setf total (+ total next-number))
	   (setf num-parse (lambda (x) (parse-nums x (expect #\m) "" nil)))))
	(cond
	  ((functionp next-switch) (setf active-parser next-switch))
	  (t
	   (setf active next-switch)
	   (setf active-parser (if active
				   (lambda (x) (parse-dont x (expect #\d)))
				   (lambda (x) (parse-do x (expect #\d)))))))))
    (format t "~d~%" total)))
