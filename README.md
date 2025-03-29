## Visitor Entry Exit Management System

VISITOR TYPE = civilian, foreigner, internal, gov agency
PASS TYPE = 
    visitor -> 1 day,
    work pass(ofc employee) -> max 30 days, 
    daily pass(ofc employee) -> 1 day (who forgot id),
    temp veh pass(employee) -> max 1 month,
    visitor(Foreigner) -> 1 day
    work pass -> 1 day
    no pass

Department Names -> civil work, MES, FIre, Horticulture

Admin user -> login, logout
    Visitor -> [id, created_on, updated_on, name, phone, email, pic, address, VISITOR TYPE, gov id,
                gov id no.] -> CRUD operation
    Employee -> [id, employee_id, created_on, updated_on, name, rank, extension no] CRUD operation
    Department -> [id, created_on, updated_on, department name] CRUD operation
    Pass -> [id, created_on, updated_on, PASS TYPE, **local_pass_id**, visitor_id, **employee id**,
            validity, pass_image] CRU operation, In case of no pass, local_pass_id will be null, either 
            visitor id or employee id should be present.
    Visit Log -> [id, created_on, updated_on, pass_id, local_pass_id, PASS TYPE, 
                  whom_to_visit(employee_id), visiting_department(department_id), purpose_of_visit,
                  escorted_by(employee_id), in_datetime, submitted devices, token no,
                  carried devices, vehicle details, out_datetime]
    (AT THE TIME OF LOGGING, CHECK AGAINST PASS TABLE VALIDITY)

1. we need to show how many passes issued today?
2. how many persons are still in the premise.
3. which passes are going to expire soon (default sorting). [DONE]
4. support for filter on Visitor log table -> visitor_id, whom_to_visit, escorted_by, in_datetime, 
   out_datetime, pass type


    
    
