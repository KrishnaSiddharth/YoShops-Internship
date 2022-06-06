#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings('ignore')


# In[1]:


import pandas as pd
import numpy as np
import PyPDF2
from os import remove
from os import startfile


# In[3]:


review = pd.read_csv('review_dataset.csv')


# In[4]:


order = pd.read_csv('orders_2016-2020_Dataset.csv')


# In[5]:


review.head()


# In[6]:


review.shape


# In[7]:


review.info()


# In[8]:


review.isnull().sum() # Number of missing values


# In[9]:


review['status']


# In[10]:


review['status'].unique()


# In[11]:


review['status'] = review['status'].fillna('Reviewd')


# In[12]:


review['stars']


# In[13]:


review['stars'].unique()


# In[14]:


review['stars'].mode()


# In[15]:


review['stars'] = review['stars'].fillna('no_review')


# In[16]:


review.isnull().sum()


# In[17]:


review['stars'].value_counts()


# In[18]:


import matplotlib.backends.backend_tkagg
import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import seaborn as sns


# In[19]:


review['stars']


# In[20]:


review['stars'] = review['stars'].str.split(' ')


# In[21]:


review['stars']


# In[22]:


spilt_review_dataframe = pd.DataFrame(review['stars'].tolist())
spilt_review_dataframe


# In[23]:


review['stars'] = spilt_review_dataframe[0]


# In[24]:


review['stars']


# In[25]:


review['stars'].unique()


# ## Task - 1

# In[26]:


plt.figure(figsize=(20,10))
sns.countplot(review['stars']).set_title('Analysis of Reviews given by Customers')
plt.savefig('edatask1.pdf')


# ## Task - 2

# In[27]:


order.head()


# In[28]:


order.isnull().sum()


# In[29]:


order['Payment Method'].unique()


# In[30]:


order['Payment Method'].mode()


# In[31]:


order['Payment Method'] = order['Payment Method'].fillna('Offline Payment ₹1,499.00')


# In[32]:


order['Payment Method'] = order['Payment Method'].str.split('₹')


# In[33]:


order['Payment Method']


# In[34]:


split_dataframe = pd.DataFrame(order['Payment Method'].tolist())


# In[35]:


split_dataframe[0].unique()


# In[36]:


split_dataframe[0]


# In[37]:


order['Payment Method'] = split_dataframe[0]


# In[38]:


order.head()


# In[39]:


order['Payment Method'].unique()


# In[40]:


order['Payment Method'].value_counts()


# In[41]:


edatask2 = sns.countplot(order['Payment Method']).set(title='Analysis of Payment Methods')
plt.savefig('edatask2.pdf')


# ## Task - 3

# In[42]:


order.isnull().sum() / order.shape[0] * 100


# In[43]:


order['Billing State'].unique()


# In[44]:


order['Billing State'].mode()


# In[45]:


order['Billing State'] = order['Billing State'].fillna('IN-TN')


# In[46]:


order['Billing State'].isnull().sum()


# In[47]:


order['Billing State'].value_counts()[0:3] 


# In[48]:


plt.figure(figsize=(20,10))
sns.countplot(order['Billing State']).set_title('Analysis of Top Consumer Indian States')
plt.savefig('edatask3.pdf')


# ## Task - 4

# In[49]:


order['Billing City'].unique()


# In[50]:


order['Billing City'].mode()


# In[51]:


order['Billing City'] = order['Billing City'].fillna('Chennai')


# In[52]:


order['Billing City'].value_counts()[0:3]


# In[53]:


order['Billing City'] = order['Billing City'].replace('chennai', 'Chennai')


# In[54]:


order['Billing City'].value_counts()


# In[55]:


orderCleaned = order["Billing City"]
filter1 = orderCleaned != "test"
filter2 = orderCleaned != "TAMILNADU"
filter3 = orderCleaned != "dwwwwwwww"
filter4 = orderCleaned != "rgtvrg"
orderCleaned = orderCleaned.where(filter1 & filter2 & filter3 & filter4, inplace = False).replace('CHENNAI', 'Chennai')
orderCleaned.unique()


# In[56]:


plt.figure(figsize=(20,10))
sns.countplot(orderCleaned, order=orderCleaned.value_counts().iloc[:10].index).set_title('Analysis of Top Consumer Indian Cities')
plt.savefig('edatask4.pdf')


# ## Task - 5

# In[57]:


review['category'].isnull().sum()


# In[58]:


review['category'].value_counts()


# In[59]:


review['category'].mode()


# In[60]:


review['category'] =review['category'].replace('Chennai','Mobiles')
review['category'] =review['category'].replace('Bengaluru','Mobiles')
review['category'] =review['category'].replace('Mumbai','Mobiles')


# In[61]:


review['category'].value_counts()[0:3]


# In[62]:


