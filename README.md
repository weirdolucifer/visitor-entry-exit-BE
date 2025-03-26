## Visitor Entry Exit Management System

VISITOR TYPE = civilian, internal, gov agency
PASS TYPE = daily, limited, NA

Admin user -> login, logout
    Visitor -> [id, created_on, updated_on, name, phone, email, pic, address, VISITOR TYPE, gov id,
                gov id no.] -> CRUD operation
    Pass -> [id, created_on, updated_on, visitor_id, PASS TYPE, validity, pass_image] CRU operation
    Employee -> [id, created_on, updated_on, name, rank, extension no] CRUD operation
    Department -> [id, created_on, updated_on, department name] CRUD operation
    Visit Log -> [id, created_on, updated_on, pass_id, PASS TYPE, visitor_id, _visitor name_, 
                  whom_to_visit(employee_id), visiting_department(department_id), purpose_of_visit,
                  escorted_by(employee_id), in_datetime, submitted devices, carried devices, out_datetime]
    (AT THE TIME OF LOGGING, CHECK AGAINST PASS TABLE VALIDITY)

1. we need to show how many passes issued today -> daily, limited and how many persons are still in
   the premise.
2. need to show, which passes are going to expire soon (default sorting).
3. add (AND) support for filter on Visitor log table -> visitor_id, whom_to_visit, escorted_by, in_datetime, 
   out_datetime, pass type


    
    
