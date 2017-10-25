# -*- encoding: utf-8 -*-
import os


templateDir = os.path.dirname(os.path.realpath(__file__))

cIndependentFunctionsPath = os.path.join(templateDir, "independent.c")
cTemplatePath = os.path.join(templateDir, "c_template.c")
headerTemplatePath = os.path.join(templateDir, "c_template.h")
