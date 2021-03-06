#!/usr/bin/env python
# encoding: utf-8
# Vassilis Vassiliades - 2016

import sys
sys.path.insert(0, sys.path[0]+'/waf_tools')

import boost
import eigen
import tbb

def options(opt):
    opt.load('compiler_cxx')
    opt.load('compiler_c')
    opt.load('boost')
    opt.load('eigen')
    opt.load('tbb')

def configure(conf):
    conf.load('compiler_cxx')
    conf.load('compiler_c')
    conf.load('boost')
    conf.load('eigen')
    conf.load('tbb')

    conf.check_eigen()
    conf.check_boost(lib='serialization filesystem \
            system unit_test_framework program_options \
            thread', min_version='1.39')
    conf.check_tbb()

    if conf.env.CXX_NAME in ["icc", "icpc"]:
        common_flags = "-Wall -std=c++11"
        opt_flags = " -O3 -xHost  -march=native -mtune=native -unroll -fma -g"
    elif conf.env.CXX_NAME in ["clang"]:
        common_flags = "-Wall -std=c++11"
        opt_flags = " -O3 -march=native -g"
    else:
        if int(conf.env['CC_VERSION'][0]+conf.env['CC_VERSION'][1]) < 47:
            common_flags = "-Wall -std=c++0x"
        else:
            common_flags = "-Wall -std=c++11"
        opt_flags = " -O3 -march=native -g"

    all_flags = common_flags + opt_flags
    conf.env['CXXFLAGS'] = conf.env['CXXFLAGS'] + all_flags.split(' ')
    print conf.env['CXXFLAGS']


def build(bld):
    libs = 'BOOST EIGEN TBB'

    bld.program('cxx', 'program',
        source = 'cvt.cpp',
        includes = '',
        use = '',
        uselib = libs,
        target = 'cvt')
