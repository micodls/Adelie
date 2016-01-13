#!/usr/bin/env python

import textwrap, sys, os, subprocess, re, time

class ArgsParser:
	def __init__(self):
		import argparse

		class CustomFormatter(argparse.RawTextHelpFormatter, argparse.RawDescriptionHelpFormatter) :
			pass

		description = textwrap.dedent('''\
			Everyday OAM commands made easier.

			Available subcommands
			----------------------
			  demangle
			  logs
			  cmake
			  gen
			  build
			  buildall
			  run
			  runall
			  rb
			  co''')

		parser = argparse.ArgumentParser(prog = 'FM',
			usage = '%(prog)s <subcommand> [options][args]',
			formatter_class = CustomFormatter,
			description = description,
			add_help = False)

		subparser = parser.add_subparsers()
		
		# logs
		logs_parser = subparser.add_parser('logs', conflict_handler = 'resolve')
		logs_parser.add_argument('-cmd', default = 'logs', help = argparse.SUPPRESS)
		logs_parser.add_argument('-r', '--release', dest = 'release', type = int, choices = range(2, 4), required = True, help = 'release')
		logs_parser.add_argument('-tc', '--testcase', dest = 'testcase', required = True, help = 'testcase path')
		logs_parser.add_argument('-e', '--explorer', dest = 'explorer', action = 'store_true', default = False, help = 'opens the testcase in explorer')
		
		# cmake
		cmake_parser = subparser.add_parser('cmake', conflict_handler = 'resolve')
		cmake_parser.add_argument('-cmd', default = 'cmake', help = argparse.SUPPRESS)
		cmake_parser.add_argument('-r', '--release', dest = 'release', type = int, choices = range(2, 4), required = True, help = 'release')
		
		# gen
		gen_parser = subparser.add_parser('gen', conflict_handler = 'resolve')
		gen_parser.add_argument('-cmd', default = 'gen', help = argparse.SUPPRESS)
		gen_parser.add_argument('-r', '--release', dest = 'release', type = int, choices = range(2, 4), required = True, help = 'release')
		
		# build
		build_parser = subparser.add_parser('build', conflict_handler = 'resolve')
		build_parser.add_argument('-cmd', default = 'build', help = argparse.SUPPRESS)
		build_parser.add_argument('-w', '--warning', dest = 'warning', action = 'store_true', default = False, help = 'turns warning prints on')
		build_parser.add_argument('-e', '--error', dest = 'error', action = 'store_false', default = True, help = 'turns error prints off')
		build_parser.add_argument('-r', '--release', dest = 'release', type = int, choices = range(2, 4), required = True, help = 'release')
		
		# build all
		buildall_parser = subparser.add_parser('buildall', conflict_handler = 'resolve')
		buildall_parser.add_argument('-cmd', default = 'buildall', help = argparse.SUPPRESS)
		buildall_parser.add_argument('-w', '--warning', dest = 'warning', action = 'store_true', default = False, help = 'turns warning prints on')
		buildall_parser.add_argument('-e', '--error', dest = 'error', action = 'store_false', default = True, help = 'turns error prints off')
		buildall_parser.add_argument('-r', '--release', dest = 'release', type = int, choices = range(2, 4), required = True, help = 'release')
		
		# run
		run_parser = subparser.add_parser('run', conflict_handler = 'resolve')
		run_parser.add_argument('-cmd', default = 'run', help = argparse.SUPPRESS)
		run_parser.add_argument('-tc', '--testcase', dest = 'testcase', required = True, help = 'testcase path')
		run_parser.add_argument('-l', '--leak', dest = 'leak', action = 'store_true', default = False, help = 'turn memory leak detection off')
		
		# run all
		runall_parser = subparser.add_parser('runall', conflict_handler = 'resolve')
		runall_parser.add_argument('-cmd', default = 'runall', help = argparse.SUPPRESS)
		runall_parser.add_argument('-l', '--leak', dest = 'leak', action = 'store_true', default = False, help = 'turn memory leak detection off')
		
		# rb
		rb_parser = subparser.add_parser('rb', conflict_handler = 'resolve')
		rb_parser.add_argument('-cmd', default = 'rb', help = argparse.SUPPRESS)
		rb_parser.add_argument('-r', '--reviewboard', dest = 'rb_id', type = int, help = 'review board id')
		rb_me_group_parser = rb_parser.add_mutually_exclusive_group(required = True)
		rb_me_group_parser.add_argument('-cl', '--changelist', dest = 'changelist', help = 'changelist')
		rb_me_group_parser.add_argument('-d', '--diff', dest = 'diff', help = 'diff')
		
		# fm checkout
		co_parser = subparser.add_parser('co', conflict_handler = 'resolve')
		co_parser.add_argument('-cmd', default = 'co', help = argparse.SUPPRESS)
		co_parser.add_argument('source', nargs='?', help = 'source URL')
		co_parser.add_argument('dest', nargs='?', help = 'dest URL')

		args = parser.parse_args()

		if args.cmd == 'logs' :
			TestCaseOpener(args)
		elif args.cmd == 'cmake' or args.cmd == 'gen' or args.cmd == 'build' or args.cmd == 'buildall' :
			SutCompiler(args)
		elif args.cmd == 'rb' :
			reviewboardPoster(args)
		elif args.cmd == 'run' or args.cmd == 'runall' :
			TestCaseRunner(args)
		elif args.cmd == 'co' :
			if args.source == None :
				print('ERROR: Empty source path! Try FM co [source][dest]')
			else :
				SVNAccessor(args)

