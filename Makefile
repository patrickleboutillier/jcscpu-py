test:
	@cat modules.tests | while read m ; do echo -n $$m: ; \
	 	PYTHONPATH=. python $$m | python sim/sim.py 2>&1 | grep -v -P '^(Ran|\.|-|$$)'; done
	@for m in mcs4/m*.py ; do echo -n $$m: ; \
		PYTHONPATH=. python $$m | python sim/sim.py 2>&1 | grep -v -P '^(Ran|\.|-|$$)'; done