# distutils: language = c++


from libcpp.string cimport string
from libcpp.map cimport map as mapcpp
from libcpp.vector cimport vector
from libcpp.pair cimport pair as paircpp
from libcpp.utility cimport make_pair
from cython.operator import dereference, postincrement
from cython.parallel import prange, threadlocal

import numpy as np

cdef class Node:

    cdef double lon, lat
    
    cdef mapcpp[str, str] in_links
    cdef vector[str] out_links
    cdef vector[str] go_vehs

    def __init__(self, node_id: str, lon: float, lat: float, ntype: str, osmid: str=''):
        self.lon = lon
        self.lat = lat

        # faster to leave these as generic Pyobject
        # ref: https://stackoverflow.com/questions/49585038/cython-when-should-i-define-a-string-as-char-str-or-bytes
        self.nid = node_id
        self.ntype = ntype
        self.osmid = osmid
        self.status = ''

    cdef Node create_virtual_node(self):
        return Node('vn_source_{}'.format(self.nid), self.lon+0.001, self.lat+0.001, 'vn_source')

    def calculate_straight_ahead_links(self, dict node_id_dict, dict link_id_dict):
        cdef mapcpp[str, Node] node_id_map = node_id_dict
        cdef mapcpp[str, Link] link_id_map = link_id_dict
        cdef vector[str] link_id_keys = link_id_dict.keys()
        cdef Py_ssize_t link_id_size = link_id_keys.size()

        cdef Py_ssize_t i
        cdef double lon, lat
        lon, lat = self.lon, self.lat

        # for use within prange local scope
        cdef threadlocal(double) x_start, y_start
        cdef np.ndarray[double] in_vec = np.array([[0, 0] for _ in np.arange(link_id_size)], double)
        cdef str out_link

        in_vec = np.array([0, 0])

        for i in prange(link_id_size, nogil=True):
            out_link = self.out_links.at(i)
            x_start = node_id_map.get(link_id_map.get(out_link).start_nid).lon
            y_start = node_id_map.get(link_id_map.get(out_link).start_nid).lat
            with gil:
                in_vec[i][:] = [lon - x_start, la]
            
            
            



cdef class Link:

    cdef str link_id, ltype
    cdef int lanes
    cdef double lanes

    def __init__(self, link_id, lanes, length, fft, capacity, ltype, start_nid, end_nid, geometry):
        pass



        
