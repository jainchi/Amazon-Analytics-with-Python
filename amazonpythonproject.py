print("Amazon Project")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np



# Reading Files

categories=pd.read_csv('category.csv')
# print(categories.head())

customers=pd.read_csv('customers.csv')
# print(customers.head())

inventory=pd.read_csv('inventory.csv')
# print(inventory.head())

orders=pd.read_csv('orders.csv')
# print(orders.head())
orders['order_date'] = pd.to_datetime(orders['order_date'])

order_items=pd.read_csv('order_items.csv') 
# print(order_items.head())

payments=pd.read_csv('payments.csv')
# print(payments.head())

products=pd.read_csv('products.csv')
# print(products.head())

sellers=pd.read_csv('sellers.csv')
# print(sellers.head())

shippings=pd.read_csv('shipping.csv')
# print(shippings.head())
shippings['shipping_date'] = pd.to_datetime(shippings['shipping_date'])
# print(shippings['delivery_status'].unique())
shippings['delivery_status']= shippings['delivery_status'].str.strip()



# ############
# primary keys =>>
# categories: category_id,customers: customer_id, inventory: inventory_id, orders: order_id, order_items: order_item_id, payments: payment_id,
# products: product_id, sellers: seller_id, shippings: shipping_id



### Category Murder:
procat=pd.merge(products,categories,on='category_id',how='inner')

# #Q1 Revenue by category
def category_q1():

    procatorder=pd.merge(procat,order_items,on='product_id',how='left')

    procatorder['revenue'] = procatorder['price'] * procatorder['quantity']
    revbycategory=procatorder.groupby(['category_id','category_name'])['revenue'].sum().sort_values(ascending=False)
    print(revbycategory)

    revbycategory=pd.DataFrame(revbycategory)
    plt.figure(figsize=(11,6))
    sns.barplot(data=revbycategory,x='category_name',y='revenue',color='orange')
    plt.ticklabel_format(style='plain', axis='y')
    plt.title('Total Revenue by Category')
    plt.show()

# # Q2: What is the percentage revenue or quantity contribution of each category relative to total sales?
def category_q2():

    procatitem=procat.merge(order_items,on='product_id', how='inner')
    # print(procatitem)
    print((procatitem.groupby(['category_id','category_name'])['quantity'].sum()/procatitem['quantity'].sum())*100)

# # # Q3: Unique customers per category?

def category_q3():
    cusorder=customers.merge(orders,on='customer_id',how="inner")
    cusorderitems=cusorder.merge(order_items,on='order_id',how='inner')
    cusorderitemsprod=cusorderitems.merge(products,on='product_id',how='inner')
    cusorderitemsprodcat=cusorderitemsprod.merge(categories,on='category_id',how='inner')

    Q3=cusorderitemsprodcat.groupby(['category_id','category_name'])['customer_id'].nunique().reset_index().sort_values(by='customer_id',ascending=False)
    print(Q3)

    plt.figure(figsize=(11,5))
    sns.barplot(data=Q3,y='category_name',x='customer_id',color='orange')
    plt.bar_label(plt.gca().containers[0])
    plt.title('Customer Count by category')
    plt.xlabel('Customer_ids Count')
    plt.show()

# Q4 Which and how many seller sells in all categories?

def category_q4():
    sellord=sellers.merge(orders,on='seller_id',how='inner')
    sellorditems=sellord.merge(order_items,on='order_id',how='inner')
    sellorditemsprod=sellorditems.merge(products,on='product_id',how='inner')
    sellorditemsprodcat=sellorditemsprod.merge(categories,on='category_id',how='inner')
    Q4=sellorditemsprodcat.groupby(['seller_id','seller_name'])['category_id'].nunique().reset_index().rename(columns={'category_id':'totalids'})
    print(Q4[Q4.totalids==len(categories)].reset_index())
    print((Q4.totalids==len(categories)).value_counts())






# ####Customers Murder

custord=customers.merge(orders,on='customer_id',how='left')
custordleftanti=customers.merge(orders,on='customer_id',how='left_anti')
custorder=customers.merge(orders,on='customer_id',how='inner')
custorditemsinner=custorder.merge(order_items,on='order_id',how='inner')
custorditemsleft=custord.merge(order_items,on='order_id',how='left')



