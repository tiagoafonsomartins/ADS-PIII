'''import jpype

CLASSPATH = "C:\\Users\\Nuno Dias\\swrlapi-example\\src\\main\\java\\org\\swrlapi\\example\\SWRLAPIExample.jar"
jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % CLASSPATH)
jpype.java.lang.System.out.println("Calling Java Print from Python using Jpype!")
jpype.shutdownJVM()
'''

import subprocess
subprocess.call(['java', '-jar', 'SWRLAPIExample.jar', "hello"])

