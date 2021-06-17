test:
	@for m in modules/j*.py ; do echo -n $$m: ; \
		PYTHONPATH=. python $$m | python sim/sim.py 2>&1 | grep -v -P '^(Ran|\.|-|$$)'; done