# ### customer life-time value

def customer_q1():
    custorditemsleft['revenue'] = custorditemsleft['price_per_unit'] * custorditemsleft['quantity']
    # print(custorditems)
    Q1=custorditemsleft.groupby(['customer_id','first_name','last_name'])['revenue'].sum().sort_values(ascending=False)
    print(Q1)



# ### Customers with no purchases Q.2

def customer_q2():
    print(custordleftanti)



# #Q3: What are the total quantities sold across different states (to determine the least-selling categories/products by state)?

def customer_q3():
    Q3=custorditemsleft.groupby(['state'])['quantity'].sum().sort_values(ascending=False)
    print(Q3)
    # We connected customers to extract state.


    Q3=pd.DataFrame(Q3)
    plt.figure(figsize=(13,6))
    sns.barplot(data=Q3,x='state',y='quantity',color='orange')
    plt.title('Total Quantity Sold by States')
    plt.xticks(rotation=90)
    plt.bar_label(plt.gca().containers[0],size=6)
    plt.show()



# print("Q.4")
# # Repeat customer rate Q.4
def customer_q4():   
    Q4=custorder.groupby('customer_id')['order_id'].count().sort_values(ascending=False)
    # print(Q4)
    Q4_repeat_rate = (Q4[Q4 > 1].count() / Q4.count()) * 100
    print(Q4_repeat_rate)



# print("Q.5")

# # # Multi-month repeat customer rateQ.5
def customer_q5():
    orders['order_month'] = orders['order_date'].dt.to_period('M')
    customer_months = orders.groupby('customer_id')['order_month'].nunique()
    # print(customer_months.sort_values())
    retained_customers = (customer_months > 1).sum()
    total_customers = customer_months.count()
    print((retained_customers/total_customers)*100)



# print("Q.6")
# Give me only customers who have purchased more than the average quantity Q.6

def customer_q6():
    quantitycount=custorditemsinner.groupby(['customer_id','first_name','last_name'])['quantity'].sum().sort_values(ascending=False).reset_index()
    # print(quantitycount)
    aa=quantitycount.agg({'quantity':np.mean})
    print(quantitycount[quantitycount['quantity']>aa['quantity']])
    # print(aa)



# # customer return ? Q.7
# print("Q.7")
custordship=custord.merge(shippings,on='order_id',how='inner')
custordshipreturned=custordship[custordship['delivery_status']=='Returned']

def customer_q7():
    custordship=custord.merge(shippings,on='order_id',how='inner')
    custordshipreturned=custordship[custordship['delivery_status']=='Returned']
    print(custordshipreturned)

##subquestion: tell me customers who returned most

def customer_q7_sub1():
    topreturnedcustomer=custordshipreturned.groupby('customer_id')['order_id'].count().sort_values(ascending=False).reset_index().head(20)
    print(topreturnedcustomer)

# #Subquestion: DO top 20 customers{returned} comes in top 20 customer{by no.of purchase}
topcustomersbyorder=custordship.groupby('customer_id')['order_id'].count().reset_index().rename(columns={'order_id':'totalorders'}).sort_values(by='totalorders',ascending=False).head(50)

def customer_q7_sub2():
    print(topcustomersbyorder)
    print("Insight: Only 30 of 682 customers (≈4.4%) have ever had a returned order — the remaining 652 customers (≈95.6%) have a '0%' return rate across their entire order history.Within that small group, the pattern is unusually extreme: most of these 30 customers return '100%' of the orders they place, rather than a mix of kept and returned items.")


#Subquestion: To which states these customers belongs to

# print(custordshipreturned.groupby('state')['order_id'].count().sort_values())
def customer_q7_sub3():
    print(custordshipreturned.groupby('state')['customer_id'].nunique().sort_values())
# print(customers['state'].nunique())

# "Out of 49 states of our data,  these customers belongs to total 7 states"



# Q8: Who are the top customers by total order count within each state?
def customer_q8():
    sorted_df=custorditemsinner.groupby(['state','customer_id'])['order_id'].nunique().reset_index().sort_values(by=['state','order_id'],ascending=[True,False])
    top_per_state=sorted_df.groupby('state').head(2)
    print(top_per_state)



