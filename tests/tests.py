import unittest
import json

from application import views
import main

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.client = main.app.test_client()
        main.db.create_all()
        registration_details = {"email":"mutua.charles48@gmail.com","password":"124245yytstts"}
        self.client.post("v1/auth/register",data = json.dumps(registration_details),
                                     content_type='application/json')  
        login_details = {"email":"mutua.charles48@gmail.com","password":"124245yytstts"}
        response =  self.client.post("v1/auth/login",data = json.dumps(login_details),
                                     content_type='application/json')  
        self.token = json.loads(response.get_data())['Authorization']
      
class TestUserRegistration(BaseTest):
    def test_user_registration_using_bad_request(self):
        registration_details = 0 
        
        response =  self.client.post("v1/auth/register",data = registration_details,
                                     content_type='application/json')                     
        self.assertEqual(response.status_code, 400)

    def test_user_can_register(self):
        registration_details = {"email":"mutua1.charles48@gmail.com","password":"124245yytstts"}
        
        response =  self.client.post("v1/auth/register",data = json.dumps(registration_details),
                                     content_type='application/json')                     
        self.assertEqual(response.status_code, 201)

    def test_user_can_regiter_with_missing_data(self):
        registration_details = {"email":"","password":"ssdffsfsfsffsfsffs"}
        response =  self.client.post("v1/auth/register",data = json.dumps(registration_details),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_user_can_register_with_weak_password(self):
        registration_details = {"email":"mutua2.charles48@gmail.com","password":"12"}
        response =  self.client.post("v1/auth/register",data = json.dumps(registration_details),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

class TestCreateBucketList(BaseTest):

    def test_create_bucket_list_using_bad_request(self):
        bucket_list = 0 
        
        response =  self.client.post("v1/bucketlists",data = bucket_list,
                                     headers={'Content-Type':'application/json','Authorization': self.token})                     
        self.assertEqual(response.status_code, 400)
   
    def test_create_bucket_list(self):
        bucket_list = {"name": "BucketList1"}
        response =  self.client.post("v1/bucketlists",data = json.dumps(bucket_list),
                                     headers={'Content-Type':'application/json','Authorization': self.token})                     
        self.assertEqual(response.status_code, 201)

    def test_create_bucket_list_with_missing_data(self):
        bucket_list = {"name": ""}
        response =  self.client.post("v1/bucketlists",data = json.dumps(bucket_list),
                                     headers={'Content-Type':'application/json','Authorization': self.token})                     
        self.assertEqual(response.status_code, 400)

class TestUserLogin(BaseTest):
    def test_user_can_login(self):
        login_details = {"email":"mutua.charles48@gmail.com","password":"124245yytstts"}
        response =  self.client.post("v1/auth/login",data = json.dumps(login_details),
                                     content_type='application/json') 
        self.assertEqual(response.status_code, 200) 

    def test_user_cannot_login_with_wrong_credentials(self):
        login_details = {"email":"mutua.charles48@gmail.com","password":"125yytstts"}
        response =  self.client.post("v1/auth/login",data = json.dumps(login_details),
                                     content_type='application/json') 
        self.assertEqual(response.status_code, 401)
        
class TestGetBucketLists(BaseTest):
    def test_get_bucketlists(self):
        bucket_list = {"name": "BucketList1"}
        response =  self.client.post("v1/bucketlists",data = json.dumps(bucket_list),
                                     headers={'Content-Type':'application/json','Authorization': self.token}) 
        response =  self.client.post("v1/bucketlists", headers={'Content-Type':'application/json','Authorization': self.token})                     
        self.assertEqual(response.status_code, 400)
   


def tearDown(self):
    main.db.drop_all()
    