class OptParser:
	def __init__(self):
		import optparse


class TestCaseOpener :
	def __init__(self, args) :
		logsPath = '\C_Test\SC_OAM\FM_FaultManagement\MT\logs'
		release = '\FSMr%d' % (args.release)
		fullPath = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir) + logsPath + release + '\\' + self.formatString(args.testcase) + '.log')
		self.openFile(fullPath, args.explorer)

	# regex replace
	def formatString(self, testcase) :
		replace = {'<' : '', '>' : '', ':' : '', '/' : '\\', '`' : '', '\'' : ''}
		replace = dict((re.escape(k), v) for k, v in replace.iteritems())
		pattern = re.compile("|".join(replace.keys()))
		path = pattern.sub(lambda m: replace[re.escape(m.group(0))], testcase)
		return path

	def getDefaultExecutable(self) :
		notepadExe = 'notepad.exe'
		notepadPlusPlusExe = 'notepad++.exe'
		prontoTerminatorExe = 'C:\work\prontoTerminator\ProntoTerminator.exe'
		sublimeText3Exe = 'C:\Program Files (x86)\Sublime Text 3\subl.exe'
		# change if necessary
		if os.path.exists(sublimeText3Exe) :
			return sublimeText3Exe
		elif os.path.exists(prontoTerminatorExe) :
			return prontoTerminatorExe
		elif os.path.exists(notepadPlusPlusExe) :
			return notepadPlusPlusExe
		else :
			return notepadExe

	def openFile(self, path, explorer) :
		if os.path.exists(path) :
			subprocess.call('"%s" %s' % (self.getDefaultExecutable(), path))

			if explorer == True :
				subprocess.Popen(r'explorer /select,"%s"' % (path))
		else :
			print('ERROR: File does not exists. Try running testcase first.')

class TestCaseRunner :
	def __init__(self, args) :
		appExePath = 'C_Test\SC_OAM\FM_FaultManagement\MT\\app\exe'
		os.chdir(os.path.join(os.path.dirname(__file__), os.pardir, appExePath))
		 # change if necessary
		mtCommand = 'FM_FaultManagement_Test.exe --nouserattention --spawn=4 '
		if args.leak == True :
			mtCommand += '--detect_memory_leak=0 '

		if args.cmd == 'run' :
			tcCommand = '-t \"%s\"' % (args.testcase)
			subprocess.call(mtCommand + tcCommand)
		elif args.cmd == 'runall' :
			print('RUNNING ALL... PLEASE BE PATIENT...')
			logCommand = '--output_format=XML --log_level=all '
			f = open(r'test_output.log','w+')
			subprocess.call(mtCommand + logCommand, stdout=f, stderr=f)
			f.close()
			