# # "Customers Insight"

"1. Custoerids{554,616,711,591,748,718,625,712,669,701}"
"2. Total 212 cuatomers are there with no purchase"
"3. 'Ohio','Texas','New York' "
"4. 94.46% of customers purchased more than 1 time"
"5. 686 out of total customers retained with us"
"6. 211 customers purchased more than average quantity in total {average quantity=61}"
"7. We have 2840 returns in total which are made by 30 unique customers from 7 unique states,State with maximum return is'South Carolina' "





# # # Seller's Murder


seller_order=sellers.merge(orders,on='seller_id',how='left')
seller_order_items=seller_order.merge(order_items,on='order_id',how='inner')
seller_order_items['revenue']=seller_order_items['quantity']*seller_order_items['price_per_unit']



# # #Q1 sellers revenue

revperseller=seller_order_items.groupby(['seller_id','seller_name'])['revenue'].sum().sort_values(ascending=False).reset_index()
def seller_q1():
    revperseller=seller_order_items.groupby(['seller_id','seller_name'])['revenue'].sum().sort_values(ascending=False).reset_index()
    print(revperseller)

    revperseller=pd.DataFrame(revperseller)
    plt.figure(figsize=(13,8))
    sns.barplot(data=revperseller,y='seller_name',x='revenue',color='orange')
    plt.title('Revenue by Sellers')
    plt.ticklabel_format(style='plain', axis='x')
    plt.show()

# # # Subquestion: Give me sellers whose revenue is greater as compare to average revenue of all sellers 
def seller_q1_sub1():
    avgseller_sales=(revperseller['revenue'].sum())/revperseller['seller_id'].count()
    greaterthanaverage=revperseller[revperseller['revenue']>avgseller_sales]
    print(greaterthanaverage)
    print(revperseller['seller_id'].count())



# # # Q.2 quanity sold by each seller
def seller_q2():
    sellerq_2=seller_order_items.groupby('seller_id')['quantity'].sum().sort_values(ascending=False)
    print(sellerq_2)

    sellerq_2=pd.DataFrame(data=sellerq_2)

    plt.figure(figsize=(11,6))
    sns.barplot(data=sellerq_2,x='seller_id',y='quantity',color='orange')
    plt.title('Quantity sold by Sellers')
    plt.show()


# # #Q.3 Which sellers have most customers?
def seller_q3():
    print(seller_order.groupby('seller_id')['customer_id'].nunique().sort_values(ascending=False).head(1))


    sellerq_3=seller_order.groupby('seller_id',as_index=False)['customer_id'].nunique()
    plt.figure(figsize=(13,5))
    sns.barplot(data=sellerq_3,x='seller_id',y='customer_id',color='orange')
    plt.title('Unique Customers by Sellers')
    plt.ylabel('Customer_count')
    plt.show()


# # #Q.4 Give me seller's count by their origins.
def seller_q4():
    print(sellers.groupby('origin')['seller_id'].nunique().sort_values(ascending=False))

    sellerq_4=sellers.groupby('origin')['seller_id'].nunique().sort_values(ascending=False)
    sellerq_4=pd.DataFrame(sellerq_4)
    plt.figure(figsize=(11,5))
    sns.barplot(data=sellerq_4,x='origin',y='seller_id',color='orange')
    plt.title('Seller Count by State')
    plt.ylabel('seller count')
    plt.show()

# # # # Q.5 In how many states a seller sells their items
def seller_q5():
    seller_order_customer=seller_order.merge(customers,on='customer_id',how="inner")
    print(seller_order_customer.groupby('seller_id')['state'].nunique().sort_values(ascending=False))
    # print(seller_order_customer)

# # #Q.6 Which sellers sells across all categories (Solved in categories murder)


# # #Q.7 Seller's returns
seller_order_ship=seller_order.merge(shippings,on='order_id',how='inner')
seller_order_ship_returned = seller_order_ship[seller_order_ship['delivery_status']=='Returned']
sellers_returns = seller_order_ship_returned.groupby(['seller_id','seller_name'])['order_id'].count()


def seller_q7():
    print(sellers_returns)

