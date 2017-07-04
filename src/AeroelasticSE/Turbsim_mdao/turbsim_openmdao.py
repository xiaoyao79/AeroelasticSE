from openmdao.api import Group, Problem, Component, IndepVarComp, ParallelGroup
import numpy as np
from AeroelasticSE.Turbsim_mdao.turbsim_writer import TurbsimBuilder
from AeroelasticSE.Turbsim_mdao.turbsim_wrapper import Turbsim_wrapper
from AeroelasticSE.Turbsim_mdao.turbsim_reader import turbsimReader

class turbsimGroup(Group):
    def __init__(self):
        super(turbsimGroup, self).__init__()
        self.reader = turbsimReader()
        self.writer = TurbsimBuilder()
        self.wrapper = Turbsim_wrapper()
        self.run_dir = self.writer.run_dir

    def solve_nonlinear(self):
        self.writer.run_dir = self.run_dir
        self.reader.run_dir = self.run_dir
        self.wrapper.run_dir = self.run_dir
        self.writer.turbsim_vt = self.reader.turbsim_vt
        self.writer.execute()
        self.wrapper.execute()

test = turbsimGroup()
test.reader.read_input_file('TurbsimInputFiles/test01.inp')
test.writer.turbulence_template_file = '../Turbsim_mdao/TurbsimInputFiles/turbulence_user.inp'
test.writer.profile_template = '../Turbsim_mdao/TurbsimInputFiles/shear.profile'
test.wrapper.turbsim_exe = '/Users/jquick/SE/TurbSim/bin/TurbSim_glin64'
test.solve_nonlinear()
