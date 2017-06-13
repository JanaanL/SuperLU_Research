#!/usr/bin/env python
import os
import sys
import opentuner 
from opentuner import ConfigurationManipulator
from opentuner import EnumParameter
from opentuner import IntegerParameter
from opentuner import MeasurementInterface 
from opentuner import Result
import time
class SuperLUTuner(MeasurementInterface):

    def manipulator(self):
        manipulator = ConfigurationManipulator()

        manipulator.add_parameter(IntegerParameter('nsup', 50, 300))
        manipulator.add_parameter(IntegerParameter('nrel', 10, 40))
        manipulator.add_parameter(IntegerParameter('colperm', 0, 5))
        manipulator.add_parameter(IntegerParameter('lookahead', 0, 10))
        manipulator.add_parameter(IntegerParameter('numthreads', 1, 10))

        '''
   	Parameters for testing SuperLU     
        '''

        return manipulator


    def run(self, desired_result, input, limit):
        cfg = desired_result.configuration.data

	nsupval='{0}'.format(cfg['nsup'])
	os.environ['NSUP']=nsupval
	try:
	    print "NSUP = " + os.environ['NSUP']
	except KeyError:
	    print "No environmental variable set for NSUP"
	    sys.exit(1)

	nrelval='{0}'.format(cfg['nrel'])
	os.environ['NREL']=nrelval
	try:
	    print "NREL = " + os.environ['NREL']
	except KeyError:
	    print "No environmental variable set for NREL"
	    sys.exit(1)
	
	colpermvalue='{0}'.format(cfg['colperm'])
	os.environ['COLPERM']=colpermvalue
	try:
	    print "COLPERM = " + os.environ['COLPERM']
	except KeyError:
	    print "No environmental variable set for COLPERM"
	    sys.exit(1)

	lookaheadvalue='{0}'.format(cfg['lookahead'])
	os.environ['NUM_LOOKAHEADS']=lookaheadvalue
	try:
	    print "NUM_LOOKAHEADS = " + os.environ['NUM_LOOKAHEADS']
	except KeyError:
	    print "No environmental variable set for NUM_LOOKAHEADS"
	    sys.exit(1)

	numthreads='{0}'.format(cfg['numthreads'])
	os.environ['OMP_NUM_THREADS']=numthreads
	try:
	    print "OMP_NUM_THREADS = " + os.environ['OMP_NUM_THREADS']
	except KeyError:
	    print "No environmental variable set for OMP_NUM_THREADS"
	    sys.exit(1)


	#time is the performance measure currently used
        superlu_run = 'mpirun -n 16 pddrive -r 4 -c 4 '
        datafile = os.getenv("HOME")
	datafile += '/Research/DataFiles/Ga19As19H42/Ga19As19H42.rb'
	superlu_run += datafile
	print superlu_run
	run_res = self.call_program(superlu_run)

        assert run_res['returncode'] == 0
        print run_res['stdout']
	return Result(time=run_res['time'])       # 'time' is a built-in metric in OpenTuner, and it's a minimizer

if __name__== '__main__':
    argparser = opentuner.default_argparser()
    SuperLUTuner.main(argparser.parse_args())
