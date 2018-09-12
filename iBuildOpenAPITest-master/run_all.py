#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestLoader, TestSuite
# from HtmlTestRunner import HTMLTestRunner
import test_OpenAPISign
import test_env_monitor_testdevice
import test_env_monitor
import test_construction_elevator
import test_electricity_meter
import test_hanging_basket
import test_hanging_basket_params
import test_tower_crane
import test_tower_crane_params
# import test_tower_heart_beat
import test_unloading_platform
import test_unloading_platform_params
import test_water_meter
import test_concrete_temp
import test_soil_temp
import test_smoke_detector
import test_sewage_outfall
import test_rain_recovery
import test_construction_elevator_params
import test_process_task
import test_qualityCheck
import test_securityCheck
import test_vehicle_management
import test_intrusion_detector
import os
import HTMLReport
import datetime
from config.AppConfig import ENV

dir_path = os.path.dirname(os.path.realpath(__file__))

OpenAPISign = TestLoader().loadTestsFromModule(test_OpenAPISign)
env_monitor_testdevice = TestLoader().loadTestsFromModule(
    test_env_monitor_testdevice)
env_monitor = TestLoader().loadTestsFromModule(test_env_monitor)
process_task = TestLoader().loadTestsFromModule(test_process_task)
construction_elevator = TestLoader().loadTestsFromModule(
    test_construction_elevator)
electricity_meter = TestLoader().loadTestsFromModule(test_electricity_meter)
hanging_basket = TestLoader().loadTestsFromModule(test_hanging_basket)
hanging_basket_params = TestLoader().loadTestsFromModule(
    test_hanging_basket_params)
tower_crane = TestLoader().loadTestsFromModule(test_tower_crane)
tower_crane_params = TestLoader().loadTestsFromModule(test_tower_crane_params)
# tower_heart_beat = TestLoader().loadTestsFromModule(test_tower_heart_beat)
unloading_platform = TestLoader().loadTestsFromModule(test_unloading_platform)
unloading_platform_params = TestLoader().loadTestsFromModule(
    test_unloading_platform_params)
water_meter = TestLoader().loadTestsFromModule(test_water_meter)
concrete_temp = TestLoader().loadTestsFromModule(test_concrete_temp)
soil_temp = TestLoader().loadTestsFromModule(test_soil_temp)
smoke_detector = TestLoader().loadTestsFromModule(test_smoke_detector)
sewage_outfall = TestLoader().loadTestsFromModule(test_sewage_outfall)
rain_recovery = TestLoader().loadTestsFromModule(test_rain_recovery)
construction_elevator_params = TestLoader().loadTestsFromModule(
    test_construction_elevator_params)

qualityCheck = TestLoader().loadTestsFromModule(test_qualityCheck)
securityCheck = TestLoader().loadTestsFromModule(test_securityCheck)
vehicle_management = TestLoader().loadTestsFromModule(test_vehicle_management)
intrusion_detector = TestLoader().loadTestsFromModule(test_intrusion_detector)

suite = TestSuite([
    OpenAPISign, env_monitor, construction_elevator, electricity_meter,
    hanging_basket, hanging_basket_params, tower_crane, tower_crane_params,
    unloading_platform, unloading_platform_params, water_meter,
    env_monitor_testdevice, concrete_temp, soil_temp, smoke_detector,
    sewage_outfall, rain_recovery, construction_elevator_params, process_task,
    securityCheck, qualityCheck, vehicle_management, intrusion_detector
])

tower_suite = TestSuite([tower_crane])
# runner = HTMLTestRunner(output=dir_path + '/Reports/', report_title="OpenAPI-Test")
# runner.run(suite)

# "%Y-%m-%d_%H-%M-%S"))
if ENV['Env'] is 'QA':
    FileName = 'TestReport-{}'.format(datetime.datetime.now().strftime(
        "%Y-%m-%d"))
    title = 'QA-测试报告'
if ENV['Env'] is 'PRDTest':
    FileName = 'PRDTest-TestReport-{}'.format(datetime.datetime.now().strftime(
        "%Y-%m-%d"))
    title = 'PRDTest-测试报告'
if ENV['Env'] is 'PRD':
    FileName = 'PRD-TestReport-{}'.format(datetime.datetime.now().strftime(
        "%Y-%m-%d"))
    title = 'PRD-测试报告'
# else:
# break
runner = HTMLReport.TestRunner(
    report_file_name=FileName,
    output_path=dir_path + '/Reports/',
   # verbosity=2,
    title=title,
    description='',
    thread_count=1,
    sequential_execution=True)

runner.run(suite)
# runner.run(TestSuite([construction_elevator_params,hanging_basket_params,tower_crane_params,unloading_platform_params]))
# runner.run(TestSuite([tower_crane, construction_elevator]))