plt.figure(figsize = (20,10))
sns.countplot(review['category'], order=review['category'].value_counts().iloc[:10].index).set_title('Analysis of Top Selling Product Categories')
plt.savefig('edatask5.pdf')


# ## Task - 6

# In[63]:


review['stars'].unique()


# In[64]:


reviewlist = review['category'].value_counts().index.tolist()[:10]
selectedCategories = review[['category','stars']]
selectedCategories = selectedCategories[selectedCategories['category'].isin(reviewlist)]   ## https://stackoverflow.com/questions/27965295/dropping-rows-from-dataframe-based-on-a-not-in-condition

for index in selectedCategories.index:
    if (selectedCategories['stars'][index] != 'no_review'):
        x = float(selectedCategories['stars'][index])
        if x >=  4.5 and x <  5:
            selectedCategories['stars'][index] = '4.5-5'
        if x >=  4.0 and x <  4.5:
            selectedCategories['stars'][index] = '4.0-4.5'
        if x >=  3.5 and x <  4:
            selectedCategories['stars'][index] = '3.5-4.0'
        if x >=  3.0 and x <  3.5:
            selectedCategories['stars'][index] = '3.0-3.5'
        if x >=  2.5 and x <  3:
            selectedCategories['stars'][index] = '2.5-3.0'
        if x >=  2.0 and x <  2.5:
            selectedCategories['stars'][index] = '2.0-2.5'

selectedCategories['stars'].unique()


# In[65]:


selectedCategories = selectedCategories.groupby('category').value_counts().to_frame()
selectedCategories.columns = ['Count']
selectedCategories


# In[66]:


selectedCategories['Count'].astype(int) ## Converting the last count column from string to int for plotting


# In[67]:


selectedCategories = selectedCategories.unstack(level = 'stars').fillna(0)
cols_to_sum_stars = selectedCategories.columns[0:5].values
selectedCategories['Total (Reviewed)'] = selectedCategories[cols_to_sum_stars].sum(axis = 1)
cols_to_sum_stars = selectedCategories.columns[0:6].values
selectedCategories['Grand Total'] = selectedCategories[cols_to_sum_stars].sum(axis = 1)
selectedCategories


# In[69]:


df_total_2 = selectedCategories['Total (Reviewed)']
df_2 = selectedCategories.iloc[:, 0:5]
df_2.plot(kind='barh',stacked = True, title = 'Review Analysis of top 10 products (Only Reviewed Orders)', mark_right = True, figsize=(20, 20))

df_rel_2 = df_2[df_2.columns[1:]].div(df_total_2, 0)*100

for n in df_rel_2:
    for i, (cs, ab, pc, tot) in enumerate(zip(df_2.iloc[:, 1:].cumsum(1)[n], df_2[n], df_rel_2[n], df_total_2)):
        if pc >= 30:
            plt.text(cs - ab/2, i, str(np.round(pc, 1)) + '%', va='center', ha='center')
        elif (pc >=10 and pc < 30):
            plt.text(cs - ab/2, i, str(np.round(pc, 1)) + '%', va='center', ha='center', rotation=90)

plt.savefig('edatask6_2.pdf')
            
df_total_1 = selectedCategories['Grand Total']
df_1 = selectedCategories.iloc[:, 0:6]
df_1.plot(kind='barh',stacked = True, title = 'Analysis of top 10 products (Reviewed and Unreviewed Orders)', mark_right = True, figsize=(20, 20))

df_rel_1 = df_1[df_1.columns[1:]].div(df_total_1, 0)*100

for n in df_rel_1:
    for i, (cs, ab, pc, tot) in enumerate(zip(df_1.iloc[:, 1:].cumsum(1)[n], df_1[n], df_rel_1[n], df_total_1)):
        if pc >= 30:
            plt.text(cs - ab/2, i, str(np.round(pc, 1)) + '%', va='center', ha='center')
        elif (pc >=10 and pc < 30):
            plt.text(cs - ab/2, i, str(np.round(pc, 1)) + '%', va='center', ha='center', rotation=90)

plt.savefig('edatask6_1.pdf')  

pdfs = ['edatask6_2.pdf', 'edatask6_1.pdf']

merger = PyPDF2.PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("edatask6.pdf")
merger.close()


# In[70]:


for pdf in pdfs:
    remove(pdf)


# 
# ## Task - 7

# In[71]:


#to see the analysis of Number of Orders Per Month Per Year


# In[72]:


order['Order Date and Time Stamp']


# In[73]:


order['months'] = pd.DatetimeIndex(order['Order Date and Time Stamp']).month


# In[74]:


order['year'] = pd.DatetimeIndex(order['Order Date and Time Stamp']).year


# In[75]:


order


# In[76]:


order['LineItem Qty'].unique()


# In[77]:


order.groupby('year')['LineItem Qty'].count()