# # ##Subquestion: Do top sellers{returned} comes in top sellers{by no.of orders} ?

totalorderbysellers=seller_order_ship.groupby(['seller_id','seller_name'])['order_id'].count()
def seller_q7_sub1():    
    print((sellers_returns/totalorderbysellers)*100)



# # #Q.8 Which seller sells most no.of unique products
def seller_q8():
    order_orderitems=orders.merge(order_items,on='order_id',how="inner")
    print(order_orderitems.groupby('seller_id')['product_id'].nunique().sort_values(ascending=False).head(1))



# # #Q.9 Top sellers Y-O-Y revenue 
def seller_q9():
    seller_order_items['year']=seller_order_items['order_date'].dt.to_period('Y')
    yearly_revperseller=seller_order_items.groupby(['seller_id','seller_name','year'])['revenue'].sum().reset_index().sort_values(by=['seller_id','year'])
    previous_yearly_revperseller=yearly_revperseller.groupby('seller_id').shift(1)
    # print(yearly_revperseller.head(20))
    # print(previous_yearly_revperseller.head(20))
    print(100*(yearly_revperseller['revenue']-previous_yearly_revperseller['revenue'])/previous_yearly_revperseller['revenue'])

# # #or
print("Q-----9")

seller_order_items['year']=seller_order_items['order_date'].dt.to_period('Y')
yearly_revperseller=seller_order_items.groupby(['seller_id','seller_name','year'])['revenue'].sum().reset_index().sort_values(by=['seller_id','year'])
yearly_revperseller['prev_revenue'] = yearly_revperseller.groupby('seller_id')['revenue'].shift(1)

yearly_revperseller['growth_pct'] = 100 * ((yearly_revperseller['revenue'] - yearly_revperseller['prev_revenue'])
                                                                                          / yearly_revperseller['prev_revenue'])

# print(yearly_revperseller.head(20))


# # # Inactive sellers Q.10

def seller_q10():
    sellord=sellers.merge(orders,on='seller_id',how='left_anti')
    print(sellord)



# "Seller's Insights"

"1. We have 52 sellers in total."
"2. Seller Ids(2,3,1,4,5,23,24) are the ids of those sellers who generates more than average revenue."
"3. Seller Ids(2,4,3,5,1) are the ids of top 5 sellers arranged in descending order {on basis of quantity sold}."
"4. Our most of the sellers belongs to The USA"
"5. 38 maximum, 3 minimum, "
"7. Amazon Basics have most returns."
"Bigger sellers aren't systematically better or worse at avoiding returns,they simply generate more absolute returns because they sell more, which is expected and healthy."
"Maximum return rate of a seller lie at 29.03% amd minimum return rate lies at 4.16%"
"8. Seller with Id 2 sells 596 products, which is maximum among all."

"9. The dataset's order history ends July 30, 2024, giving 2024 roughly 58% of a full year's worth of trading days versus prior years."
" Every seller shows an apparent 83--87% YoY revenue 'decline' in 2024 — but this is a data-completeness artifact, not a genuine business downturn,"






# #### Products Murder

product_items=products.merge(order_items,on='product_id',how="left")
product_items['revenue']=product_items['price_per_unit']*product_items['quantity']

product_order_items=product_items.merge(orders,on='order_id',how="left")
# #Q.1 Revenue by product
def products_q1():
    revenueby_product=product_items.groupby(['product_id','product_name'])['revenue'].sum().sort_values(ascending=False)
    print(revenueby_product)

# #Sub-question- Is there any product which is getting sold by more than half of sellers?

print(product_order_items)
def products_q1_sub1():
    prodq_1=(product_order_items.groupby(['product_id','product_name'],as_index=False)['seller_id'].nunique()>len(sellers['seller_id'])/2).value_counts()
    print((product_order_items.groupby(['product_id','product_name'])['seller_id'].nunique()>len(sellers['seller_id'])/2))
    


# Q.2 product sold in how many states

product_order_items_customer=product_order_items.merge(customers,on='customer_id',how="inner")
def products_q2():
    print(product_order_items_customer.groupby(['product_id','product_name'])['state'].nunique().sort_values(ascending=False))