class SutCompiler :
	def __init__(self, args) :
		self.release = args.release
		self.binPath = os.path.join(os.path.dirname(__file__), os.pardir) + '\C_Application\SC_OAM\\bin_rel%s' % (self.release)
		
		# not working because .bat files are being called on another process
		# self.setEnv()
		
		if args.cmd == 'cmake' :
			self.cmake()
		elif args.cmd == 'gen' :
			self.gen()
		elif args.cmd == 'build' :
			self.build(args.warning, args.error)
		elif args.cmd ==  'buildall' :
			self.cmake()
			self.gen()
			self.build(args.warning, args.error)
	
	def setEnv(self) :
		subprocess.call([r'C:\Program Files (x86)\Microsoft Visual Studio 12.0\Common7\Tools\vsvars32.bat'])
		
	def cmake(self) :
		if self.release == 2 :
			board = 'FCMD'
		else :
			board = 'FCT'

		if os.path.exists(self.binPath) :
			os.chdir(self.binPath)
			subprocess.call('cmake ..')
		else :
			os.mkdir(self.binPath)
			os.chdir(self.binPath)
			# change if necessary
			subprocess.call('cmake .. -G "Visual Studio 12" -DBOARD=%s -DOM_TEST_TYPE=UTMT -DUSE_BM=OFF -DOM_MT_TEST_ENABLE=ON -DINCLUDE_DB_Database=ON -DINCLUDE_FM_FaultManagement=ON' % (board))

	def gen(self) :
		print('GENERATING...')
		try :
			subprocess.call('msbuild /m /verbosity:minimal %s\generate_rhapsody_all.vcxproj' % (self.binPath), shell = True)
		except OSError :
			print('ERROR: run setenv.bat first')
	
	def build(self, warning, error) :
		print('BUILDING...')
		try :
			self.buildFMAndRedirectOutputToFile()
			self.findForWarningOrErrorPrints(warning, error)
		except OSError :
			print('ERROR: run setenv.bat first')
	
	def buildFMAndRedirectOutputToFile(self) :
		f = open(r'%s\FSMr%d_build.log' % (self.binPath, self.release),'w+')
		subprocess.call('msbuild /m /verbosity:minimal %s\T\FM_FaultManagement\FM_FaultManagement_Test.vcxproj' % (self.binPath), shell = True, stdout = f)
		f.close()
	
	def findForWarningOrErrorPrints(self, warning, error) :
		if warning == True :
			self.grepLogsInFile ('warning')
		if error == True :
			self.grepLogsInFile ('error')
			self.grepLogsInFile ('fatal error')
	
	def grepLogsInFile(self, toSearch) :
		for line in open(r'%s\FSMr%d_build.log' % (self.binPath, self.release)) :
			if ": %s" % toSearch in line :
				print('[============================= %s =============================]' % (toSearch.upper()))
				break

		for line in open(r'%s\FSMr%d_build.log' % (self.binPath, self.release)) :
			if ": %s" % toSearch in line :
				print(line)

class reviewboardPoster:
	def __init__(self, args) :
		os.chdir(os.path.join(os.path.dirname(__file__), os.pardir))

		# change if necessary
		rbCommand = 'rbt.cmd post --server=http://omcpservices.wroclaw.nsn-rdnet.net/reviewboard -o'

		if args.changelist != None :
			rbCommand = rbCommand + ' --svn-changelist=%s' % (args.changelist)
		elif args.diff  != None :
			rbCommand = rbCommand + ' --diff-filename=%s' % (args.diff)
		
		if args.rb_id != None :
			rbCommand = rbCommand + ' -r %d' % (args.rb_id)
		else :
			rbCommand = rbCommand + ' --target-groups="NIMASOPER_EXT_FM, WR_INDIA" --target-people="penaflor, nirza, iang, lewowski" --testing-done=MT/UT'

		subprocess.call(rbCommand)

