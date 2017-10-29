
#Sampling latitudal points
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import random as rd
import numpy as np

class LatitudalPolygon:
    def __init__(self,bound1 = (42.745458, -73.265071),bound2=(42.061597, -73.527701),
                 bound3 = (41.247793, -70.002255), bound4 = (42.948057, -70.589209)):
        self.bound1 = bound1
        self.bound2 = bound2
        self.bound3 = bound3
        self.bound4 = bound4
        #define plot bounds
        self.latMin = min([bound[0] for bound in [self.bound1,self.bound2, self.bound3,self.bound4]])
        self.latMax = max([bound[0] for bound in [self.bound1,self.bound2, self.bound3,self.bound4]])
        self.longMin = min([bound[1] for bound in [self.bound1,self.bound2, self.bound3,self.bound4]])
        self.longMax = max([bound[1] for bound in [self.bound1,self.bound2, self.bound3,self.bound4]])
    def plot(self,lat_offset=.125, long_offset = .125):
        verts = [
        self.bound1,self.bound2,self.bound3,self.bound4,self.bound1
        ]
        codes = [
            Path.MOVETO,
             Path.LINETO,
             Path.LINETO,
             Path.LINETO,
             Path.CLOSEPOLY,
        ]
        path = Path(verts, codes)
        fig =  plt.figure()
        ax = fig.add_subplot(111)
        patch = patches.PathPatch(path, facecolor='orange', lw=2)
        ax.add_patch(patch)
        ax.set_xlim(self.latMin-lat_offset,self.latMax+lat_offset)
        ax.set_ylim(self.longMin-long_offset,self.longMax+long_offset)
        plt.show()
    #helper function for incrementor
    #Inputs:
        #Indexes:
        #max_index: 
    #Output:
        #Truth table indicating the non-maxed out indices
    def indexValuePick(self, indexes, max_index):
        table = []
        for index, item in enumerate(indexes[::-1]):
            #print "index: "+str(index)+" item: "+str(item)
            if item<max_index-index:
                table.append(True)
            else:
                table.append(False)
        return table
    #Helper function for incrementor
    #Input:
        #Table: True table indicating indices that hasn't maxed out yet
    #Output:
        #Index of the table to be incremented first
    def index_to_increment(self,table):
        for index,boolean in enumerate(table):
            if boolean:
                return len(table)-index -1
        return -1
    #Helper function for pointSets
    #Input:
        #indexes: list of indexes or integers
        #max_value an index can take
    #Output:
        #The input indexes with one of them incremented or -1 if not needed
    def incrememtor(self, indexes, max_index):
        
        truth_table = self.indexValuePick(indexes, max_index)
        #index to increment
        index = self.index_to_increment(truth_table)
        if index!=-1:
            indexes[index]+=1
            for i in range(len(indexes[index:])):
                indexes[index+i]=indexes[index]+i
            return indexes
        return -1
    #Helper function for pointSets
    #Input:
        #indexes: list of indexes to extract points from
        #points: List of points to extract points from
    #Output:
        #points: List of points with at given indices 
    def extractPoints(self, indexes,points):
        points = [points[i] for i in indexes]
        return points
    #Input:
        #points: List of points within in the polygon
        #Numbpoints: number of points in a group(list) of points
    #Output:
        #list of lists of points each with length numPoints
    def pointSets(self, numPoint, points):
        
        point_set = []
        
        indexes = range(numPoint)
        max_index = len(points)-1

        while isinstance(indexes, list):
            #print 'running with indices: '+str(indexes)+" max_index: "+str(max_index)
            extracted_points = self.extractPoints(indexes,points)
            indexes = self.incrememtor(indexes, max_index)
            #print 'running with indices: '+str(indexes)+" max_index: "+str(max_index)
            point_set.append(extracted_points)
        return point_set
    #Helper function for point_set_min_dist
    #Input:
        #point1: latitudal point(latitude, logitude)
        #point2: latitudal point(latidue, logitude)
    #Output:
        #The euclidean distance between point1 and point2, assumes the latitude/logitude lines are fairly straight
    def distance_calc(self,point1, point2):
        distance = np.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
        return distance
    #Helper function for variances 
    #Input:
        #point_set: a list of points within the polygon 
    #Output:
        #minimum of the distances between any two points in the list
    def point_set_min_dist(self,point_set):
        dists = []
        for i in range(len(point_set)-1):
            for j in range(i+1,len(point_set)):
                dists.append(self.distance_calc(point_set[i], point_set[j]))
        return min(dists)   
    #Helper function for sample_points
    #Input:
        #numPoints: number of points to taken from a population of points within the polygon
        #points:  The population of points
    #output:
        #map of the min distance between any two points in a list of points to the list of points
    def variances(self,numPoints, points):
        point_set = self.pointSets(numPoints, points)
        point_map = {self.point_set_min_dist(points): points for points in point_set}
        return point_map
    #Helper function for sample_points
    #Input:
        #point_map: map of the min distance any two points in a list of points to the list of points
    #Output:
        #List of points with highest min distance
    def highest_variance(self, point_map): 
        return max(point_map.iteritems(), key=operator.itemgetter(0))[1]
    #Input:
        #numPoints: Number of points to pick from the sample
        #point_population: Number of points to sample
    #Output:
        #list of length numPoints with the highest min distance between
        #any two points in the list; we're looking for a list with high variance
    def sample_points(self,numPoints = 3, point_population = 100):
        point_array = []
        point_count = point_population
        while(point_count>0):
            #print "still running with point count: "+str(point_count)
            lat = rd.uniform(self.latMin,self.latMax)
            longi = rd.uniform(self.longMin, self.longMax)
            point_count-=1
            point = (lat,longi)
            point_array.append(point)
        #print "point array: "+str(point_array)
        point_map = self.variances(numPoints, point_array)
        return self.highest_variance(point_map)

    