# print("q.3")
# #Q3 each product is purchased by how many customers

def products_q3():
    print(product_order_items_customer.groupby(['product_id','product_name'])['customer_id'].nunique().sort_values(ascending=False))


# #Q.4 returns
# print("q.4")
shippings_orders=orders.merge(shippings,on='order_id',how="inner")
shippings_orders_items=shippings_orders.merge(order_items,on='order_id',how="inner")
shippings_returned_orders=shippings_orders_items[shippings_orders_items['delivery_status']=='Returned']
# print(shippings_returned_orders)
print('Q4')
def products_q4():
    productsq_4=shippings_returned_orders.groupby('product_id',as_index=False)['order_id'].nunique().sort_values(by='order_id',ascending=False).head(20)
    print(productsq_4)

    plt.figure(figsize=(13,7))
    plt.title('Top 20 Product_id by total orders')
    sns.barplot(data=productsq_4,x='product_id',y='order_id',color='orange')
    plt.ylabel('Total Orders')
    plt.show()


# ## Year-over-year product revenue decline Q.5

proditem=products.merge(order_items,on='product_id',how='inner')
proditemorder=proditem.merge(orders,on='order_id',how='inner')

proditemorder['year'] = proditemorder['order_date'].dt.year
proditemorder['revenue'] = proditemorder['price_per_unit'] * proditemorder['quantity']

groupbyrevenue=proditemorder.groupby(['product_id','product_name','year'])['revenue'].sum().reset_index()
groupbyrevenue = groupbyrevenue.sort_values(['product_id', 'year'])
groupbyrevenue['prevrevenue']=groupbyrevenue.groupby('product_id')['revenue'].shift(1)

groupbyrevenue['realgrowth']=groupbyrevenue['revenue']-groupbyrevenue['prevrevenue']
groupbyrevenue['percent_change']= 100*(groupbyrevenue['revenue']-groupbyrevenue['prevrevenue'])/groupbyrevenue['prevrevenue']
# print(groupbyrevenue.head(50))

# Products with decline
decline = groupbyrevenue[groupbyrevenue['percent_change'] < 0]
def products_q5():
    print(decline.head(100))
    print("Note: We have partial 2024 data!!! ")






# #Insights ::::>>>>>>

"1. Best Revenue Product is AppleiMacPro. There are some products which are not contributing anything into revenue"
"686 products are there which are getting sold by more than half of the sellers"
"2. Apple AirPods Max  get sold in maximum states and also have most customers, "
"                                              but it do not generate highest revenue and also do not get sold by more than half of the sellers."
"3. Product_id 6 had maximum returns of 23 in total,so it should be investigated for potential quality or logistics issues because it has the highest number of returns."







### Miscellaneous Killing:-



# # Revenue by shipping provider Q.1
def mis_q1():
    shipitems=shippings.merge(order_items,on='order_id',how='inner')
    shipitems['revenue'] = shipitems['price_per_unit'] * shipitems['quantity']
    misq_1=shipitems.groupby('shipping providers',as_index=False)['revenue'].sum()
    print(misq_1)

    sns.barplot(data=misq_1,x='shipping providers',y='revenue',color='orange',legend=True)
    plt.ticklabel_format(style='plain', axis='y')
    plt.title('Total Revenue by Shipping Providers')
    plt.show()

# fedex contributed most among shipping providers


#Inventory Stock Alert Q.2:
def mis_q2():
    prodinvent=products.merge(inventory,on='product_id',how='inner')
    print(prodinvent[prodinvent['stock']<30])
# 236 products have less stock


#Q.3 quantity breakdown
def mis_q3():
    misq_3=order_items.groupby('quantity',as_index=False)['order_id'].nunique()
    print(misq_3)

    plt.figure(figsize=(10,5))
    sns.barplot(data=misq_3,x='quantity',y='order_id',color='orange')
    plt.ylabel('Total Orders')
    plt.title('Total Orders by Quantity Sold')
    plt.show()

# more than 50% of orders were for only single quantity


#Q.4 Which Inventory hold good no. of  products
def mis_q4():
    print(inventory.groupby('inventory_id')['product_id'].nunique())
#Every product has its own unique inventory