class SVNAccessor :
	def __init__(self, args) :
		# change if necessary
		workPath = 'D:\\userdata\\pdelos\\work'
		
		if os.path.exists(workPath) :
			os.chdir(workPath)

		if args.dest != None :
			dest = args.dest
		else :
			dest = args.source[args.source.rfind('/')+1:]

		if os.path.exists(os.path.join(workPath, dest)) :
			print('ERROR: %s already exist' % (os.path.join(workPath, dest)))
		else :
			checkout(args.source, dest)

		# relocate
		# https://mnisop50.apac.nsn-net.net/isource/svnroot/BTS_SC_OAM/WCDMA/branches/users/penaflor/CNI1441v1.3
		# http://svne1.access.nsn.com/isource/svnroot/BTS_SC_OAM/WCDMA/branches/users/penaflor/CNI1441v1
		# https://mnisop50.apac.nsn-net.net/isource/svnroot/BTS_SC_OAM/WCDMA/trunk
		# https://mnisop50.apac.nsn-net.net/isource/svnroot/BTS_SC_OAM/WCDMA/branches/maintenance/WN9.1_0000
		# \\mnlinn60.apac.nsn-net.net
		# svn sw --relocate https://mnisop50.apac.nsn-net.net/isource/svnroot/BTS_SC_OAM http://svne1.access.nsn.com/isource/svnroot/BTS_SC_OAM
		# rm -rf `svn status --no-ignore | grep '^[\?I]' | sed 's/^[\?I]//'`

def checkout(source, dest) :
	subprocess.call('svn checkout %s %s --depth empty' % (source, dest))

	subprocess.call('svn update --set-depth infinity %s/C_Application' % (dest))

	# change if necessary
	subprocess.call('svn update --set-depth immediates --parents %s/C_Test/' % (dest))
	subprocess.call('svn update --set-depth files --parents %s/C_Test/SC_OAM' % (dest))
	subprocess.call('svn update --set-depth infinity --parents %s/C_Test/SC_OAM/CoreMT' % (dest))
	subprocess.call('svn update --set-depth infinity --parents %s/C_Test/SC_OAM/FM_FaultManagement' % (dest))
	subprocess.call('svn update --set-depth infinity --parents %s/C_Test/SC_OAM/MT_COMMONS' % (dest))
	subprocess.call('svn update --set-depth infinity --parents %s/C_Test/SC_OAM/SSW_FML_Workaround' % (dest))
	subprocess.call('svn update --set-depth infinity --parents %s/C_Test/SC_OAM/SSW_SupportSoftware' % (dest))
	subprocess.call('svn update --set-depth infinity --parents %s/C_Test/SC_OAM/SSW_WORKAROUND' % (dest))
	subprocess.call('svn update --set-depth infinity --parents %s/C_Test/SC_OAM/UT_Commons' % (dest))

	subprocess.call('svn update --set-depth infinity %s/I_Interface' % (dest))
	subprocess.call('svn update --set-depth infinity %s/E_External' % (dest))

class Timer :
	def __init__(self) :
		self.startTime = time.time()
	
	def printElapsedTime(self) :
		min, sec = divmod((time.time() - self.startTime), 60)
		print('Elapsed time: %dm %ds' % (min, sec))

# custom action class
# class ClassName(argparse.Action) :
	# def __init__(self, option_strings, dest, nargs = None, **kwargs) :
		 # super(ClassName, self).__init__(option_strings, dest, **kwargs)
	# def __call__(self, parser, namespace, values, option_string = None) :
		# print namespace
		# print values

# custom action with parameter
# def compileFM(compile_command) :
	# class ClassName(argparse.Action) :
		# def __init__(self, option_strings, dest, nargs = None, **kwargs) :
			 # super(ClassName, self).__init__(option_strings, dest, **kwargs)
			
		# def __call__(self, parser, namespace, values, option_string = None) :
	# return ClassName

def main() :
	timer = Timer()

	if sys.version_info >= (2, 7):
		ArgsParser()
	else :
		OptParser

	timer.printElapsedTime()

if __name__ ==  '__main__':
	main()