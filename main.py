from flask import Flask,render_template,request,redirect,url_for,flash
import datetime
import psycopg2
def get_connection():
    try:
        return psycopg2.connect(
            database="tfms",
            user="postgres",
            password="charith",
            host="127.0.0.1",
            port=5432,
        )
    except:
        return False
conn = get_connection()
if conn:
    print("Connection to the PostgreSQL established successfully.")
else:
    print("Connection to the PostgreSQL encountered and error.")


app = Flask(__name__)
# app.secret_key = "chchch"

@app.route("/")
def main():
    return render_template("master.html")

@app.route("/supplier",methods=['POST'])
def supplier():
    curr = conn.cursor()
    sql = f"""
INSERT INTO public.bl_sup_register (
    created_by, 
    updated_by, 
    company_id, 
    product_id, 
    reg_no, 
    route_id, 
    partner_id, 
    reg_name, 
    bank_id, 
    bank_account, 
    welfare_registered, 
    saving_scheme_registered, 
    saving_amount, 
    other_scheme_registered, 
    collector, 
    collector_no, 
    branch_id, 
    pay_mode, 
    cf_coins, 
    dob, 
    enrolled_date, 
    notes, 
    bssmsstatus, 
    transporttype, 
    acreage, 
    hectreage, 
    rood, 
    purch, 
    analysiscode01, 
    analysiscode02, 
    analysiscode03, 
    analysiscode04, 
    analysiscode05, 
    advance_status, 
    advance_pay_type, 
    manure_tr_type, 
    manure_tr_id, 
    nic_no, 
    transport_id, 
    bank_account_name, 
    is_active, 
    address_line01, 
    address_line02, 
    address_line03, 
    address_line04, 
    estate_name, 
    telephone, 
    transport_incentive, 
    member_fee, 
    other_fee
) 
VALUES (
    %(created_by)s,
    %(updated_by)s,
    %(company_id)s,
    %(product_id)s,
    %(reg_no)s, 
    %(route_id)s,
    %(partner_id)s,
    %(reg_name)s,
    %(bank_id)s,
    %(bank_account)s, 
    %(welfare_registered)s,
    %(saving_scheme_registered)s,
    %(saving_amount)s, 
    %(other_scheme_registered)s,
    %(collector)s,
    %(collector_no)s,
    %(branch_id)s, 
    %(pay_mode)s,
    %(cf_coins)s, 
    %(dob)s, 
    %(enrolled_date)s, 
    %(notes)s, 
    %(bssmsstatus)s, 
    %(transporttype)s, 
    %(acreage)s, 
    %(hectreage)s, 
    %(rood)s, 
    %(purch)s, 
    %(analysiscode01)s, 
    %(analysiscode02)s, 
    %(analysiscode03)s, 
    %(analysiscode04)s, 
    %(analysiscode05)s, 
    %(advance_status)s, 
    %(advance_pay_type)s, 
    %(manure_tr_type)s, 
    %(manure_tr_id)s, 
    %(nic_no)s, 
    %(transport_id)s, 
    %(bank_account_name)s, 
    %(is_active)s, 
    %(address_line01)s, 
    %(address_line02)s, 
    %(address_line03)s, 
    %(address_line04)s, 
    %(estate_name)s, 
    %(telephone)s, 
    %(transport_incentive)s, 
    %(member_fee)s, 
    %(other_fee)s
)
"""
    
    data = request.form.to_dict()

    for x in data.keys():
        if data[x].strip() == "":
            data[x] = None

    data["welfare_registered"] = bool(request.form.get('welfare_registered'))
    data["advance_status"] = bool(request.form.get('advance_status'))
    data["is_active"] = bool(request.form.get('is_active'))
    data["saving_scheme_registered"] = bool(request.form.get('saving_scheme_registered'))
    data["other_scheme_registered"] = bool(request.form.get('other_scheme_registered'))
    data["collector"] = bool(request.form.get('collector'))

    try:
        
        curr.execute(sql, data)
        conn.commit()
        # flash("Supplier registered successfully!", "success")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        # flash(f"Error registering supplier: {str(error)}", "danger")
        conn.rollback()
    
    finally:
        curr.close()
        return redirect(url_for("main"))
    


@app.route("/route",methods=['POST'])
def route():
    curr = conn.cursor()
    sql = f"""INSERT INTO blg_routemaster (
    created_date, 
    created_by, 
    updated_by, 
    updated_date, 
    company_id, 
    route_code, 
    route_name, 
    last_sup_no, 
    route_order, 
    route_device_no, 
    gps_location, 
    status, 
    active, 
    route_manager_id, 
    consolidation_id, 
    transportid, 
    category_01, 
    category_02, 
    category_03, 
    category_04, 
    category_05
) 
VALUES (
    %(CreatedDate)s,      
    %(CreatedBy)s,              
    %(UpdatedBy)s,               
    %(UpdatedDate)s,    
    %(CompanyId)s,               
    %(RouteCode)s,              
    %(RouteName)s,              
    %(LastSupNo)s,               
    %(RouteOrder)s,               
    %(RouteDeviceNo)s,               
    %(GPSLocation)s,               
    %(Status)s,               
    %(active)s,              
    %(RouteManagerId)s,               
    %(ConsolidationId)s,               
    %(TransportId)s,               
    %(category_01)s,               
    %(category_02)s,               
    %(category_03)s,               
    %(category_04)s,               
    %(category_05)s                
);"""
    data = request.form.to_dict()

    for x in data.keys():
        if data[x].strip() == "":
            data[x] = None

    data["CreatedDate"] = datetime.date.today()
    data["UpdatedDate"] = datetime.date.today()
    data["active"] = True if data["active"] else False

    try:
        
        curr.execute(sql, data)
        conn.commit()
        # flash("Route created successfully", "success")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        curr.close()
        # flash(f"Error: {str(error)}", "danger")

        return redirect(url_for("main"))

if(__name__ == "__main__"):
    app.run(debug=True)