#Q.5 Which Warehouse hold good no. of  products
def mis_q5():
    print(inventory.groupby('warehouse_id')['product_id'].nunique())

#We have only 1 warehouse holding all products across alll categories


#Q.6 Which year had the most returns?
shippings['year']=shippings['shipping_date'].dt.to_period('Y')
rr=shippings[shippings['delivery_status']=='Returned']
returnbyyear=rr.groupby('year')['shipping_id'].count()
totalbyyear=shippings.groupby('year')['shipping_id'].count()

def mis_q6():
    print(returnbyyear)
    print(totalbyyear)
    print(100*returnbyyear/totalbyyear)

# Currently year 2022 have maximum returns and also the return rate is maximum.



#Q.7: What are the total quantities sold across different states (to determine the least-selling states)?
def mis_q7(): 
    custord=customers.merge(orders,on='customer_id',how='inner')
    custorditems=custord.merge(order_items,on='order_id',how='inner')
    Q7=custorditems.groupby('state',as_index=False)['quantity'].sum().sort_values(by='quantity',ascending=True)
    print(Q7)

    plt.figure(figsize=(10,7))
    sns.barplot(data=Q7,x='state',y='quantity',estimator=sum,color='orange')
    plt.title('Total Quantity Sold across States')
    plt.xticks(rotation=70)
    plt.show()


#Q.8 Shipping delays(consider deliveries after 3 day as delayed)

# print(shippings.head(25))
ors=orders.merge(shippings,on='order_id',how='inner')
ors['daystooktodeliver']    =   (ors['shipping_date']- ors['order_date']).dt.days  
delayed_orders = ors[ors['daystooktodeliver'] > 3]

def mis_q8():
    print(delayed_orders)
    print(delayed_orders['daystooktodeliver'].count()/len(shippings['shipping_date']))
    print("Total 8452 orders delivered after 3 day means approximate '40%' of the total")

      

#Q.9 Orders pending shipment 
def mis_q9():
    print(orders['order_status'].isin(['Inprogress']).sum())
    print(orders['order_status'].isin(['Inprogress']).value_counts())

# 499 orders do have pending shipments



# Q.10 Average basket size 
def mis_q10():
    basket_sizes = order_items.groupby('order_id')['quantity'].sum()
    print(basket_sizes.mean())



# def mis_q11():
#     orditems=orders.merge(order_items,on='order_id',how='inner')
#     orditems['revenue'] = orditems['price_per_unit'] * orditems['quantity']
#     orditems['month'] = orditems['order_date'].dt.to_period('M')

#     print(orditems.groupby(['month'])['revenue'].sum())

# ###Q11 Monthly sales trend
def mis_q11():
    orditems=orders.merge(order_items,on='order_id',how='inner')
    orditems['revenue'] = orditems['price_per_unit'] * orditems['quantity']
    orditems['month'] = orditems['order_date'].dt.to_period('M')
    
    q_11=orditems.groupby('month',as_index=False)['revenue'].sum()
    q_11['month'] = q_11['month'].astype(str)
    print(q_11)

     
    plt.figure(figsize=(13,7))
    sns.lineplot(data=q_11,x=q_11['month'],y=q_11['revenue'],color='orange',markersize=10,marker='o',linewidth=2.5)
    plt.xticks(rotation=90)
    plt.show()
    






category_q1()
# category_q2()
category_q3()
# category_q4()

# customer_q1()
# customer_q2()
customer_q3()
# customer_q4()
# customer_q5() 
# customer_q6()
# customer_q7()
# customer_q7_sub1()
# customer_q7_sub2()
# customer_q7_sub3()
# customer_q8()





seller_q1()
# seller_q1_sub1()
seller_q2()
seller_q3()
seller_q4()
# seller_q5()
# seller_q7()
# seller_q7_sub1()
# seller_q8()
# seller_q9()
# seller_q10()


# products_q1()
# products_q1_sub1()
# products_q2()
# products_q3()
products_q4()
# products_q5()



mis_q1()
# mis_q2()
mis_q3()
# mis_q4()
# mis_q5()
# mis_q6()
mis_q7()
# mis_q8()
# mis_q9()
# mis_q10()
mis_q11()

