from .mem_event import MemEvent
import math
from lib.mglobal.global_function import Global
from numpy import dot
from numpy.linalg import norm

class MemLib:
    @staticmethod
    def mem_generate_event_dict(events):
        result=dict()
        for e in events:
            result[e.id]=e
        return result
    
    @staticmethod
    def mem_extract_recency(events):
        """
        Get the recency score from events, outputs a dictionary taht key is event id and value is recency score

        Args:
            events (List[MemEvent]): list of MemEvent

        Returns:
            recency_out: a dictionary whose keys are the event.id and whose values 
                        are the float that represents the recency score.
        """
        now=Global.get_global_now_time_stamp()
        
        def get_recency_score(now_time,from_time):
            return math.pow(0.95,abs((now_time-from_time)))
        
        result={}
        for index,e in enumerate(events):
            result[e.id]=get_recency_score(now,e.lastaccess)
            
        return result
    
    @staticmethod
    def mem_extract_importance(events):
        """
        Get the importance from events, outputs a dictionary taht key is event id and value is recency score

        Args:
            events (List[MemEvent]): list of MemEvent

        Returns:
            recency_out: a dictionary whose keys are the event.id and whose values 
                        are the float that represents the recency score.
        """
        result=dict()
        for index, node in enumerate(events):
            result[node.id]=node.importance*0.01
            
        return result
    
    @staticmethod
    def mem_extract_favor(events):
        """
        Get the favor from events, outputs a dictionary taht key is event id and value is recency score

        Args:
            events (List[MemEvent]): list of MemEvent

        Returns:
            recency_out: a dictionary whose keys are the event.id and whose values 
                        are the float that represents the recency score.
        """
        result=dict()
        for index, node in enumerate(events):
            result[node.id]=node.favor*0.01
            
        return result
    
    @staticmethod
    def mem_extract_relevance(events,pool,ref_embedding):
        """
        Get the relevance from events, outputs a dictionary taht key is event id and value is recency score

        Args:
            events (List[MemEvent]): list of MemEvent

        Returns:
            recency_out: a dictionary whose keys are the event.id and whose values 
                        are the float that represents the recency score.
        """
        result=dict()
        for index, node in enumerate(events):
            temp_embedding=pool.get_embedding(node)
            relevance=MemLib.cos_sim(temp_embedding,ref_embedding)
            result[node.id]=relevance
            
        return result
    
    @staticmethod
    def cos_sim(a,b):
        """
        This function calculates the cosine similarity between two input vectors
        'a' and 'b'. Cosin similarity is a measure of similarity between two
        non-zero vectors of an inner product space that measures the cosine
        of the angle between them.

        Args:
            a (_type_): 1-D array object
            b (_type_): 1-D array object

        Returns:
            A scalar value representing the cosine similarity between the input
            vectors 'a' and 'b'
            
        Example input:
            a = [0.2,0.3,0.4]
            b = [0.3,0.2,0.4]
        """
        return dot(a,b)/(norm(a)*norm(b))
    
    @staticmethod
    def normalize_dict_floats(d, target_min, target_max):
        """
        This function normalizes the float values of a given dictionary 'd' between 
        a target minimum and maximum value. The normalization is done by scaling the
        values to the target range while maintaining the same relative proportions 
        between the original values.

        INPUT: 
            d: Dictionary. The input dictionary whose float values need to be 
            normalized.
            target_min: Integer or float. The minimum value to which the original 
                        values should be scaled.
            target_max: Integer or float. The maximum value to which the original 
                        values should be scaled.
        OUTPUT: 
            d: A new dictionary with the same keys as the input but with the float
            values normalized between the target_min and target_max.

        Example input: 
            d = {'a':1.2,'b':3.4,'c':5.6,'d':7.8}
            target_min = -5
            target_max = 5
        """
        min_val = min(val for val in d.values())
        max_val = max(val for val in d.values())
        range_val = max_val - min_val

        if range_val == 0: 
            for key, val in d.items(): 
                d[key] = (target_max - target_min)/2
        else: 
            for key, val in d.items():
                d[key] = ((val - min_val) * (target_max - target_min) 
                        / range_val + target_min)
        return d
    
    @staticmethod    
    def top_highest_x_values(d, x):
        """
        This function takes a dictionary 'd' and an integer 'x' as input, and 
        returns a new dictionary containing the top 'x' key-value pairs from the 
        input dictionary 'd' with the highest values.

        INPUT: 
            d: Dictionary. The input dictionary from which the top 'x' key-value pairs 
            with the highest values are to be extracted.
            x: Integer. The number of top key-value pairs with the highest values to
            be extracted from the input dictionary.
        OUTPUT: 
            A new dictionary containing the top 'x' key-value pairs from the input 
            dictionary 'd' with the highest values.
        
        Example input: 
            d = {'a':1.2,'b':3.4,'c':5.6,'d':7.8}
            x = 3
        """
        top_v = dict(sorted(d.items(), 
                            key=lambda item: item[1], 
                            reverse=True)[:x])
        return top_v