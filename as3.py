'''
Data Mining Assignment 3, K-Medoids
2016253072
명수환(Myeong Suhwan)
'''
from datetime import datetime
import math

#? Step1. 랜덤으로 K개의 클러스터링

#? Step2. 각 클러스터마다 K-Means에 가장 가까운 centroid를 선정

#? Step3. 클러스터 내의 다른 노드를 대상으로, 다른 클러스터의 centroid와의 거리가 더 가까우면 Reassign한다.

#? Step4. 변화가 없을 때까지 step2-step3를 반복한다.

def getDataFromFile(filename):
    input_file = open(filename, 'r')
    gene_id = dict()
    
    line_num = 0
    for line in input_file:
        time_point_data = line.split()
        gene_id[line_num] = time_point_data
        
        line_num += 1
        
        
    return gene_id

def randClustering(gene_id):
    cluster = list() # k개의 cluster 생성, k : 10
    init_mem_num_in_cluster = int(len(gene_id) / k)
    line_num = 0

    for i in range(0,len(gene_id)-1,init_mem_num_in_cluster):
        same_cluster = list()
        for i in range(init_mem_num_in_cluster):
            same_cluster.append(line_num)
            line_num += 1    
        cluster.append(same_cluster)

    return cluster

def getKMeans(cluster,cluster_num,gene_id): 
    kmeans = [0,0,0,0,0,0,
                0,0,0,0,0,0,] #* 12-dimension
    object_num = len(cluster[cluster_num])

    for i in range(DIMENSION):
        
        tmp = 0
        for num in range(object_num):
            
            tmp += (float(gene_id[cluster[cluster_num][num]][i]))
            
        tmp /= float(object_num)
        
        kmeans[i] = float("{:.3f}".format(tmp))
        
    #*print("k-means : ", kmeans)
    return kmeans


def getDistance(kmeans, object):
    dist = 0
    
    for dimension in range(DIMENSION):
        dist_dimesion = float(kmeans[dimension]) - float(object[dimension])
        tmp = math.pow(dist_dimesion,2)
        dist += tmp
    dist = math.sqrt(dist)
    dist = "{:.3f}".format(dist)
    
    return float(dist)

def Reassign(obj, to_cluster_num,from_cluster_num,cluster):
    # * add to new cluster
    cluster[to_cluster_num].append(obj) # * number of object

    # * remove from old cluster
    #print(cluster[from_cluster_num])
    #print(obj)
    cluster[from_cluster_num].remove(obj)
    #*print(obj,"이", "cluster",to_cluster_num,"에 추가되었습니다.")
    #*print(cluster[to_cluster_num])
    

def output_to_file(filename,cluster):
    file = open(filename, 'w')
    
    for i in range(k):
        file.write('{0}: '.format(len(cluster[i])))
        for v in cluster[i]:
            file.write(str(v)+" ")
        file.write("\n")
        

    file.close()
    print("Finished to print to output file : ", filename)

def SetCentroid(cluster,gene_id):
    cluster_num = 0
    centroid_list = [-1,-1,-1,-1,-1,
                    -1,-1,-1,-1,-1] #* the number of cluster is k:10, value:-1 for initializing.

    while(cluster_num < k):
        #print("DEBUG: Cluster ",cluster_num)
        kmeans = getKMeans(cluster,cluster_num=cluster_num,gene_id=gene_id)
        
        shortest_distance = getDistance(kmeans,gene_id[cluster[cluster_num][0]]) #!init value
        centroid = cluster[cluster_num][0] #!init value

        for i in range(len(cluster[cluster_num])):
            distance = getDistance(kmeans,gene_id[cluster[cluster_num][i]])
            
            if distance < shortest_distance:
                centroid = cluster[cluster_num][i]
                shortest_distance = distance

        centroid_list[cluster_num] = centroid
        #print("centroid : ",centroid) #? centroid means line number
        #print("shortest_distance :",shortest_distance)
        #print("===============================")
        cluster_num += 1
    print("centroid_list :",centroid_list)
    return centroid_list

def SetNewCluster(cluster,centroid_list,gene_id):
    isChanged = False
    for cluster_num in range(k):
        #print("Cluster",cluster_num,"=> ",cluster[cluster_num])
        idx = 0
        while idx < len(cluster[cluster_num]):
            
            
            if cluster[cluster_num][idx] == centroid_list[cluster_num]:
                #*print("This is the centroid.")
                idx += 1
                continue
            #*print("오브젝트 ",cluster[cluster_num][idx])
            
            distance_same = getDistance(gene_id[centroid_list[cluster_num]],gene_id[cluster[cluster_num][idx]])
            shortest_distance = distance_same #!init value
            for u in centroid_list:    
                distance_other = getDistance(gene_id[u],gene_id[cluster[cluster_num][idx]])

                if distance_other < shortest_distance:
                    to_cluster_number = centroid_list.index(u)
                    shortest_distance = distance_other
            #*print("shortest distance : ",shortest_distance)
            #*print("========================")
            
            if distance_same != shortest_distance:
                isChanged = True
                obj = cluster[cluster_num][idx]
                Reassign(obj,to_cluster_number,from_cluster_num = cluster_num,cluster=cluster)
                idx -= 1

            idx += 1

    return isChanged    


def main():
    global DIMENSION,k
    DIMENSION = 12
    k = 10
    input_filename = 'assignment3_input.txt' #500
    #input_filename = 'test1.txt'
    output_filename = 'assignment3_output.txt'

    gene_id = getDataFromFile(input_filename)
    
    
    print(gene_id)
    start_time = datetime.now()

    #? Step1. 랜덤으로 K개의 클러스터링
    cluster = randClustering(gene_id)
    for num in range(k):
        print("cluster",num,cluster[num])
        for i in range(len(cluster[num])):
            print(gene_id[cluster[num][i]])
        print("\n")


    isChanged = True #! init value
    debug_count = 0
    while isChanged:     #? Step4. 변화가 없을 때까지 step2-step3를 반복한다.
        debug_count += 1
        print("[+]",debug_count,"번 반복하였습니다.")
        #? Step2. 각 클러스터마다 K-Means에 가장 가까운 centroid를 선정
        centroid_list = SetCentroid(cluster,gene_id)

        #? Step3. 클러스터 내의 다른 노드를 대상으로, 다른 클러스터의 centroid와의 거리가 더 가까우면 Reassign한다.
        isChanged = SetNewCluster(cluster,centroid_list,gene_id)
    end_time = datetime.now()
    print("\n")
    for num in range(k):
        cluster[num].sort()
        print("cluster",num,"SIZE:",len(cluster[num]),cluster[num])
        print("\n")
        
    output_to_file(output_filename,cluster)
    print("\n")
    print("Time Elapsed : ", end_time - start_time,"microseconds")



if __name__ == '__main__':
    main()