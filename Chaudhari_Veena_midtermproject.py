#!/usr/bin/env python
# coding: utf-8

# ## Topic: Apriori algorithm, generate and print out all the association rules.
# 
# #### Name: Veena Chaudhari
# 
# #### Subject: CS 634 Data mining
# 

# ## Loading Libraries

# In[1]:


#importing all libraries
import pandas as pd
import numpy as np
import csv
from itertools import combinations


# ## Defining functions

# In[2]:


# For loading data and creating a list of items
def data_prep(file):
    df = pd.read_csv(file).iloc[:,1:]
    data1 = dict()
    for i, row in df.iterrows():
        data1[i] = list(row)
        
    listed = list(data1.values())
    unique_list = np.unique(np.concatenate(listed))[np.unique(np.concatenate(listed)) != 'nan']
    oneitem_list = {key: None for key in unique_list}
    return oneitem_list, data1
    


# In[3]:


# Create itemset for specified number of combinations
def create_itemset(k,itemset):
    unique_itemset = np.unique(list(itemset.keys()))
    items_list = list(combinations(unique_itemset, k))
    return items_list


# In[4]:


#Calculate the frequency of each itemset (1, 2, 3, itemsets) by checking the number of transactions in the database
def frequency (item_list, data):
    itemset_count = dict()
    for i in range(len(item_list)):
        counter = 0
        for j in range(len(data)):
            if all(elem in data[j] for elem in item_list[i]):
                counter += 1
        itemset_count[item_list[i]] = counter
    return itemset_count


# In[5]:


# Check if itemset are superset of previously removed transactionc
def check_if_superset(itemset, previ, n):
    if n>2:    
        subsets = list(combinations(itemset, (n-1)))
        if any(elem in previ for elem in subsets):
            return False
    return True


# In[6]:


# Check if the itemset satisfy specified minimum support
def min_support(item_freq, data,min_sup, n,previous_removed):
    min_sup = min_sup/100
    length = len(data)
    return_item = {}
    removed_item = []
    for key, value in item_freq.items():
        if value/length < min_sup:
            removed_item.append(key)
        else:
             if check_if_superset(key, previous_removed, n) == True :
                    return_item[key] = value
             
    return return_item, removed_item


# In[7]:


# Main Function to calculate all item sets and print rules
def main(file,minimum_support, minimum_confidence):
    min_confidence = minimum_confidence/100 
    itemlist, data = data_prep(file)
    
    # 1-item_set
    prev = []
    one_item_min ={}
    one_item_list = create_itemset(1,itemlist)
    one_item_freq = frequency(one_item_list, data)
    one_min, removed_item_1 = min_support(one_item_freq, data, minimum_support, 1,prev)
    for keys, values in one_min.items():
        one_item_min[keys[0]] = values

    # 2 item-set
    two_item_list = create_itemset(2,one_item_min)
    two_item_freq = frequency(two_item_list, data)
    two_item_min, removed_item_2 = min_support(two_item_freq, data, minimum_support, 2, removed_item_1)

    # 3 item-set
    three_item_list = create_itemset(3,two_item_min)
    three_item_freq = frequency(three_item_list, data)
    three_item_min, removed_item_3 = min_support(three_item_freq, data, minimum_support, 3,removed_item_2)

    #four item-set
    four_item_list = create_itemset(4,three_item_min)
    four_item_freq = frequency(four_item_list, data)
    four_item_min, removed_item_4 = min_support(four_item_freq, data, minimum_support, 4,removed_item_3)

    itemset_all = {**one_item_min, **two_item_min, **three_item_min, **four_item_min} 
    
# For printing all association rules for two itemset
    printing = pd.DataFrame()
    for i in two_item_min:
            confidence_1 = np.round (itemset_all[i]/itemset_all[i[0]], decimals = 2)
            confidence_2 = np.round (itemset_all[i]/itemset_all[i[1]], decimals = 2)
            if confidence_1 > min_confidence:
                new_row_2_1 = {'Antecedent' : i[0],'Consequent' : i[1],'Rule_Confidence' : confidence_1 }
                printing = printing.append(new_row_2_1, ignore_index=True)
            else: 
                pass
            if confidence_2 > min_confidence:
                new_row_2_2 = {'Antecedent' : i[1],'Consequent' : i[0],'Rule_Confidence' : confidence_2 }
                printing = printing.append(new_row_2_2, ignore_index=True)
            else: 
                pass
#printing all association rules for three itemset
    for i in three_item_min:
        combos = list(combinations(i, 2))
        for j in combos:
            confidence = np.round(itemset_all[i]/itemset_all[j], decimals = 2)
            if confidence > min_confidence:
                trans2 = list(set(i) - set(j))
                new_row_3 = {'Antecedent' : j,'Consequent':trans2,'Rule_Confidence' : confidence }
                printing = printing.append(new_row_3, ignore_index=True)
            else: 
                pass
#printing all association rules for four itemset            
    for i in four_item_min:
        combos = list(combinations(i, 3))
        for j in combos:
            confidence = np.round(itemset_all[i]/itemset_all[j], decimals = 2)
            if confidence > min_confidence:
                trans2 = list(set(i) - set(j))
                new_row_4 = {'Antecedent' : j,'Consequent':trans2,'Rule_Confidence' : confidence }
                printing = printing.append(new_row_4, ignore_index=True)
            else: 
                pass    
    
    return itemset_all,printing


# ## Determining Association Rules for K-Mart

# #### Running Kmart dataset with support 40% and confidence 50%

# In[8]:


#File for dataset
kmart = '/Users/veena/Desktop/Dmining/Projects/Datasets/K-mart.csv'
#Specify minimum support
minimum_support = 40
#Specify minimum confidence
minimum_confidence = 50

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_kmart_1 = main(kmart,minimum_support,minimum_confidence)

print('***************** KMART *****************')
#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Kmart with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_kmart_1,'\n')
print('---------------------------------------------------------------------\n')
#Printing Final association rules in format A,B --> C
print("Final Association Rules for Kmart with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_kmart_1['Rule_Confidence'])):
    print ("{}) {} --> {} ".format(i+1, rules_kmart_1['Antecedent'][i],rules_kmart_1['Consequent'][i]))


# #### Running Kmart dataset with support 50% and confidence 75%

# In[9]:


#Specify minimum support
minimum_support = 50
#Specify minimum confidence
minimum_confidence = 75

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_kmart = main(kmart,minimum_support,minimum_confidence)

#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Kmart with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_kmart,'\n')
print('---------------------------------------------------------------------\n')
#Printing Final association rules in format A,B --> C
print("Final Association Rules for Kmart with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_kmart['Rule_Confidence'])):
    print ("{}) {} --> {} ".format(i+1, rules_kmart['Antecedent'][i],rules_kmart['Consequent'][i]))


# #### Running Kmart dataset with support 30% and confidence 90%

# In[10]:


#Specify minimum support
minimum_support = 30
#Specify minimum confidence
minimum_confidence = 90

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_kmart = main(kmart,minimum_support,minimum_confidence)

#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Kmart with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_kmart,'\n')
print('---------------------------------------------------------------------\n')
#Printing Final association rules in format A,B --> C
print("Final Association Rules for Kmart with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_kmart['Rule_Confidence'])):
    print ("{}) {} --> {} ".format(i+1, rules_kmart['Antecedent'][i],rules_kmart['Consequent'][i]))


# #### Running Kmart dataset with support 35% and confidence 60%

# In[11]:


#Specify minimum support
minimum_support = 35
#Specify minimum confidence
minimum_confidence = 60

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_kmart = main(kmart,minimum_support,minimum_confidence)

#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Kmart with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_kmart,'\n')
print('---------------------------------------------------------------------\n')
#Printing Final association rules in format A,B --> C
print("Final Association Rules for Kmart with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_kmart['Rule_Confidence'])):
    print ("{}) {} --> {} ".format(i+1, rules_kmart['Antecedent'][i],rules_kmart['Consequent'][i]))


# ## Determining Association Rules for Best_buy

# #### Running Best Buy dataset with support 40% and confidence 90%

# In[12]:


bb = '/Users/veena/Desktop/Dmining/Projects/Datasets/Best_buy.csv'
#Specify minimum support
minimum_support = 40
#Specify minimum confidence
minimum_confidence = 90


print('***************** BEST BUY *****************')
#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_bb = main(bb,minimum_support,minimum_confidence)
print()
#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Best buy with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_bb,'\n')
print('---------------------------------------------------------------------')
#Printing Final association rules in format A,B --> C
print("Final Association Rules for Best buy with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_bb['Rule_Confidence'])):
    print ("{}) {} --> {}  ".format(i+1, rules_bb['Antecedent'][i],rules_bb['Consequent'][i]))


# #### Running Best Buy dataset with support 30% and confidence 80%

# In[13]:


#Specify minimum support
minimum_support = 55
#Specify minimum confidence
minimum_confidence = 80

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_bb = main(bb,minimum_support,minimum_confidence)

#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Best buy with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_bb,'\n')
print('---------------------------------------------------------------------')
#Printing Final association rules in format A,B --> C
print("Final Association Rules for Best buy with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_bb['Rule_Confidence'])):
    print ("{}) {} --> {}  ".format(i+1, rules_bb['Antecedent'][i],rules_bb['Consequent'][i]))


# #### Running Best Buy dataset with support 45% and confidence 95%

# In[14]:


#Specify minimum support
minimum_support = 45
#Specify minimum confidence
minimum_confidence = 95

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_bb = main(bb,minimum_support,minimum_confidence)

#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Best buy with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_bb,'\n')
print('---------------------------------------------------------------------')
#Printing Final association rules in format A,B --> C
print("Final Association Rules for Best buy with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_bb['Rule_Confidence'])):
    print ("{}) {} --> {}  ".format(i+1, rules_bb['Antecedent'][i],rules_bb['Consequent'][i]))


# #### Running Best Buy dataset with support 35% and confidence 90%

# In[15]:


#Specify minimum support
minimum_support = 35
#Specify minimum confidence
minimum_confidence = 90

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_bb = main(bb,minimum_support,minimum_confidence)

#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Best buy with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_bb,'\n')
print('---------------------------------------------------------------------')
#Printing Final association rules in format A,B --> C
print("Final Association Rules for Best buy with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_bb['Rule_Confidence'])):
    print ("{}) {} --> {}  ".format(i+1, rules_bb['Antecedent'][i],rules_bb['Consequent'][i]))


# ## Determining Association Rules for Costco

# #### Running Costco dataset with support 40% and confidence 30%

# In[16]:


costco = '/Users/veena/Desktop/Dmining/Projects/Datasets/costco.csv'
#Specify minimum support
minimum_support = 40
#Specify minimum confidence
minimum_confidence = 30

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_costco = main(costco,minimum_support,minimum_confidence)

print('***************** COSTCO *****************')
#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Costco with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_costco,'\n')
print('---------------------------------------------------------------------')
#Printing Final association rules in format A,B --> C
print("Final Association Rules for costco with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_costco['Rule_Confidence'])):
    print ("{}) {} --> {}  ".format(i+1, rules_costco['Antecedent'][i],rules_costco['Consequent'][i]))


# #### Running Costco dataset with support 45% and confidence 65%

# In[17]:


#Specify minimum support
minimum_support = 45
#Specify minimum confidence
minimum_confidence = 65

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_costco = main(costco,minimum_support,minimum_confidence)

#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Costco with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_costco,'\n')
print('---------------------------------------------------------------------')
#Printing Final association rules in format A,B --> C
print("Final Association Rules for costco with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_costco['Rule_Confidence'])):
    print ("{}) {} --> {}  ".format(i+1, rules_costco['Antecedent'][i],rules_costco['Consequent'][i]))


# #### Running Costco dataset with support 30% and confidence 75%

# In[18]:


#Specify minimum support
minimum_support = 30
#Specify minimum confidence
minimum_confidence = 75

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_costco = main(costco,minimum_support,minimum_confidence)

#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Costco with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_costco,'\n')
print('---------------------------------------------------------------------')
#Printing Final association rules in format A,B --> C
print("Final Association Rules for costco with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_costco['Rule_Confidence'])):
    print ("{}) {} --> {}  ".format(i+1, rules_costco['Antecedent'][i],rules_costco['Consequent'][i]))


# #### Running Costco dataset with support 40% and confidence 40%

# In[19]:


#Specify minimum support
minimum_support = 40
#Specify minimum confidence
minimum_confidence = 40

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_costco = main(costco,minimum_support,minimum_confidence)

#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Costco with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_costco,'\n')
print('---------------------------------------------------------------------')
#Printing Final association rules in format A,B --> C
print("Final Association Rules for costco with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_costco['Rule_Confidence'])):
    print ("{}) {} --> {}  ".format(i+1, rules_costco['Antecedent'][i],rules_costco['Consequent'][i]))


# ## Determining Association Rules for Nike

# #### Running Nike dataset with support 60% and confidence 60%

# In[20]:


nike = '/Users/veena/Desktop/Dmining/Projects/Datasets/Nike.csv'
#Specify minimum support
minimum_support = 60
#Specify minimum confidence
minimum_confidence = 60
#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_nike = main(nike,minimum_support,minimum_confidence)

print('***************** NIKE *****************')
#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Nike with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_nike,'\n')
print('---------------------------------------------------------------------')
#Printing Final association rules in format A,B --> C
print("Final Association Rules for Nike with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_nike['Rule_Confidence'])):
    print ("{}) {} --> {}  ".format(i+1, rules_nike['Antecedent'][i],rules_nike['Consequent'][i]))


# #### Running Nike dataset with support 60% and confidence 90%

# In[21]:


#Specify minimum support
minimum_support = 60
#Specify minimum confidence
minimum_confidence = 90

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_nike = main(nike,minimum_support,minimum_confidence)

#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Nike with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_nike,'\n')
print('---------------------------------------------------------------------')
#Printing Final association rules in format A,B --> C
print("Final Association Rules for Nike with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_nike['Rule_Confidence'])):
    print ("{}) {} --> {}  ".format(i+1, rules_nike['Antecedent'][i],rules_nike['Consequent'][i]))


# #### Running Nike dataset with support 55% and confidence 55%

# In[22]:


#Specify minimum support
minimum_support = 55
#Specify minimum confidence
minimum_confidence = 55

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_nike = main(nike,minimum_support,minimum_confidence)

#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Nike with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_nike,'\n')
print('---------------------------------------------------------------------')
#Printing Final association rules in format A,B --> C
print("Final Association Rules for Nike with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_nike['Rule_Confidence'])):
    print ("{}) {} --> {}  ".format(i+1, rules_nike['Antecedent'][i],rules_nike['Consequent'][i]))


# #### Running Nike dataset with support 55% and confidence 70%

# In[23]:


#Specify minimum support
minimum_support = 55
#Specify minimum confidence
minimum_confidence = 70

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_nike = main(nike,minimum_support,minimum_confidence)

#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Nike with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_nike,'\n')
print('---------------------------------------------------------------------')
#Printing Final association rules in format A,B --> C
print("Final Association Rules for Nike with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_nike['Rule_Confidence'])):
    print ("{}) {} --> {}  ".format(i+1, rules_nike['Antecedent'][i],rules_nike['Consequent'][i]))


# ## Determining Association Rules for Generic

# #### Running Generic dataset with support 20% and confidence 90%

# In[24]:


generic = '/Users/veena/Desktop/Dmining/Projects/Datasets/Generic.csv'
#Specify minimum support
minimum_support = 20
#Specify minimum confidence
minimum_confidence = 90

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_generic = main(generic,minimum_support,minimum_confidence)

print('***************** GENERIC *****************')
#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Generic with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_generic,'\n')
print('---------------------------------------------------------------------\n')
#Printing Final association rules in format A,B --> C
print("Final Association Rules Generic with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_generic['Rule_Confidence'])):
    print ("{}) {} --> {}  ".format(i+1, rules_generic['Antecedent'][i],rules_generic['Consequent'][i]))


# #### Running Generic dataset with support 35% and confidence 95%

# In[25]:


#Specify minimum support
minimum_support = 35
#Specify minimum confidence
minimum_confidence = 95

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_generic = main(generic,minimum_support,minimum_confidence)

#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Generic with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_generic,'\n')
print('---------------------------------------------------------------------\n')
#Printing Final association rules in format A,B --> C
print("Final Association Rules Generic with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_generic['Rule_Confidence'])):
    print ("{}) {} --> {}  ".format(i+1, rules_generic['Antecedent'][i],rules_generic['Consequent'][i]))


# #### Running Generic dataset with support 40% and confidence 42%

# In[26]:


#Specify minimum support
minimum_support = 40
#Specify minimum confidence
minimum_confidence = 42

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_generic = main(generic,minimum_support,minimum_confidence)

#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Generic with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_generic,'\n')
print('---------------------------------------------------------------------\n')
#Printing Final association rules in format A,B --> C
print("Final Association Rules Generic with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_generic['Rule_Confidence'])):
    print ("{}) {} --> {}  ".format(i+1, rules_generic['Antecedent'][i],rules_generic['Consequent'][i]))


# #### Running Generic dataset with support 10% and confidence 70%

# In[27]:


#Specify minimum support
minimum_support = 10
#Specify minimum confidence
minimum_confidence = 70

#To determine association rules, the abover parameters(minimum support and confidence) are passed to main function alogn with the datset
for_rules,rules_generic = main(generic,minimum_support,minimum_confidence)

#Printing all Rules which satify mininmum confidence criterion. Rules: Tansactiona --> Transaction 
print('\n All association rules for Generic with support = {} and Confidence = {} \n' .format(minimum_support, minimum_confidence))
print(rules_generic,'\n')
print('---------------------------------------------------------------------\n')
#Printing Final association rules in format A,B --> C
print("Final Association Rules Generic with support = {} and Confidence = {} \n" .format(minimum_support, minimum_confidence))
for i in range(len(rules_generic['Rule_Confidence'])):
    print ("{}) {} --> {}  ".format(i+1, rules_generic['Antecedent'][i],rules_generic['Consequent'][i]))