# In[78]:


order.groupby('months')['LineItem Qty'].count().sort_values(ascending=False).plot.barh()


# In[79]:


order.groupby('year')['LineItem Qty'].count().sort_values(ascending=False).plot.barh()


# In[80]:


order.groupby(['year', 'months'])['LineItem Qty'].count()


# In[81]:


order16 = order


# In[82]:


order2016 = order16.groupby(['year', 'months'])['LineItem Qty'].count()  ## This would result in a series


# In[83]:


order2016df = order2016.to_frame()  ## The series is converted into a data frame


# In[84]:


order2016df


# In[85]:


orderDataFrameYear = order2016df.unstack(level='months')    ## Now the dataframe is unstacked! Very powerful method!!


# In[86]:


orderDataFrameYear = orderDataFrameYear.fillna(0)
orderDataFrameYear


# In[87]:


orderDataFrameYear.plot( kind='bar', stacked=True, title='Breakdown of Costs', mark_right=True, figsize=(10, 15))  


# In[88]:


orderDataFrameMonth = order2016df.unstack(level='year') 


# In[89]:


orderDataFrameMonth = orderDataFrameMonth.fillna(0)
orderDataFrameMonth


# In[90]:


orderDataFrameMonth.plot( kind='bar', stacked=True, title='Breakdown of Costs', mark_right=True, figsize=(10, 15))  


# In[91]:


orderDataFrameMonthTotal = orderDataFrameYear.sum()


# In[92]:


orderDataFrameMonthTotal


# In[93]:


for column in orderDataFrameYear:
    orderDataFrameYear[column].astype(int)   ## Converting all the values in the dataframe to int


# In[94]:


for column in orderDataFrameMonth:
    orderDataFrameMonth[column].astype(int)


# In[95]:


cols_to_sum_year = orderDataFrameYear.columns.values
cols_to_sum_year


# In[96]:


orderDataFrameYear['Total'] = orderDataFrameYear[cols_to_sum_year].sum(axis = 1)
orderDataFrameYear


# In[97]:


cols_to_sum_month = orderDataFrameMonth.columns.values
cols_to_sum_month


# In[98]:


orderDataFrameMonth['Total'] = orderDataFrameMonth[cols_to_sum_month].sum(axis = 1)
orderDataFrameMonth


# In[99]:


df_total = orderDataFrameMonth['Total']
df = orderDataFrameMonth.iloc[:, 0:5]
figure7 = df.plot(kind='barh',stacked = True, title = 'Analysis of Number of Orders Per Month Per Year', mark_right = True, figsize=(20, 20))

df_rel = df[df.columns[1:]].div(df_total, 0)*100

for n in df_rel:
    for i, (cs, ab, pc, tot) in enumerate(zip(df.iloc[:, 1:].cumsum(1)[n], df[n], df_rel[n], df_total)):
        if pc >= 30:
            plt.text(cs - ab/2, i, str(np.round(pc, 1)) + '%', va='center', ha='center')
        elif (pc >=10 and pc < 30):
            plt.text(cs - ab/2, i, str(np.round(pc, 1)) + '%', va='center', ha='center', rotation=90)

plt.savefig('edatask7.pdf')


# In[100]:


review['product_name'].unique()


# # Task 8

# In[101]:


order['Review'] = np.nan
for i in order['LineItem Name'].index:
    for j in review['product_name'].index:
        if order['LineItem Name'][i].strip().replace(" ", "") == review['product_name'][j].strip().replace(" ", ""):
            order['Review'][i] = review['stars'][j]


# In[102]:


order['Review'] = order['Review'].fillna('no_review')


# In[103]:


order_review = order.iloc[:,-3:]


# In[104]:


order_review['Count'] = np.nan


# In[105]:


order_review['Count'] = order_review['Count'].fillna(1)


# In[106]:


for ind in order_review.index:
    if order_review['Review'][ind] != 'no_review':
        if float(order_review['Review'][ind]) >= 4.5 and float(order_review['Review'][ind]) <= 5:
            order_review['Review'][ind] = '4.5-5'
        elif float(order_review['Review'][ind]) >= 4.0 and float(order_review['Review'][ind]) < 4.5:
            order_review['Review'][ind] = '4.0-4.5'
        elif float(order_review['Review'][ind]) >= 3.5 and float(order_review['Review'][ind]) < 4:
            order_review['Review'][ind] = '3.5-4'
        elif float(order_review['Review'][ind]) >= 3.0 and float(order_review['Review'][ind]) < 3.5:
            order_review['Review'][ind] = '3-3.5'
        elif float(order_review['Review'][ind]) < 3:
            order_review['Review'][ind] = 'Less than 3'


# In[113]:


order_review['Review'].unique()


# In[114]:


pdfs = []

