# PricingModuleV2-main
 PricingModuleV2-main
# gfg
 #inorder to run the Django server locally please follow the following steps 

In ( Apple M2 Chip mac version ) 

 1.download and unzip the code
 2.open the code in the vscode
 3.open the terminal inside the PricingModuleV2-Main
 4.Install the virtual environment 

 pip3 install virtualenv

 5.Create Virtual environment 

 python3 -m venv venv

 6.Activate the Environment Variable

 source venv/bin/activate

 7.install django 

 pip install django

 8.install the djanjo rest framework

 pip install djangorestframework

9.please run the server locally by running the command

python manage.py runserver

Please read mopre to understand the pricing module 

the api stand at http://127.0.0.1:8000/calculation_price_api

===> how to test the api result 
1.Press Options to Switch to POST Method
2.In the Content please type the Sample testcase
as 

Test Case 1 :

{
"total_dist":20,
"day":"monday",
"time":1.6,
"waiting_time":10
}

and press post 
the api result will be given as "Pricing",596.6

-------------------

The another way of testing it is through a UI at http://127.0.0.1:8000/drivers
the result will be displayed in the running terminal 

-------------------

As per the requirement the user can alter multiple factors and can make changes to the daily uber or cab services pricing with automation and effective use cases .

----------

for dashboard please visit http://127.0.0.1:8000/dashboard , you can activate and deactivate according to the situation , rememebr not all the modules can be activated as it can lead to the pricing conflict , which has been taken logically on the backend server a pop up will appear if someone tries to do so .

------
developed by Utkarsh Singh 
utkarshsingh001997@gmail.com
8431573174
    