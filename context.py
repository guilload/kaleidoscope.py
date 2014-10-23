from llvm.core import Module
from llvm.ee import ExecutionEngine
from llvm.passes import (FunctionPassManager,
                         PASS_GVN,
                         PASS_INSTCOMBINE,
                         PASS_REASSOCIATE,
                         PASS_SIMPLIFYCFG)


class Context(object):

    optimizations = (PASS_GVN,
                     PASS_INSTCOMBINE,
                     PASS_REASSOCIATE,
                     PASS_SIMPLIFYCFG)

    def __init__(self, name):
        self.name = name
        self.module = Module.new(name)
        self.builder = None
        self.scope = {}
        self.executor = ExecutionEngine.new(self.module)
        self.fpm = self.setup_fpm()

    def setup_fpm(self):
        fpm = FunctionPassManager.new(self.module)

        # github.com/llvmpy/llvmpy/issues/44
        fpm.add(self.executor.target_data.clone())

        for optimization in self.optimizations:
            fpm.add(optimization)

        fpm.initialize()

        return fpm