for year in order_review['year'].unique():
    df = order_review[order_review['year'] == year].groupby(['months', 'year', 'Review']).count()['Count']
    # plot the result
    df.unstack().plot(title = "Review Analysis of Orders per Month in "+str(year),figsize = (10,10))
    plt.xticks(rotation=30)
    plt.savefig('edatask8_'+str(year)+'.pdf')
    pdfs.append('edatask8_'+str(year)+'.pdf')

merger = PyPDF2.PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("edatask8.pdf")
merger.close()


# In[115]:


for pdf in pdfs:
    remove(pdf)


# # Task 9

# In[116]:


review_parts_day = pd.DataFrame()
review_parts_day['Time'] = order['months'] = pd.DatetimeIndex(order['Order Date and Time Stamp']).hour
review_parts_day['LineItem Qty'] = order['LineItem Qty']
review_parts_day


# In[117]:


for ind in review_parts_day.index:
    if float(review_parts_day['Time'][ind]) >= 6 and float(review_parts_day['Time'][ind]) < 9:
        review_parts_day['Time'][ind] = "Morning (6:00-9:00)"
    elif float(review_parts_day['Time'][ind]) >= 9 and float(review_parts_day['Time'][ind]) < 12:
        review_parts_day['Time'][ind] = "Late Morning (9:00-12:00)"
    elif float(review_parts_day['Time'][ind]) >= 12 and float(review_parts_day['Time'][ind]) < 15:
        review_parts_day['Time'][ind] = "Afternoon (12:00-15:00)"
    elif float(review_parts_day['Time'][ind]) >= 15 and float(review_parts_day['Time'][ind]) < 18:
        review_parts_day['Time'][ind] = "Evening (15:00-18:00)"
    elif float(review_parts_day['Time'][ind]) >= 18 and float(review_parts_day['Time'][ind]) < 21:
        review_parts_day['Time'][ind] = "Night (18:00-21:00)"
    elif float(review_parts_day['Time'][ind]) >= 21:
        review_parts_day['Time'][ind] = "Late Night (21:00-00:00)"
    elif float(review_parts_day['Time'][ind]) >= 0 and float(review_parts_day['Time'][ind]) < 3:
        review_parts_day['Time'][ind] = "Mid Night (00:00-03:00)"
    elif float(review_parts_day['Time'][ind]) >= 3 and float(review_parts_day['Time'][ind]) < 6:
        review_parts_day['Time'][ind] = "Early Morning (03:00-06:00)"
review_parts_day


# In[118]:


plt.figure(figsize = (20,10))
review_parts_day.groupby('Time')['LineItem Qty'].count().sort_values(ascending=False).plot.barh().set_title('Analysis of Number of Orders across different parts of the Day')
plt.savefig('edatask9.pdf')


# # Task 10

# In[119]:


merger = PyPDF2.PdfMerger()
for i in range(1,10):
    merger.append('edatask'+str(i)+'.pdf')

merger.write("Full Report.pdf")
merger.close()


# In[2]:


import tkinter

master=tkinter.Tk()
master.geometry("400x260")

def click(type):
    startfile('edatask'+type+'.pdf')

button1=tkinter.Button(master, text="1. Analysis of Customer Reviews", command = lambda:click('1'))
button1.grid(row=1,column=0, ipadx = '0px')

button2=tkinter.Button(master, text="2. Analysis of Customer Payment Methods", command = lambda:click('2'))
button2.grid(row=2,column=0, padx= '0px')

button3=tkinter.Button(master, text="3. Analysis of Top Consumer Indian States", command = lambda:click('3'))
button3.grid(row=3,column=0, padx= '0px')

button4=tkinter.Button(master, text="4. Analysis of Top Indian Consumer Cities", command = lambda:click('4'))
button4.grid(row=4,column=0, padx= '0px')

button5=tkinter.Button(master, text="5. Analysis of Top Selling Product Categories", command = lambda:click('5'))
button5.grid(row=5,column=0, padx= '0px')

button6=tkinter.Button(master, text="6. Analysis of Top Product Category Reviews", command = lambda:click('6'))
button6.grid(row=6,column=0, padx= '0px')

button7=tkinter.Button(master, text="7. Analysis of Number of Orders Per Month Per Year", command = lambda:click('7'))
button7.grid(row=7,column=0, padx= '0px')

button8=tkinter.Button(master, text="8. Review Analysis for Number of Orders per Month per Year", command = lambda:click('8'))
button8.grid(row=8,column=0, padx= '20px')

button9=tkinter.Button(master, text="9. Analysis of Number of Orders across parts of a Day", command = lambda:click('9'))
button9.grid(row=9,column=0, padx= '0px')

button10=tkinter.Button(master, text="10. Full Report", command = lambda: startfile('Full Report.pdf'))
button10.grid(row=10,column=0, padx= '0px')

master.mainloop()


# In[ ]:




