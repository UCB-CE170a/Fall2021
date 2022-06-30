import unittest
import sim_package as sm
from sim_package.interface import simplegraph, from_dataframe
from ctypes import c_double
import logging
import sys
import pandas as pd

logger = logging.getLogger()
logger.level = logging.DEBUG

class TestInterface(unittest.TestCase):
    
    def setUp(self):
      self.stream_handler = logging.StreamHandler(sys.stdout)
      logger.addHandler(self.stream_handler)
      
    def tearDown(self):
      logger.removeHandler(self.stream_handler)
  
    
    def test_spt_single(self):
      g = simplegraph()
      #g = readgraph(b"../sf.mtx")
      res = g.update_edge(1, 3, c_double(0.5))
      sp = g.dijkstra(1, -1)
      g.writegraph(b"test.mtx")
      lg = logging.getLogger()
      lg.info('test 1')
      for destination in [2, 3]:
          
          self.assertEqual([vertex[1] for vertex in sp.route(destination)], [destination])
      sp.clear()
    
    def test_spt_data_frame_scenario_1(self):
      df = pd.DataFrame({'start':[0,1,2,3,4,5,6,7], 'end':[1,2,3,4,5,6,7,0], 'wgh':[0.1,0.5,1.9,1.1,1.2,1.5,1.6,1.9]})
      g = from_dataframe(df, 'start', 'end', 'wgh')

      origin, destin = 1, 5
      sp = g.dijkstra(origin, destin)
      lg = logging.getLogger()
      lg.info('test 2')
      
      self.assertEqual(list(range(1, 6)), [origin] + [vertex[1] for vertex in sp.route(destin)])
      self.assertEqual(4.7, sp.distance(destin))
      sp.clear()

    def test_spt_data_frame_scenario_2(self):
      df = pd.DataFrame({'start':[0,2,4,10,12], 'end':[1,3,5,12,0], 'wgh':[0.1,0.5,1.9,1.1,1.2]})
      g = from_dataframe(df, 'start', 'end', 'wgh')

      origin, destin = 10, 1
      sp = g.dijkstra(origin, destin)
      lg = logging.getLogger()
      lg.info('test 3')
      self.assertEqual([10, 12, 0, 1], [origin] + [vertex[1] for vertex in sp.route(destin)])
      self.assertEqual(2.4, sp.distance(destin))
      sp.clear()