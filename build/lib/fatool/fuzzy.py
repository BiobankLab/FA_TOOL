# -*- coding: utf-8 -*-

#import math
import logging

def find_aprox_match_iter(needle, hstack, missmatch_level, hs_start_pos = 0):
    i = hs_start_pos # start iterate from start position 
    start = hs_start_pos # start of founded region at begining start of search
    mmatch_count = 0  # missmatch counter
    needle_len = len(needle)
    j = 0  # needle iterator
    while i < len(hstack):
        if hstack[i] != needle[j]:
            mmatch_count += 1
            if mmatch_count > missmatch_level:
            # if missmatch level oversized back to strat + 1 and start again
                i -= j
            # needle iterator restart (-1) because it will be increased in a moment
                j = -1
            # new start = start + 1
                start = i+1
                #print 'start = '+str(start)
            # reset mmatch_count
                mmatch_count = 0
        i += 1
        j += 1
        # if needle iterator = len of needle match found return it.
        if j >= needle_len:
            return (start,i,mmatch_count)
            
def find_all_aprox_matches(needle, hstack, missmatch_level, hs_start_pos):
    ret_list = [] # list of matches to return
    i = hs_start_pos # start iteration from start position
    needle_len = len(needle)
    while i+needle_len <= len(hstack):
        r = find_aprox_match_iter(needle, hstack, missmatch_level, i)
        # match found append to list strat new look in start + 1 position
        if r:
            ret_list.append(r)
            i = r[0]+1
        # match not found - no more maches in hstack
        else:
            break
    return ret_list

# return string from between two aproximated motifs 
def find_motif_in_aprox_range(start_motif, stop_motif, hstack, missmatch_level, hs_start_pos = 0):
    start = 0
    stop = 0
    start = find_aprox_match_iter(start_motif, hstack, missmatch_level, hs_start_pos = 0)
    stop = find_aprox_match_iter(stop_motif, hstack, missmatch_level, start[1])
    if start and stop:
        return hstack[start[1]:stop[0]]
        
def find_all_motifs_in_aprox_range(start_motif, stop_motif, hstack, missmatch_level, hs_start_pos = 0, len_min = 0, len_max = float('inf')):
    i = hs_start_pos
    start = 0
    stop = 0
    ret_list = []
    logger = logging.getLogger(__name__)
    #logger.setLevel(logging.DEBUG)
    logger.debug([start_motif, stop_motif, hstack, missmatch_level, hs_start_pos, len_min, len_max])
    logger.debug(hstack)
    
    while i <= len(hstack):
        start = find_aprox_match_iter(start_motif, hstack, missmatch_level, i)
        stop = find_aprox_match_iter(stop_motif, hstack, missmatch_level, start[1])
        if start and stop:
            if stop[1] - start[0] >= len_min and stop[1] - start[0] <= len_max:
                ret_list.append(hstack[start[0]:stop[1]])
            i = start[0]+1
        else:
            break
    logger.debug(ret_list)
    return ret_list

def find_motif(needle, hstack, missmatch_level, hs_start_pos = 0):
    r = 0
    r = find_aprox_match_iter(needle, hstack, missmatch_level, hs_start_pos = 0)
    if r:
        return hstack[r[0]:r[1]]

def find_all_motifs(needle, hstack, missmatch_level, hs_start_pos = 0):
    i = hs_start_pos
    ret_list = []
    while i <= len(hstack):
        r = find_aprox_match_iter(needle, hstack, missmatch_level, i )
        if r:
            ret_list.append(hstack[r[0]:r[1]])
            i = r[0]+1
        else:
            break
    return ret_list