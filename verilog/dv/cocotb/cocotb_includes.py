from os import path
import sys
sys.path.append(path.abspath('/home/rady/caravel/caravel_release/caravel-dynamic-sims/cocotb'))
from interfaces.common_functions.test_functions import report_test
from interfaces.common_functions.test_functions import test_configure
from interfaces.common_functions.test_functions import max_num_error
from interfaces.common_functions.test_functions import read_config_file
from interfaces.UART import UART
from interfaces.caravel import Caravel_env
from interfaces.cpu import RiskV
from interfaces.defsParser import Regs
from interfaces.caravel import GPIO_MODE
from interfaces.caravel import Caravel_env
from interfaces.SPI import SPI
from interfaces.common_functions.Timeout import Timeout

import cocotb 