.PHONY: test
test:
	python -m tornado.testing discover

.PHONY: clean
clean:
	find . -name "*.pyc" -delete
